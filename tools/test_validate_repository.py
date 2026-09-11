"""Regression tests for public repository structural validation."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from validate_repository import document_references, validate


class DocumentTests(unittest.TestCase):
    def test_github_fragments_duplicates_unicode_and_explicit_anchors(self):
        anchors, _ = document_references('''# Hello, `world`!
# Hello, `world`!
# Hello-world-1
## Café & sensors
<a id="legacy"></a>
Setext title
------------
```
# Not a heading
```
''')
        self.assertEqual(anchors, {'hello-world', 'hello-world-1', 'hello-world-1-1',
                                   'café--sensors', 'legacy', 'setext-title'})

    def test_links_balanced_paths_html_references_and_ignored_code(self):
        _, links = document_references('''[figure](images/part_(v2).png "Figure")
[space](<images/my part.png>)
[reference][paper]
[paper]: docs/paper.md#result
<video poster="poster.jpg" src="demo.mp4"></video>
`[ignore](missing.md)`
~~~
[ignore](also-missing.md)
~~~
''')
        self.assertEqual(set(links), {'images/part_(v2).png', 'images/my part.png',
                                     'docs/paper.md#result', 'poster.jpg', 'demo.mp4'})


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write('README.md', '# Example\n\n[chapter](docs/chapter.md#second)\n')
        self.write('docs/chapter.md', '# First\n## Second\n')
        self.record = {'id': 'DOC-example', 'sha256': 'a' * 64,
                       'destinations': ['docs/chapter.md#second']}
        self.write_json('project/evidence/source-records.json', [self.record])
        self.write_json('project/evidence/team-work.json', {'contributors': [
            {'contributor': 'Example', 'source_ids': ['DOC-example'],
             'public_chapters': ['docs/chapter.md#second']}]})
        for location in ('subsystems/simulation/media', 'subsystems/airframe/media',
                         'subsystems/multicamera-sensing/presentation'):
            self.write(location + '/sample.txt', 'checked bytes')
            self.write_json(location + ('/manifest.json' if location.endswith('/media') else '/assets-manifest.json'),
                            [{'file': 'sample.txt', 'sha256': hashlib.sha256(b'checked bytes').hexdigest(), 'bytes': 13}])

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')

    def write_json(self, name, data):
        self.write(name, json.dumps(data))

    def errors(self):
        return '\n'.join(validate(self.root)[0])

    def test_valid_fixture_and_ignored_outputs(self):
        self.write('outputs/private.pt', 'not a publication target')
        self.write('.venv/broken.json', '{')
        self.assertEqual(self.errors(), '')

    def test_missing_file_and_fragment(self):
        self.write('README.md', '[gone](missing.md)\n[bad](docs/chapter.md#absent)\n')
        errors = self.errors()
        self.assertIn('missing local target: missing.md', errors)
        self.assertIn('missing fragment: docs/chapter.md#absent', errors)

    def test_encoded_links_html_and_directory_readme_fragments(self):
        self.write('docs/a b.md', '# Café\n')
        self.write('docs/README.md', '# Chapter list\n')
        self.write('README.md', '[unicode](docs/a%20b.md#caf%C3%A9)\n[dir](docs/#chapter-list)\n<a href="docs/chapter.md#second">go</a>')
        self.assertEqual(self.errors(), '')

    def test_record_ids_digest_and_destinations(self):
        self.write_json('project/evidence/source-records.json', [self.record, self.record,
                        {'id': 'other', 'sha256': 'wrong', 'destinations': ['docs/chapter.md#absent']}])
        errors = self.errors()
        self.assertIn('duplicate id', errors)
        self.assertIn('invalid source sha256', errors)
        self.assertIn('missing fragment', errors)

    def test_manifest_hash_byte_count_and_escape(self):
        self.write('subsystems/simulation/media/sample.txt', 'tampered')
        self.write_json('subsystems/multicamera-sensing/presentation/assets-manifest.json', [{'file': '../../../README.md', 'sha256': 'a' * 64}])
        errors = self.errors()
        self.assertIn('SHA-256 mismatch', errors)
        self.assertIn('byte-count mismatch', errors)
        self.assertIn('invalid or duplicate file path', errors)

    def test_discovers_additional_public_subsystem_manifests(self):
        self.write('subsystems/new-subsystem/media/sample.txt', 'new asset')
        self.write_json('subsystems/new-subsystem/media/manifest.json', [
            {'file': 'sample.txt', 'sha256': 'a' * 64}])
        self.assertIn('new-subsystem/media/manifest.json record 0: SHA-256 mismatch', self.errors())

    def test_baseline_manifest_cannot_silently_disappear(self):
        (self.root / 'subsystems/airframe/media/manifest.json').unlink()
        self.assertIn('subsystems/airframe/media/manifest.json: expected non-empty manifest list', self.errors())

    def test_invalid_json_and_model_artifact(self):
        self.write('bad.json', '{"same": 1, "same": 2}')
        self.write('weights.ONNX', 'placeholder')
        errors = self.errors()
        self.assertIn('duplicate JSON key', errors)
        self.assertIn('excluded model artifact suffix', errors)

    def test_code_formatted_link_labels_and_empty_directories(self):
        (self.root / 'presentations/assets').mkdir(parents=True)
        self.write('README.md', '[`gone`](missing.md)\n[`assets`](presentations/assets/)\n')
        errors = self.errors()
        self.assertIn('missing local target: missing.md', errors)
        self.assertIn('empty or excluded local directory: presentations/assets/', errors)

    def test_team_source_ids_chapters_and_catalogue_mapping(self):
        self.write('docs/unmapped.md', '# Unmapped')
        self.write_json('project/evidence/team-work.json', {'contributors': [
            {'contributor': 'Example', 'source_ids': ['DOC-example', 'DOC-missing'],
             'public_chapters': ['docs/chapter.md#absent', 'docs/unmapped.md', 'missing.md']}]})
        errors = self.errors()
        self.assertIn("unknown or invalid source id: 'DOC-missing'", errors)
        self.assertIn('missing fragment: docs/chapter.md#absent', errors)
        self.assertIn('public chapter not mapped by listed source ids: docs/unmapped.md', errors)
        self.assertIn('missing local target: missing.md', errors)

    def test_escape_and_external_urls(self):
        self.write('README.md', '[escape](../outside.md)\n[external](https://example.invalid/)')
        errors = self.errors()
        self.assertIn('link escapes repository', errors)
        self.assertNotIn('example.invalid', errors)


if __name__ == '__main__':
    unittest.main()
