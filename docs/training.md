# Training and evaluation workflow

The simulation archive includes checkpointed reinforcement-learning experiments. The useful engineering progress was building a repeatable path from a recorded environment configuration to logs, checkpoints and a separate evaluation record.

## What was retained

- Source revision and runtime identity for the experiment.
- Frozen configuration and seed information.
- Training logs and checkpoint artifacts.
- Evaluation records where evaluation ran.
- Frame sequences, video candidates and their labels.
- Checksums and recovery records for exported files.

These records support inspection, reproducibility and recovery. Model weights and checkpoint bytes remain closed source under the [model-access policy](../MODEL-ACCESS.md).

## The development sequence

1. Establish the simulation environment and a small repeatable integration run.
2. Record the experiment configuration before starting training.
3. Save model state and logs during the run.
4. Evaluate separately from the training loop, keeping the configuration and conditions identifiable.
5. Inspect recorded behavior before selecting material for a presentation.
6. Preserve the outputs and enough context to continue the work later.

Parallel environments were part of the development workflow. The completed scale profile measured five environment counts across three seeds and selected 2,048 environments at 64,094.408 transitions per second under the recorded throughput/headroom rule.

## How to read the videos

The [gallery](../media/README.md) leads with the verified model-based autonomous corridor flight and a reviewed simulation montage. Separate chase and first-person views show the mapped-course camera workflow, while the physical-prototype recording documents the assembled airframe hovering outdoors.

The [acro-racing reward-policy specification](reward-policy-overview.md) reproduces the recorded reward equations, term coefficients, bounded ledger and terminal-dominance proof. [Source coverage](vault-source-coverage.md) identifies that adapted scope and the complete original documents retained privately.

## How the historical records fit together

The training history connects the initial experiment specification to implemented control/observation contracts, real-Isaac integration, deterministic dynamics qualification, a measured parallelism profile and a retained Stage 0 training tranche. Each result keeps its run identity and source revision.

| Record type | What it contributes to the engineering history |
| --- | --- |
| Initial specification | Component roles and the experiment contract. |
| Implemented contracts | Control, observation, course, reward and evidence interfaces. |
| Real-Isaac qualification | Source-linked integration, dynamics and exact replay results. |
| Scale profile | A five-rung, three-seed measurement of parallel execution. |
| Stage 0 package | Ten accepted updates, 1,310,720 transitions and hash-bound model-state records. |
| Published footage | Independently reviewed autonomous trajectory control and camera outputs. |

[Experiment-to-artifact workflow](experiment-artifacts.md) explains how these records are connected. [Source records](source-records.md) preserve the identities of the archived documents used in this public account.

## Source basis

This public explanation is grounded in the dated project records identified in the [source records for this chapter](source-records.md#chapter-docs-training-md). The catalogue distinguishes complete notices from adapted explanations and preserves separate document versions.
