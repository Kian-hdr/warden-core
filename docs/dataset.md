# Dataset record

The computer-vision work used still images. The archive contains records of an earlier baseline and a later collected-image experiment; they should not be presented as one unchanged benchmark.

## Recorded collected-image experiment

| Item | Recorded amount |
| --- | ---: |
| Training-era image inventory | 1,913 |
| Unique images recorded at training time | 1,905 |
| Training partition | 1,331 |
| Validation partition | 283 |
| Test partition | 291 |
| Images present in the later preserved collection | 1,853 |

The partition totals refer to the recorded experiment. The later preserved collection is a different snapshot: 59 referenced partition images are absent, including eight test images. It therefore cannot currently reproduce the exact training-era dataset on its own.

The original notes report 77 near-duplicate pairs crossing partition boundaries. Those pairs can inflate apparent held-out performance. A new evaluation needs duplicate groups kept together and an immutable, complete dataset version.

## Source and publication status

The earlier baseline’s records name Wikimedia Commons and Hugging Face as source platforms. Platform names are not per-image reuse permissions, and the later collected dataset does not include the provenance document referenced by its results note.

For that reason, this repository describes the collection and workflow but does not redistribute the raw images, embeddings, split files or model weights. Their omission reflects unresolved provenance and reuse permissions, not a claim of a secret operational model.

## What is useful to preserve

The development package retains partition records, feature artifacts, model state, training logs and error analysis. Keeping these together made the collection’s version differences and split-quality issues visible. Future work should add a complete source manifest, per-item rights information, content hashes and a group-aware partition record before publishing or reusing the dataset more broadly.
