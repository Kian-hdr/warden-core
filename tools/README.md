# Repository maintenance

These tools inspect local documents and artifact identities. They do not execute a model, simulator or vehicle interface.

From the repository root:

```sh
python3 tools/validate_repository.py
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/verify_media.py
```

The repository validator checks Markdown/HTML paths and anchors, JSON syntax, source-catalogue destinations, the team evidence ledger, media/presentation hashes and prohibited model artifact extensions. It skips generated environments and outputs. This is structural validation, not proof of engineering performance or an exhaustive confidentiality review.

For the executable package, install its development dependencies in a fresh Python 3.11+ environment before testing the CLI subprocesses:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e './software[dev]'
(cd software && python -m pytest)
ruff check --config ruff.toml software tools
```

Confidential model/access terms remain in [licensing](../licensing/model-access.md). Maintenance source uses the [software licence](LICENSE.md).
