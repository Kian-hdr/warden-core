# Warden Core system architecture

Warden Core was developed as a layered robotics system: cloud GPU infrastructure runs large parallel simulations, Isaac Sim supplies the physical scene and sensors, the policy/control stack turns observations into bounded vehicle actions, and the evidence layer records what happened.

## Platform architecture

```mermaid
flowchart TB
    subgraph Local[Local engineering workstation]
        DEV[Source, configuration and review]
        QA[Artifact and media QA]
        ARC[Checksums and archive]
    end

    subgraph Brev[NVIDIA Brev GPU workspace]
        SIM[NVIDIA Isaac Sim 4.5]
        LAB[Isaac Lab 2.1.x]
        ENV[Parallel environments]
        TRAIN[Shared-policy training]
        EVAL[Deterministic evaluation]
        CAM[Virtual cameras]
    end

    DEV --> SIM
    SIM --> LAB --> ENV
    ENV --> TRAIN
    ENV --> EVAL
    ENV --> CAM
    TRAIN --> ARC
    EVAL --> ARC
    CAM --> QA --> ARC
```

The remote workspace provided the NVIDIA GPU, simulator runtime and parallel execution capacity. The local workstation handled source preparation, review and durable preservation. Run identity and content hashes connected both sides.

## Simulation and control loop

The verified runtime used a 250 Hz physics loop and a 50 Hz policy loop. Five physics steps therefore occur for every policy decision.

```mermaid
sequenceDiagram
    participant Physics as Isaac physics (250 Hz)
    participant Obs as Observation builder
    participant Policy as Shared policy (50 Hz)
    participant Control as Rate control + mixer
    participant Evidence as Telemetry recorder

    loop Five physics steps
        Physics->>Obs: State, contacts, rotor data
        Obs->>Evidence: Timestamped state
    end
    Obs->>Policy: 260-value actor observation
    Policy->>Control: Bounded action
    Control->>Physics: Rotor allocation
    Control->>Evidence: Action and safety state
```

The actor and critic have separate information contracts. The actor consumes a 260-value history built from four 65-value frames. The critic receives a 290-value representation with additional training-time context. This asymmetric structure lets the training system use richer simulator information while keeping the deployed policy input contract compact.

## Observation-to-action path

```mermaid
flowchart LR
    S[Vehicle and course state] --> F[65-value frame]
    F --> H[Four-frame history]
    H --> A[260-value actor input]
    H --> C[290-value critic input]
    A --> P[Policy network]
    P --> U[Mass-normalized thrust and desired body rates]
    U --> PID[Bounded rate control]
    PID --> MIX[Quad-X allocation and desaturation]
    MIX --> ROT[Simulated rotors]
```

The controller includes anti-windup, slew limits, motor lag and ordered desaturation. The Phase C qualification exercised this path over 800 cases and exact replay in fresh Isaac processes.

## Course and reward structure

The course representation tracks ordered gate progress, directed crossing and collision-aware clearance. Dense shaping is accumulated in a bounded episodic ledger; valid completion and invalid terminal outcomes are separated by terminal terms. The exact formula and coefficient table are published in the [reward-policy chapter](../reward-and-evaluation/reward-policy.md).

```mermaid
flowchart LR
    G[Ordered gates] --> Q[Course coordinate]
    X[Vehicle pose and velocity] --> Q
    Q --> R[Progress, alignment, clearance and smoothness terms]
    R --> L[Bounded shaping ledger]
    L --> T[Terminal reward]
    T --> RET[Recorded episodic return]
```

## Evidence and reproducibility layer

Every major stage emits artifacts with explicit identity:

| Layer | Recorded artifacts |
| --- | --- |
| Source | Git revision, tree identity, component hashes |
| Experiment | Frozen configuration, seed, environment count, runtime versions |
| Runtime | Telemetry, metrics, contact state, camera frames |
| Learning | Update records, checkpoint index, closed-source policy state |
| Evaluation | Scenario summaries, replay comparison, aggregate metrics |
| Media | Source run, encode properties, representative frames, visual review |
| Delivery | Relative-file checksums, manifests and immutable package ledgers |

This structure supported exact replay comparison, independent media review and recovery of interrupted cloud work. The [experiment-artifact chapter](artifact-lineage.md) explains the packaging mechanics, and [verified engineering results](../../../project/evidence/README.md) collects the completed numerical outcomes.

## Public and private boundary

The public repository contains architecture, interfaces, mathematical policy documentation, runnable observability tools and selected verified media. Model weights remain closed source under the [model-access policy](../../../licensing/model-access.md). Upstream simulator and robot assets retain their own licences and notices in [`third_party/`](../../../licensing/third-party/README.md).
