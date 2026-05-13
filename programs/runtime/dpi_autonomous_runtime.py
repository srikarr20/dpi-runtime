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
    f"Autonomous Runtime Session: "
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
# SOURCE FIELD
# ----------------------------------------

source_field = np.exp(
    -(detector_x)**2 / 20
)

# ----------------------------------------
# DETECTOR NETWORK
# ----------------------------------------

detectors = {
    "A": {
        "noise": 0.05,
        "role": "stabilizer"
    },
    "B": {
        "noise": 0.10,
        "role": "mediator"
    },
    "C": {
        "noise": 0.15,
        "role": "explorer"
    }
}

history = {
    "A": [],
    "B": [],
    "C": []
}

# ----------------------------------------
# AUTONOMOUS EVOLUTION
# ----------------------------------------

for step in range(30):

    print(f"\nStep {step}")

    for detector_id in detectors:

        detector = detectors[detector_id]

        noise_strength = detector["noise"]

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

        peak_count = observables[
            "peak_count"
        ]

        # ----------------------------------------
        # AUTONOMOUS ROLE SPECIALIZATION
        # ----------------------------------------

        if peak_count < 165:

            detector["role"] = (
                "stabilizer"
            )

            detector["noise"] *= 1.01

        elif peak_count < 185:

            detector["role"] = (
                "mediator"
            )

            detector["noise"] *= 0.99

        else:

            detector["role"] = (
                "explorer"
            )

            detector["noise"] *= 0.95

        detector["noise"] = max(
            0.01,
            detector["noise"]
        )

        observables["role"] = (
            detector["role"]
        )

        observables["noise_strength"] = (
            float(detector["noise"])
        )

        observables["step"] = step

        history[detector_id].append(
            observables
        )

        print(
            f"Detector {detector_id} | "
            f"Role: {detector['role']} | "
            f"Noise: "
            f"{detector['noise']:.4f} | "
            f"Peaks: {peak_count}"
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

plt.title(
    "Autonomous DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Peak Count")

plt.grid(True)

plt.legend()

output_path = (
    f"{session['session_path']}/"
    "autonomous_runtime.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved autonomous runtime: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry_output = (
    f"{session['session_path']}/"
    "autonomous_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        history,
        f,
        indent=4
    )

print(
    f"Saved autonomous telemetry: "
    f"{telemetry_output}"
)

print(
    "\nAutonomous DPI Runtime Complete."
)
