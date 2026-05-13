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
    f"Hierarchical Runtime Session: "
    f"{session['session_id']}"
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

supervisor_history = []

# ----------------------------------------
# HIERARCHICAL EVOLUTION
# ----------------------------------------

for step in range(25):

    print(f"\nStep {step}")

    peak_counts = {}

    coherence_widths = {}

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

        coherence_widths[detector_id] = (
            observables["coherence_width"]
        )

        print(
            f"Detector {detector_id} | "
            f"Noise: {noise_strength:.4f} | "
            f"Peaks: "
            f"{observables['peak_count']}"
        )

    # ----------------------------------------
    # SUPERVISOR LAYER
    # ----------------------------------------

    global_peak_average = np.mean(
        list(peak_counts.values())
    )

    global_width_average = np.mean(
        list(coherence_widths.values())
    )

    supervisor_state = {
        "step": step,
        "global_peak_average": (
            float(global_peak_average)
        ),
        "global_width_average": (
            float(global_width_average)
        )
    }

    supervisor_history.append(
        supervisor_state
    )

    print(
        f"Supervisor | "
        f"Avg Peaks: "
        f"{global_peak_average:.2f}"
    )

    # ----------------------------------------
    # HIERARCHICAL CONTROL
    # ----------------------------------------

    if global_peak_average > 185:

        control_factor = 0.90

    elif global_peak_average < 165:

        control_factor = 1.04

    else:

        control_factor = 0.98

    for detector_id in detectors:

        detectors[detector_id] *= (
            control_factor
        )

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

supervisor_peaks = [
    s["global_peak_average"]
    for s in supervisor_history
]

plt.plot(
    supervisor_peaks,
    linewidth=4,
    linestyle='--',
    label="Supervisor"
)

plt.title(
    "Hierarchical DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Peak Count")

plt.grid(True)

plt.legend()

output_path = (
    f"{session['session_path']}/"
    "hierarchical_runtime.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved hierarchical runtime: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry = {
    "detectors": history,
    "supervisor": supervisor_history
}

telemetry_output = (
    f"{session['session_path']}/"
    "hierarchical_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        telemetry,
        f,
        indent=4
    )

print(
    f"Saved hierarchical telemetry: "
    f"{telemetry_output}"
)

print(
    "\nHierarchical DPI Runtime Complete."
)
