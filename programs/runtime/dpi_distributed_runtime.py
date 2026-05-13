import json
import numpy as np
import matplotlib.pyplot as plt

from core.telemetry.observables import (
    extract_observables
)

from core.session.session import (
    create_runtime_session
)

# ----------------------------------------
# SESSION
# ----------------------------------------

session = create_runtime_session()

print(
    f"Distributed Runtime Session: "
    f"{session['session_id']}"
)

# ----------------------------------------
# DETECTOR PLANES
# ----------------------------------------

detector_x = np.linspace(
    -20,
    20,
    3000
)

# ----------------------------------------
# SHARED SOURCE FIELD
# ----------------------------------------

source_field = np.exp(
    -(detector_x)**2 / 20
)

# ----------------------------------------
# DETECTOR NETWORK
# ----------------------------------------

detectors = {
    "A": 0.05,
    "B": 0.10,
    "C": 0.15
}

history = {
    "A": [],
    "B": [],
    "C": []
}

# ----------------------------------------
# DISTRIBUTED EVOLUTION
# ----------------------------------------

for step in range(20):

    print(f"\nStep {step}")

    peak_counts = {}

    for detector_id in detectors:

        noise_strength = (
            detectors[detector_id]
        )

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

        observables = (
            extract_observables(
                detector_x,
                intensity
            )
        )

        observables["noise_strength"] = (
            float(noise_strength)
        )

        observables["step"] = step

        history[detector_id].append(
            observables
        )

        peak_counts[detector_id] = (
            observables["peak_count"]
        )

        print(
            f"Detector {detector_id} | "
            f"Noise: {noise_strength:.4f} | "
            f"Peaks: "
            f"{observables['peak_count']}"
        )

    # ----------------------------------------
    # DISTRIBUTED CONSENSUS
    # ----------------------------------------

    average_peaks = np.mean(
        list(peak_counts.values())
    )

    for detector_id in detectors:

        if average_peaks > 180:

            detectors[detector_id] *= 0.92

        else:

            detectors[detector_id] *= 1.02

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

for detector_id in history:

    peak_history = [
        h["peak_count"]
        for h in history[detector_id]
    ]

    plt.plot(
        peak_history,
        label=f"Detector {detector_id}"
    )

plt.title(
    "Distributed DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Peak Count")

plt.grid(True)

plt.legend()

output_path = (
    f"{session['session_path']}/"
    "distributed_runtime.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved distributed runtime: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry_output = (
    f"{session['session_path']}/"
    "distributed_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        history,
        f,
        indent=4
    )

print(
    f"Saved distributed telemetry: "
    f"{telemetry_output}"
)

print(
    "\nDistributed DPI Runtime Complete."
)
