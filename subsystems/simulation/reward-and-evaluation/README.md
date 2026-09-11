# Policies and mathematical specifications

This is the canonical entry point for the public Warden Core policy layer. It contains the exact reward mathematics, the observation/action interface and the evaluation method used to judge recorded results.

| Specification | Contents |
| --- | --- |
| [Reward policy](reward-policy.md) | Dense shaping equation, nine coefficients, clearance barrier, bounded episodic ledger, terminal reward and terminal-dominance proof. |
| [Observation and action contracts](observation-action-contracts.md) | Actor/critic inputs, temporal history, policy output and control-rate boundary. |
| [Evaluation methodology](evaluation-methodology.md) | Frozen cases, fresh-process replay, safety checks, evidence identity and media review. |

Completed numerical outcomes are in [verified results](../../../project/evidence/README.md). Model binaries remain closed source under the [model-access policy](../../../licensing/model-access.md).
