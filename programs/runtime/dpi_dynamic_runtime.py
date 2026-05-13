import json
import numpy as np
import matplotlib.pyplot as plt

from core.telemetry.observables import extract_observables
from core.telemetry.schema import build_telemetry_event
from core.trajectory.trajectory import append_observables
from core.session.session import create_runtime_session

# ----------------------------------------
# CREATE SESSION
# ----------------------------------------

session = create_runtime_session()

print(f"Runtime Session: {session['session_id']}")

# ----------------------------------------
# DPI DYNAMIC RUNTIME
# ----------------------------------------

print("Starting Dynamic DPI Runtime...")

# ----------------------------------------
# DETECTOR PLANE
# ----------------------------------------

detector_x = np.linspace(-20, 20, 3000)

# ----------------------------------------
# SOURCE FIELD
# ----------------------------------------

source_center = 0

source_field = np.exp(
    -(detector_x - source_center)**2 / 20
)

# ----------------------------------------
# COHERENCE MODULATION
# ----------------------------------------

coherence_pattern = np.cos(detector_x * 2)

# ----------------------------------------
# PERTURBATION LAYER
# ----------------------------------------

print("Applying detector perturbation...")

noise_strength = np.random.uniform(
    0.01,
    0.15
)

noise = np.random.normal(
    0,
    noise_strength,
    detector_x.shape
)

# ----------------------------------------
# OBSERVABILITY FIELD
# ----------------------------------------

field = (
    source_field
    * coherence_pattern
)

field += noise

# ----------------------------------------
# DETECTOR INTENSITY
# ----------------------------------------

intensity = np.abs(field)**2

intensity /= np.max(intensity)

# ----------------------------------------
# EXTRACT OBSERVABLES
# ----------------------------------------

observables = extract_observables(
    detector_x,
    intensity
)

# ----------------------------------------
# ADD PERTURBATION METADATA
# ----------------------------------------

observables["noise_strength"] = (
    float(noise_strength)
)

# ----------------------------------------
# STRUCTURED TELEMETRY
# ----------------------------------------

telemetry_event = build_telemetry_event(
    observables
)

# ----------------------------------------
# PRINT OBSERVABLES
# ----------------------------------------

print("\n--- OBSERVABILITY METRICS ---")

for key, value in observables.items():

    print(f"{key}: {value}")

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

metrics_output = (
    f"{session['session_path']}/"
    "observables.json"
)

with open(metrics_output, "w") as f:

    json.dump(
        telemetry_event.model_dump(),
        f,
        indent=4
    )

append_observables(observables)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    detector_x,
    intensity,
    label="Perturbed Observability"
)

plt.title(
    "Dynamic DPI Runtime — "
    "Perturbed Detector Plane"
)

plt.xlabel("Detector Position")

plt.ylabel("Normalized Intensity")

plt.grid(True)

metrics_text = (
    f"Noise Strength: "
    f"{noise_strength:.4f}"
)

plt.text(
    0.02,
    0.95,
    metrics_text,
    transform=plt.gca().transAxes,
    verticalalignment='top',
    bbox=dict(
        facecolor='white',
        alpha=0.8
    )
)

plt.legend()

image_output = (
    f"{session['session_path']}/"
    "dynamic_runtime.png"
)

plt.savefig(image_output)

plt.close()

print(
    f"\nSaved dynamic runtime image: "
    f"{image_output}"
)

print("\nDynamic DPI Runtime Complete.")
