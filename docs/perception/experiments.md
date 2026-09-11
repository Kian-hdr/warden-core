# Vincent’s recorded experiments

Vincent produced two separate six-class still-image experiments. Both used frozen ImageNet-pretrained ResNet18 features and a linear head trained on CPU, with seed 1337. The following values are historical experiment records, not a claim of operational recognition or independently validated generalization.

| Dated record | Collection | Test images | Accuracy | Macro-F1 | Validation-selected epoch |
| --- | --- | ---: | ---: | ---: | ---: |
| August 29, 2026 | Earlier public-stills baseline | 64 | 0.890625 | 0.8625 | 9 |
| August 31, 2026 | Later collected-image linear probe | 291 | 0.9243986254 | 0.9249024129 | 33 |

The later saved confusion matrix contains 269 correct predictions out of 291. These datasets and splits differ, so the table is not a controlled measure of improvement.

## Earlier public-stills baseline

The source records a 390-image inventory across six retained classes, drawn from Wikimedia Commons and Hugging Face sources. Vincent performed the ingest solo. The retained outputs included the selected classifier, evaluation metrics, confusion visualization and per-example errors. A separate third-party detector demonstration was not Vincent’s trained model.

The recorded runtime returned `unknown` for low-confidence input and a fail-safe `unknown` for missing model or unreadable image conditions. `unknown` was abstention, not a seventh trained class. Temporal consistency across video frames was explicitly **not implemented** in the dated baseline; it remained roadmap work.

## Later collected-image probe

The August 31 record describes 1,913 collected images, 1,905 unique images and partitions of 1,331 training, 283 validation and 291 test images. It retains feature arrays, training logs, selected model state and error analysis.

The preparation record reported **77 near-duplicate pairs across splits**. The later preserved collection contains 1,853 images, and **59 split references are missing**, including eight test images. Consequently, the held-out numbers can be optimistic and the preserved image collection alone cannot reproduce the exact training-era evaluation. These are existing evidence limitations, not newly repaired data.

## Publication boundary

The work was offline classification. It did not demonstrate in-flight recognition, transfer across cameras/weather, or flight-control integration. The repository publishes this account and the result history; raw images, embeddings, split files, weights and Vincent’s private implementation remain excluded. Complete source and redistribution permissions are unresolved.

[Dataset versions](dataset.md) · [Perception overview](README.md) · [Team](../project/team.md) · [Model access](../../licensing/model-access.md)

## Source basis

[DOC-33c6ebc61608 and DOC-1e119f1f2ada](../../results/source-records.md) identify the two dated records. The later metrics were also checked against the retained metrics JSON and confusion matrix during the documentation audit on September 11, 2026. No model was executed or retrained.
