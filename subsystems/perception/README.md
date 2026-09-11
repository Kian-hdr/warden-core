# Computer-vision model

[Overview](docs/README.md) · [Dated experiments](docs/experiments.md) · [Dataset record](docs/dataset.md)

[Vincent · vwiczk](https://github.com/vwiczk) developed the separate offline computer-vision baseline for supervised object identification. The experiment uses a frozen ImageNet-pretrained ResNet18 feature extractor and a trainable linear classification head.

## Model pipeline

```mermaid
flowchart LR
    I[Collected still image] --> P[Resize and normalize]
    P --> R[Frozen ResNet18 backbone]
    R --> F[Feature vector]
    F --> L[Linear classification head]
    L --> C[Six class scores]
    C --> D[Supported class or unknown]
```

Freezing the backbone separates the pretrained visual representation from the project’s smaller supervised experiment. The linear head learns the mapping from saved feature vectors to six aircraft/background classes on CPU.

## Recorded classes

| Class | Role in the experiment |
| --- | --- |
| `shahed_series_uav` | Dataset-supported Shahed-series still images |
| `other_combat_uav` | Other combat-UAV examples |
| `civilian_drone` | Civilian/commercial drone examples |
| `crewed_fixed_wing` | Crewed fixed-wing aircraft |
| `crewed_rotary_wing` | Crewed rotorcraft |
| `background` | Non-aircraft/background examples |

## Training and evaluation record

The public baseline record identifies seed `1337`, a validation-selected checkpoint and a held-out evaluation of 64 images. The recorded score is 0.891 accuracy and 0.863 macro-F1. Class-level analysis, confusion records and data-partition identities remain associated with the experiment.

The dated baseline records confidence-based abstention and fail-safe `unknown` for missing model or unreadable image conditions. Temporal consistency across video frames was explicitly not implemented and remained roadmap work. `unknown` is abstention, not a trained class.

[The two dated experiments](docs/experiments.md) preserve the earlier and later results separately, with their split-quality and preservation limitations.

## Relationship to the other subsystems

The perception baseline is an offline supervised experiment. It has its own data, training and evaluation history and is documented separately from the Isaac policy and physical controller work.

[Detailed perception record](docs/README.md) · [Dataset record](docs/dataset.md) · [Verified results](../../project/evidence/README.md)

Vincent’s underlying dataset, embeddings, checkpoint and model code are not distributed here. They are excluded from the public licence grants; this repository grants no access or rights to Vincent’s underlying work. Model artifacts remain confidential; see the [model-access policy](../../licensing/model-access.md).
