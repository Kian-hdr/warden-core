# Computer-vision baseline

Vincent developed the team’s separate offline computer-vision experiment. It used frozen ImageNet-pretrained ResNet18 features and a linear classification head trained on CPU. This provided a compact baseline that could be inspected through its saved inputs, training log and error analysis.

## What the work produced

The collected-stills experiment covered six aircraft/background classes. Its retained package includes a checkpoint, extracted features, training log, confusion matrix and error records. The saved run records seed 1337 and validation-based selection of epoch 33.

The workflow separated feature extraction from training the classification head. Training, validation and test partitions were recorded, and class-level errors were retained alongside the aggregate results. This produced an inspectable experiment rather than a few hand-picked examples.

## Dataset and evaluation scope

The [dataset record](dataset.md) describes the collected set and recorded partitions. The experiment was still-image classification, not object detection or recognition during flight. Its records identify near-duplicate images crossing partition boundaries, so its historical test score should not be treated as an independent measure of real-world generalization. We do not use that score as a headline capability claim.

The perception experiment was not integrated into a demonstrated autonomous flight system. Awareness and avoidance remain separate from any inference about intent; no targeting or engagement function is published here.

## Next step

A stronger follow-up would establish source and reuse permissions for each image, group duplicates before partitioning, freeze a complete dataset version, and evaluate on fresh sources and capture conditions. That would make future results more meaningful than simply fitting a larger model to the same collection.
