# Training and evaluation workflow

The simulation archive includes checkpointed reinforcement-learning experiments. The useful engineering progress was building a repeatable path from a recorded environment configuration to logs, checkpoints and a separate evaluation record.

## What was retained

- Source revision and runtime identity for the experiment.
- Frozen configuration and seed information.
- Training logs and checkpoint artifacts.
- Evaluation records where evaluation ran.
- Frame sequences, video candidates and their labels.
- Checksums and recovery records for exported files.

These records support inspection and recovery. A checkpoint by itself says that model state was saved; it does not say that the model met the intended task requirements.

## The development sequence

1. Establish the simulation environment and a small repeatable integration run.
2. Record the experiment configuration before starting training.
3. Save model state and logs during the run.
4. Evaluate separately from the training loop, keeping the configuration and conditions identifiable.
5. Inspect recorded behavior before selecting material for a presentation.
6. Preserve the outputs and enough context to continue the work later.

Parallel environments were part of the development workflow. Infrastructure exercises and learning experiments were recorded separately, so increasing the amount of simulation running at once did not become a claim of better learned behavior.

## How to read the videos

The [gallery](../media/README.md) distinguishes early PPO checkpoint playback, behavioral-baseline course views, scripted parallel-scene visualization and camera calibration. Each clip is labelled for its actual role. The two-second PPO recording shows the agent near the start, not completed gate racing; the longer course views are non-learned baselines.

The [reward-policy overview](reward-policy-overview.md) explains the terminology and structure of the retained design records. [Source coverage](vault-source-coverage.md) identifies the public summaries and original documents retained privately.

## How the historical records fit together

The earliest training specification defined separate baseline, learning and playback roles. Later source and run records added implementation and saved checkpoint artifacts. Those later artifacts supersede an earlier statement that no Warden-specific checkpoint existed, but they do not turn the initial plan into a completed evaluation.

The later acro-racing design was a separate simulation profile. It superseded the racing-design portion of the earlier specification rather than replacing every operational assumption. The retained run history then records saved Stage0 training state, while the subsequent frozen evaluation did not produce a completed promotion record. Documentation of preserved partial/failure evidence is part of recovery work, not a trained-policy success.

| Record type | What it contributes to the engineering history |
| --- | --- |
| Initial specification | The intended component roles and experiment contract. |
| Later design revision | A separately identified simulation design and its implementation boundaries. |
| Implementation records | Source revisions and checks associated with the work. |
| Saved checkpoint artifacts | Recoverable model state from recorded experiments. |
| Evaluation records | The actual scope and outcome of a candidate assessment. |
| Published footage | A labelled view of the specific checkpoint, baseline or visualization recorded. |

The two-second public PPO clip is initial upstream checkpoint playback. The longer chase and FPV clips are behavioral baselines. They were selected from different camera-development revisions, so they should not be treated as synchronized views of one learned-policy run.

[Experiment-to-artifact workflow](experiment-artifacts.md) explains how these records are connected. [Source records](source-records.md) preserve the identities of the archived documents used in this public account.

## Source basis

This public explanation is grounded in the dated project records identified in the [source records for this chapter](source-records.md#chapter-docs-training-md). The catalogue distinguishes complete notices from adapted explanations and preserves separate document versions.
