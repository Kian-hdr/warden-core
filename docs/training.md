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
