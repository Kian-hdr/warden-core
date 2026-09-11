# How we develop

The difficult part of a robotics prototype is keeping the software, simulation and hardware work connected without letting progress in one stand in for progress in another.

## Make behavior inspectable

A pipeline needs more than an average runtime. The software package records individual events and resource samples so an assessment can be traced back to the data that produced it. Its tests exercise parsing, capture assembly and assessment behavior. Example data is synthetic and demonstrates the tools, not hardware performance.

## Keep the design editable

LL-11 is a connected multibay landing-leg concept expressed in parametric CAD. The source keeps the design editable, while STEP and STL exports make the geometry accessible without running the generator. The hardware notes describe the assumptions and the remaining physical checks.

## Separate the milestones

- A passing software test establishes the behavior covered by that test.
- A valid CAD solid establishes digital geometry, not a printable or load-qualified part.
- A mechanical calculation is a model under stated assumptions, not a measured result.
- A simulation result applies to its recorded configuration and conditions.
- Physical fit, repeatability and performance need their own measurements.

## Project leadership

My role connected simulation and evaluation work with hardware development, the team handoff and the project presentation. Keeping source, outputs and limitations together makes it easier for someone else to review the work and continue it. This public collection follows that same structure: source beside usage instructions, tests beside software, and CAD beside its limitations.

## Diagnosing interfaces before interpreting results

The preserved simulation-interface records show why the meaning of recorded data needs to be checked independently of a success counter. The investigation distinguished clock domains, coordinate-frame interpretation and simulator ground-truth records from the higher-level experiment’s measurements. Earlier trial descriptions and later corrections were retained together instead of treating the first report as the final account.

The engineering lesson is a method for investigating interfaces: establish what a timestamp and state field mean, compare them with an independent reference, and keep a correction associated with the record it changes. This public account describes that diagnostic discipline without reproducing controller tuning, operating commands or task-performance figures from the internal trials.

## Source basis

The [source records for this chapter](../results/source-records.md#chapter-docs-development-md) identify the archived versions used in this public explanation.
