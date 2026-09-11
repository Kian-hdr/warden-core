"""Offline checks for the public documentation repository (Python standard library).

Checks JSON syntax, local Markdown/HTML links, document fragments, source-record
identities/destinations, team source mappings, manifest bytes, and excluded model
artifact suffixes.
This is a structural check, not factual review, confidentiality certification,
or verification of engineering results. It never runs project/model code.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP = {'.git', '.venv', 'venv', 'env', 'node_modules', '__pycache__',
        '.pytest_cache', '.ruff_cache', '.mypy_cache', 'outputs', 'output', 'build', 'dist'}
MODEL_SUFFIXES = {'.pt', '.pth', '.ckpt', '.onnx', '.safetensors', '.engine',
                  '.plan', '.tflite', '.h5', '.hdf5', '.pb', '.gguf', '.ggml'}
SHA256 = re.compile(r'[0-9a-f]{64}\Z')


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src', 'poster'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if attrs.get('id'):
            self.anchors.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.anchors.add(attrs['name'])

    handle_startendtag = handle_starttag


def without_fences(text):
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append('')
        else:
            lines.append(line if fence is None else '')
    return '\n'.join(lines)


def heading_slug(heading):
    heading = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', heading)
    heading = unescape(re.sub(r'<[^>]*>', '', heading)).lower()
    heading = heading.replace('`', '').replace('*', '').replace('~', '')
    # GitHub removes punctuation/symbols but retains hyphens and underscores.
    heading = ''.join(c for c in heading if c in '-_' or
                      unicodedata.category(c)[0] not in 'PS')
    return re.sub(r'\s', '-', heading.strip())


def document_references(text, markdown=True):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = without_fences(text) if markdown else text
    parser = HTMLReferences()
    parser.feed(text)
    anchors, links = set(parser.anchors), list(parser.links)
    if not markdown:
        return anchors, links
    used = set()
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$', line)
        heading = match.group(1) if match else None
        if heading is None and index + 1 < len(lines) and line.strip() and re.match(
                r'^ {0,3}(?:=+|-+)\s*$', lines[index + 1]):
            heading = line.strip()
        if heading is not None:
            base = heading_slug(heading)
            slug, count = base, 0
            while slug in used:
                count += 1
                slug = base + '-' + str(count)
            used.add(slug)
            anchors.add(slug)
    text = re.sub(r'(`+).*?\1', '', text)
    definitions = {}
    for match in re.finditer(r'^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)', text, re.MULTILINE):
        definitions[' '.join(match[1].lower().split())] = match[2].strip('<>')
    links.extend(definitions.values())
    # Balanced parentheses support ordinary paths such as image_(final).png.
    for match in re.finditer(r'!?\[[^\]\n]*\]\(', text):
        start = match.end()
        if start < len(text) and text[start] == '<':
            end = text.find('>', start + 1)
            if end >= 0:
                links.append(text[start + 1:end])
            continue
        pos, depth = start, 0
        while pos < len(text):
            c = text[pos]
            if c == '\\':
                pos += 2
                continue
            if c == '(':
                depth += 1
            elif c == ')':
                if depth == 0:
                    break
                depth -= 1
            elif c.isspace() and depth == 0:
                break
            pos += 1
        links.append(re.sub(r'\\([() ])', r'\1', text[start:pos]))
    return anchors, links


def unique_json(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def validate(root):
    root = Path(root).resolve()
    errors, files = [], []
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not Path(directory, d).is_symlink())
        files.extend(Path(directory, name) for name in sorted(names))
    included_files = {path for path in files if not path.is_symlink()}
    json_data, documents = {}, {}
    for path in files:
        label = str(path.relative_to(root))
        if path.is_symlink():
            errors.append(label + ': symlink must be reviewed; validator does not follow it')
            continue
        if path.suffix.lower() in MODEL_SUFFIXES:
            errors.append(label + ': excluded model artifact suffix')
        try:
            if path.suffix.lower() == '.json':
                json_data[path] = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_json,
                                             parse_constant=lambda x: (_ for _ in ()).throw(ValueError('invalid JSON constant ' + x)))
            if path.suffix.lower() in {'.md', '.markdown', '.html', '.htm'}:
                documents[path] = document_references(path.read_text(encoding='utf-8'), path.suffix.lower() in {'.md', '.markdown'})
        except (OSError, ValueError) as exc:
            errors.append(label + ': ' + str(exc))

    def check_link(source, link, root_relative=False):
        label = str(source.relative_to(root))
        try:
            parsed = urlsplit(unescape(link))
        except ValueError as exc:
            errors.append(label + ': invalid link ' + repr(link) + ': ' + str(exc))
            return
        if parsed.scheme or parsed.netloc:
            if root_relative:
                errors.append(label + ': source destination must be local: ' + link)
            return
        base = root if root_relative or parsed.path.startswith('/') else source.parent
        target = (base / unquote(parsed.path).lstrip('/')).resolve() if parsed.path else source
        if target != root and root not in target.parents:
            errors.append(label + ': link escapes repository: ' + link)
        elif not target.exists():
            errors.append(label + ': missing local target: ' + link)
        elif target.is_dir() and not any(target in path.parents for path in included_files):
            errors.append(label + ': empty or excluded local directory: ' + link)
        elif parsed.fragment:
            if target.is_dir():
                target = next((target / n for n in ('README.md', 'index.html') if (target / n).is_file()), target)
            if target in documents and unquote(parsed.fragment) not in documents[target][0]:
                errors.append(label + ': missing fragment: ' + link)
            elif root_relative and target not in documents:
                errors.append(label + ': cannot validate source destination fragment: ' + link)

    for path, (_, links) in documents.items():
        for link in sorted(set(links)):
            check_link(path, link)

    records_path = root / 'project/evidence/source-records.json'
    records = json_data.get(records_path)
    source_destinations = {}
    if not isinstance(records, list) or not records:
        errors.append('project/evidence/source-records.json: expected non-empty list')
    else:
        seen = set()
        for index, record in enumerate(records):
            label = 'project/evidence/source-records.json record ' + str(index)
            if not isinstance(record, dict):
                errors.append(label + ': expected object')
                continue
            identity = record.get('id')
            if not isinstance(identity, str) or not identity or identity in seen:
                errors.append(label + ': missing, invalid or duplicate id')
            else:
                seen.add(identity)
                source_destinations[identity] = set()
            if not isinstance(record.get('sha256'), str) or not SHA256.fullmatch(record['sha256']):
                errors.append(label + ': invalid source sha256')
            destinations = record.get('destinations')
            if not isinstance(destinations, list) or not destinations:
                errors.append(label + ': expected non-empty destinations list')
            else:
                for destination in destinations:
                    if not isinstance(destination, str) or not destination:
                        errors.append(label + ': invalid destination')
                    else:
                        check_link(records_path, destination, root_relative=True)
                        if isinstance(identity, str) and identity in source_destinations:
                            source_destinations[identity].add(destination.split('#', 1)[0])

    team_path = root / 'project/evidence/team-work.json'
    team = json_data.get(team_path)
    contributors = team.get('contributors') if isinstance(team, dict) else None
    if not isinstance(contributors, list) or not contributors:
        errors.append('project/evidence/team-work.json: expected non-empty contributors list')
    else:
        seen_names = set()
        for index, contributor in enumerate(contributors):
            label = 'project/evidence/team-work.json contributor ' + str(index)
            if not isinstance(contributor, dict):
                errors.append(label + ': expected object')
                continue
            name = contributor.get('contributor')
            if not isinstance(name, str) or not name.strip() or name in seen_names:
                errors.append(label + ': missing, invalid or duplicate contributor')
            else:
                seen_names.add(name)
            source_ids = contributor.get('source_ids')
            eligible_chapters = set()
            if not isinstance(source_ids, list) or not source_ids:
                errors.append(label + ': expected non-empty source_ids list')
            else:
                seen_ids = set()
                for identity in source_ids:
                    if not isinstance(identity, str) or identity not in source_destinations:
                        errors.append(label + ': unknown or invalid source id: ' + repr(identity))
                    elif identity in seen_ids:
                        errors.append(label + ': duplicate source id: ' + identity)
                    else:
                        seen_ids.add(identity)
                        eligible_chapters.update(source_destinations[identity])
            chapters = contributor.get('public_chapters')
            if not isinstance(chapters, list) or not chapters:
                errors.append(label + ': expected non-empty public_chapters list')
            else:
                seen_chapters = set()
                for chapter in chapters:
                    if not isinstance(chapter, str) or not chapter:
                        errors.append(label + ': invalid public chapter')
                        continue
                    check_link(team_path, chapter, root_relative=True)
                    if chapter in seen_chapters:
                        errors.append(label + ': duplicate public chapter: ' + chapter)
                    seen_chapters.add(chapter)
                    if chapter.split('#', 1)[0] not in eligible_chapters:
                        errors.append(label + ': public chapter not mapped by listed source ids: ' + chapter)

    # Require the published baseline manifests, while including future subsystem
    # media/presentation manifests without scanning generated or private trees.
    manifest_paths = {
        root / 'subsystems/simulation/media/manifest.json',
        root / 'subsystems/airframe/media/manifest.json',
        root / 'subsystems/multicamera-sensing/presentation/assets-manifest.json',
    }
    for path in included_files:
        parts = path.relative_to(root).parts
        if len(parts) >= 4 and parts[0] == 'subsystems' and (
                (path.name == 'manifest.json' and 'media' in parts[2:-1]) or
                (path.name == 'assets-manifest.json' and 'presentation' in parts[2:-1])):
            manifest_paths.add(path)
    for path in sorted(manifest_paths):
        relative = str(path.relative_to(root))
        records = json_data.get(path)
        if not isinstance(records, list) or not records:
            errors.append(relative + ': expected non-empty manifest list')
            continue
        seen = set()
        for index, record in enumerate(records):
            label = relative + ' record ' + str(index)
            if not isinstance(record, dict):
                errors.append(label + ': expected object')
                continue
            name, digest = record.get('file'), record.get('sha256')
            if not isinstance(name, str) or not name or '\\' in name or Path(name).is_absolute() or '..' in Path(name).parts or name in seen:
                errors.append(label + ': invalid or duplicate file path')
                continue
            seen.add(name)
            target = (path.parent / name).resolve()
            if path.parent not in target.parents or not target.is_file():
                errors.append(label + ': missing or escaping manifest target: ' + name)
                continue
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                errors.append(label + ': invalid sha256')
                continue
            actual = hashlib.sha256()
            with target.open('rb') as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                    actual.update(chunk)
            if actual.hexdigest() != digest:
                errors.append(label + ': SHA-256 mismatch: ' + name)
            if 'bytes' in record and (type(record['bytes']) is not int or record['bytes'] != target.stat().st_size):
                errors.append(label + ': byte-count mismatch: ' + name)
    return errors, len(files), len(documents), len(json_data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error('--root must be an existing directory')
    errors, files, documents, json_files = validate(args.root)
    for error in errors:
        print('ERROR: ' + error, file=sys.stderr)
    print(f'Checked {files} files, {documents} documents, {json_files} JSON files; {len(errors)} errors.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
