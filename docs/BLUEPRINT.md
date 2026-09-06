# DPI Runtime — Research Blueprint

## Purpose

DPI Runtime is an experimental detector-plane observability runtime for
transforming detector-derived intensity structures into structured telemetry,
state trajectories, classification, prediction, and runtime responses.

## Core Research Pipeline

Detector-Plane Signal
→ Observable Extraction
→ Structured Telemetry
→ Session Persistence
→ Trajectory Accumulation
→ Calibration
→ Phase-Space Representation
→ Regime Classification
→ Predictive Observability
→ Interlock Detection
→ Dynamic / Adaptive Runtime

## 1. Observability

Implemented detector-derived observables:

- peak intensity
- mean intensity
- intensity variance
- center of mass
- coherence width
- peak count
- noise strength

Primary implementation:

- core/telemetry/observables.py
- core/telemetry/schema.py

## 2. Runtime Telemetry

Measurements are converted into typed telemetry events and persisted through
runtime sessions.

Components:

- telemetry schema
- session creation
- session manifest
- session registry
- replay
- session comparison

## 3. Calibration

Controlled detector-plane states establish reference observability signatures.

Studied states include:

- coherent
- decoherent
- collapsed
- noisy

## 4. Trajectory Analysis

Repeated observability vectors are treated as trajectories through an
observable state space.

Research includes:

- trajectory accumulation
- trajectory geometry
- trajectory dynamics
- trajectory evolution
- trajectory regions
- trajectory forecasting

## 5. State-Space and Regime Analysis

The runtime explores detector behaviour through:

- phase-space maps
- regime maps
- heuristic semantic-state classification
- KMeans regime clustering
- trajectory region classification

## 6. Predictive Observability

Two predictive approaches are explored:

1. future-regime prediction from observability variables;
2. future-trajectory extrapolation from state-space evolution.

## 7. Runtime Interlocks

Observed states are compared with calibrated baselines to detect:

- coherence-width drift
- peak-count instability
- intensity-variance changes

## 8. Adaptive Runtime

Adaptive experiments close the loop between measured observables and changing
runtime conditions.

Measurement
→ Observables
→ Runtime Assessment
→ Parameter Adaptation
→ New Measurement

## Experimental Runtime Extensions

Later experiments explored progressively more abstract runtime architectures:

- semantic
- cognitive
- meta
- autonomous
- cooperative
- distributed
- hierarchical
- evolutionary

These are retained as experimental extensions rather than treated as the
foundational DPI Runtime.

## Phase 9–11 Research Archive

The later research branch is retained under:

research/phase9-11/

It explores:

- detector federations
- topology graphs
- civilization regions
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

This branch represents a later systems-level extension of the DPI Runtime
research and is intentionally separated from the core runtime architecture.

## Scope Statement

The implemented core of DPI Runtime is:

detector observability
+ telemetry
+ calibration
+ trajectory analysis
+ regime classification
+ prediction
+ interlock detection
+ adaptive runtime experimentation.

The repository is an experimental research runtime, not a production hardware
control system.
