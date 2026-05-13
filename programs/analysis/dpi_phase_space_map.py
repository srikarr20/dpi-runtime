import json
import numpy as np
import matplotlib.pyplot as plt

from core.telemetry.observables import (
    extract_observables
)

# ----------------------------------------
# DETECTOR PLANE
# ----------------------------------------

detector_x = np.linspace(
    -20,
    20,
    3000
)

# ----------------------------------------
# SOURCE FIELD
# ----------------------------------------

source_center = 0

source_field = np.exp(
    -(detector_x - source_center)**2 / 20
)

# ----------------------------------------
# SWEEP PARAMETERS
# ----------------------------------------

noise_levels = np.linspace(
    0.0,
    0.20,
    50
)

# ----------------------------------------
# OBSERVABILITY TRACKING
# ----------------------------------------

coherence_widths = []

peak_counts = []

variance_values = []

# ----------------------------------------
# PHASE SWEEP
# ----------------------------------------

for noise_strength in noise_levels:

    coherence_pattern = np.cos(
        detector_x * 2
    )

    noise = np.random.normal(
        0,
        noise_strength,
        detector_x.shape
    )

    field = (
        source_field
        * coherence_pattern
    )

    field += noise

    intensity = np.abs(field)**2

    intensity /= np.max(intensity)

    observables = extract_observables(
        detector_x,
        intensity
    )

    coherence_widths.append(
        observables["coherence_width"]
    )

    peak_counts.append(
        observables["peak_count"]
    )

    variance_values.append(
        observables["intensity_variance"]
    )

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

plt.plot(
    noise_levels,
    coherence_widths,
    label="Coherence Width"
)

plt.plot(
    noise_levels,
    peak_counts,
    label="Peak Count"
)

plt.plot(
    noise_levels,
    variance_values,
    label="Intensity Variance"
)

plt.title(
    "DPI Coherence Phase-Space Map"
)

plt.xlabel("Noise Strength")

plt.ylabel("Observability Metric")

plt.grid(True)

plt.legend()

output_path = (
    "outputs/images/"
    "phase_space_map.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"Saved phase-space map: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE PHASE DATA
# ----------------------------------------

phase_data = {
    "noise_levels": noise_levels.tolist(),
    "coherence_widths": coherence_widths,
    "peak_counts": peak_counts,
    "variance_values": variance_values
}

phase_output = (
    "outputs/telemetry/"
    "phase_space_map.json"
)

with open(phase_output, "w") as f:

    json.dump(
        phase_data,
        f,
        indent=4
    )

print(
    f"Saved phase-space telemetry: "
    f"{phase_output}"
)
