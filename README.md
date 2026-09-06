# DPI Runtime

**Experimental detector-plane observability runtime**

DPI Runtime explores how detector-plane measurements can be transformed into
structured observables, telemetry, evolving measurement states, trajectories,
classification, prediction, interlocks, and adaptive runtime responses.

It extends Detector-Plane Imaging research from static measurement
representation toward stateful measurement observability.

---

## Core Research Pipeline

~~~text
Detector-Plane Signal
        ↓
Observable Extraction
        ↓
Structured Telemetry
        ↓
Session Persistence
        ↓
Trajectory Accumulation
        ↓
Calibration
        ↓
Phase-Space Representation
        ↓
Regime Classification
        ↓
Predictive Observability
        ↓
Interlock Detection
        ↓
Adaptive Runtime Response
~~~

---

## Core Observables

The runtime currently extracts:

- peak intensity
- mean intensity
- intensity variance
- center of mass
- coherence width
- peak count
- noise strength

Core implementation:

~~~text
core/telemetry/
├── observables.py
└── schema.py
~~~

---

## Telemetry and Reproducibility

Runtime measurements are stored as structured telemetry and organized into
reproducible sessions.

Implemented capabilities include:

- typed telemetry events
- session identifiers
- session manifests
- session registry
- trajectory persistence
- session replay
- session comparison

~~~text
core/
├── telemetry/
├── session/
├── registry/
├── replay/
└── trajectory/
~~~

---

## Calibration

Controlled detector-plane states are used to establish reference observability
signatures.

Current experimental calibration states:

- coherent
- noisy
- decoherent
- collapsed

Program:

~~~text
programs/calibration/dpi_state_calibration.py
~~~

---

## State-Space and Trajectory Analysis

Repeated observability vectors are treated as evolving trajectories through a
measurement-state space.

Research programs explore:

- phase-space maps
- trajectory geometry
- trajectory dynamics
- trajectory evolution
- trajectory-region classification
- trajectory forecasting

~~~text
programs/analysis/
~~~

---

## Regime Classification

The repository explores multiple forms of measurement-state classification,
including:

- rule-based semantic states
- observability-region classification
- KMeans clustering of phase-space variables

These are experimental classification approaches rather than universal
physical-state labels.

---

## Predictive Observability

The runtime explores two predictive directions:

1. prediction of future observability regimes;
2. extrapolation of future measurement trajectories.

The current predictive experiments operate on controlled simulated
observability data.

---

## Interlock Layer

Calibration-derived baselines are used to detect measurement-state anomalies
including:

- coherence-width drift
- peak-count instability
- intensity-variance collapse

Program:

~~~text
programs/interlock/dpi_interlock_demo.py
~~~

---

## Adaptive Runtime

The adaptive runtime closes an experimental feedback loop:

~~~text
Measurement
→ Observables
→ Runtime Assessment
→ Parameter Adaptation
→ New Measurement
~~~

Program:

~~~text
programs/runtime/dpi_adaptive_runtime.py
~~~

---

## Runtime Experiments

The research later expanded into increasingly complex runtime experiments:

- dynamic
- adaptive
- semantic
- cognitive
- meta
- autonomous
- cooperative
- distributed
- hierarchical
- evolutionary

These experiments remain under:

~~~text
programs/runtime/
~~~

They are retained as research extensions rather than treated as equivalent to
the foundational runtime core.

---

## Phase 9–11 Systems Research

Later systems-level experiments are preserved separately under:

~~~text
research/phase9-11/
~~~

This research explored:

- detector federations
- topology
- regional organization
- distributed semantic memory
- recursive consensus
- trust ecology
- governance
- constitutional evolution
- inheritance
- diplomacy
- meta-governance
- observer feedback
- field integration

See:

~~~text
research/phase9-11/README.md
~~~

---

## Repository Structure

~~~text
dpi-runtime/
├── core/
├── programs/
├── research/
│   └── phase9-11/
├── docs/
│   ├── BLUEPRINT.md
│   └── VERIFICATION.md
├── tools/
├── requirements.txt
└── README.md
~~~

---

## Verification

The cleaned core research pipeline was executed successfully on 2026-09-06.

Verified stages:

1. detector observability and telemetry
2. calibration
3. phase-space generation
4. regime classification
5. predictive observability
6. observability interlocks
7. adaptive runtime response

See:

~~~text
docs/VERIFICATION.md
~~~

---

## Research Scope

DPI Runtime is an experimental research framework.

It demonstrates software architectures for:

- detector observability
- structured measurement telemetry
- measurement-state tracking
- trajectory analysis
- state classification
- predictive observability
- anomaly/interlock detection
- adaptive feedback experiments

It is not presented as a production detector controller or as validation
against physical hardware.

External and cross-dataset validation belongs to the separate
`dpi-validation-framework` project.

---

## Related Work

- `detector-plane-imaging` — foundational detector-plane measurement research
- `dpi-validation-framework` — cross-dataset and empirical validation research
- `dpi-runtime` — stateful observability and runtime research
