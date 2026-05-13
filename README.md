
# DPI Runtime

DPI = Detector-Plane Imaging / Detector-Plane Observability

Experimental observability runtime for detector-plane coherence analysis, trajectory evolution, and runtime telemetry.

---

# Overview

DPI Runtime is an experimental observability framework for studying detector-plane coherence structure, observability vectors, trajectory evolution, and runtime telemetry.

The system models detector-plane observability as a structured runtime environment rather than a simple terminal measurement surface.

The runtime currently supports:

- detector-plane simulation
- observability vector extraction
- calibration states
- trajectory accumulation
- manifold projection
- anomaly/interlock detection
- semantic trajectory regions
- predictive trajectory forecasting

---

# Architecture Philosophy

The runtime treats the detector plane as:

- an observability surface
- a telemetry generation layer
- a coherence-state measurement environment

Rather than focusing only on isolated detector outcomes, the runtime analyzes:

- observability geometry
- coherence degradation
- trajectory evolution
- semantic state regions
- runtime anomaly behavior

---

# Runtime Pipeline

The current runtime pipeline follows:

Detector Plane
→ Observability Extraction
→ Telemetry Persistence
→ Trajectory Evolution
→ Interlock Analysis
→ Forecasting

The system treats detector-plane behavior as a structured observability environment rather than a simple terminal measurement surface.

---

# Current Runtime Capabilities

## Detector-Plane Runtime

Generate detector-plane intensity structures and observability fields.

## Observability Telemetry

Extract structured observability metrics including:

- peak intensity
- mean intensity
- coherence width
- variance
- peak count

## Calibration States

Generate controlled runtime states:

- coherent
- noisy
- decoherent
- collapsed

## Trajectory Geometry

Project observability vectors into manifold space using PCA.

## Interlock Layer

Detect coherence degradation using observability thresholds.

## Predictive Forecasting

Estimate future trajectory drift using manifold evolution.

---

# Project Structure

```text
core/
    runtime/
    telemetry/
    trajectory/
    interlock/
    visualization/

programs/
    runtime/
    calibration/
    analysis/
    interlock/
    benchmarks/

outputs/
    images/
    telemetry/
    trajectories/
    raw/
    sessions/

docs/
tools/
