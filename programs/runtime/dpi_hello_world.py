import json
import numpy as np
import matplotlib.pyplot as plt

from core.telemetry.observables import extract_observables
from core.telemetry.schema import build_telemetry_event
from core.trajectory.trajectory import append_observables

# ----------------------------------------
# DPI HELLO WORLD
# ----------------------------------------

print("Starting DPI Hello World Runtime...")

# ----------------------------------------
# DETECTOR PLANE
# ----------------------------------------

print("Creating detector plane...")

detector_x = np.linspace(-20, 20, 3000)

# ----------------------------------------
# SOURCE FIELD
# ----------------------------------------

print("Generating source field...")

source_center = 0

source_field = np.exp(-(detector_x - source_center)**2 / 20)

# ----------------------------------------
# COHERENCE MODULATION
# ----------------------------------------

print("Applying coherence modulation...")

coherence_pattern = np.cos(detector_x * 2)

# ----------------------------------------
# OBSERVABILITY FIELD
# ----------------------------------------

print("Constructing observability field...")

field = source_field * coherence_pattern

# ----------------------------------------
# DETECTOR INTENSITY
# ----------------------------------------

print("Computing detector intensity...")

intensity = np.abs(field)**2

intensity /= np.max(intensity)

# ----------------------------------------
# EXTRACT OBSERVABLES
# ----------------------------------------

print("Extracting observability metrics...")

observables = extract_observables(
    detector_x,
    intensity
)

# ----------------------------------------
# BUILD STRUCTURED TELEMETRY
# ----------------------------------------

telemetry_event = build_telemetry_event(observables)

# ----------------------------------------
# PRINT OBSERVABLES
# ----------------------------------------

print("\n--- OBSERVABILITY METRICS ---")

for key, value in observables.items():
    print(f"{key}: {value}")

# ----------------------------------------
# SAVE OBSERVABLES
# ----------------------------------------

metrics_output = "outputs/telemetry/observables.json"

with open(metrics_output, "w") as f:

    json.dump(
        telemetry_event.model_dump(),
        f,
        indent=4
    )

print(f"\nSaved observability metrics: {metrics_output}")

# ----------------------------------------
# UPDATE TRAJECTORY HISTORY
# ----------------------------------------

append_observables(observables)

# ----------------------------------------
# SAVE NUMERICAL OUTPUT
# ----------------------------------------

np.save(
    "outputs/raw/raw_detector_observability.npy",
    intensity
)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    detector_x,
    intensity,
    label="Detector Observability"
)

plt.title("DPI Hello World — Detector Plane Observability")

plt.xlabel("Detector Position")

plt.ylabel("Normalized Observability Intensity")

plt.grid(True)

# ----------------------------------------
# OVERLAY METRICS
# ----------------------------------------

metrics_text = (
    f"Peak Intensity: {observables['peak_intensity']:.2f}\n"
    f"Mean Intensity: {observables['mean_intensity']:.4f}\n"
    f"Coherence Width: {observables['coherence_width']:.2f}\n"
    f"Peak Count: {observables['peak_count']}"
)

plt.text(
    0.02,
    0.95,
    metrics_text,
    transform=plt.gca().transAxes,
    verticalalignment='top',
    bbox=dict(facecolor='white', alpha=0.8)
)

plt.legend()

# ----------------------------------------
# SAVE IMAGE
# ----------------------------------------

output_image = "outputs/images/dpi_hello_world.png"

plt.savefig(output_image)

print(f"Saved detector-plane image: {output_image}")

plt.close()

print("\nDPI Hello World Runtime Complete.")
