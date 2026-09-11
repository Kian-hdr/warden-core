"""Verify public media file identities. Added for the documentation edition.

This utility compares local files with the published manifest; it does not
interpret experiment results or execute media/model content.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import sys


def verify(manifest_path):
    manifest_path = Path(manifest_path).resolve()
    root = manifest_path.parent
    records = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("manifest must be a non-empty list")
    checked = []
    seen = set()
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("each record must be an object")
        name, expected = item.get("file"), item.get("sha256")
        if not isinstance(name, str) or "\\" in name:
            raise ValueError("file must be a relative POSIX path")
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or name in seen:
            raise ValueError("file paths must be unique and stay inside the media directory")
        if not isinstance(expected, str) or re.fullmatch(r"[0-9a-f]{64}", expected) is None:
            raise ValueError("sha256 must contain 64 lowercase hexadecimal characters")
        target = (root / relative).resolve()
        if root not in target.parents or not target.is_file():
            raise ValueError("listed file is missing or outside the media directory: " + name)
        digest = hashlib.sha256()
        with target.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != expected:
            raise ValueError("SHA-256 mismatch: " + name)
        checked.append(name)
        seen.add(name)
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=Path(__file__).resolve().parents[1] / "media" / "video-manifest.json")
    args = parser.parse_args()
    try:
        checked = verify(args.manifest)
    except (OSError, ValueError) as exc:
        print("Verification failed: " + str(exc), file=sys.stderr)
        return 1
    print("Verified " + str(len(checked)) + " media files")
    for name in checked:
        print("  " + name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
