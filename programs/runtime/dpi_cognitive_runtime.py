import json
import numpy as np
import matplotlib.pyplot as plt

from collections import deque

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
    f"Cognitive Runtime Session: "
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
# COGNITIVE DETECTORS
# ----------------------------------------

detectors = {
    "A": {
        "noise": 0.05,
        "role": "stabilizer",
        "memory": deque(maxlen=5)
    },
    "B": {
        "noise": 0.10,
        "role": "mediator",
        "memory": deque(maxlen=5)
    },
    "C": {
        "noise": 0.15,
        "role": "explorer",
        "memory": deque(maxlen=5)
    }
}

history = {
    "A": [],
    "B": [],
    "C": []
}

# ----------------------------------------
# COGNITIVE EVOLUTION
# ----------------------------------------

for step in range(40):

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
        # MEMORY UPDATE
        # ----------------------------------------

        detector["memory"].append(
            peak_count
        )

        memory_average = np.mean(
            detector["memory"]
        )

        # ----------------------------------------
        # COGNITIVE ADAPTATION
        # ----------------------------------------

        if memory_average < 165:

            detector["role"] = (
                "stabilizer"
            )

            detector["noise"] *= 1.01

        elif memory_average < 185:

            detector["role"] = (
                "mediator"
            )

            detector["noise"] *= 0.99

        else:

            detector["role"] = (
                "explorer"
            )

            detector["noise"] *= 0.94

        detector["noise"] = max(
            0.01,
            detector["noise"]
        )

        observables["role"] = (
            detector["role"]
        )

        observables["memory_average"] = (
            float(memory_average)
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
            f"Memory Avg: "
            f"{memory_average:.2f} | "
            f"Noise: "
            f"{detector['noise']:.4f}"
        )

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

for detector_id in history:

    memory_history = [
        h["memory_average"]
        for h in history[detector_id]
    ]

    plt.plot(
        memory_history,
        label=f"Detector {detector_id}"
    )

plt.title(
    "Cognitive DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Memory-Averaged Peaks")

plt.grid(True)

plt.legend()

output_path = (
    f"{session['session_path']}/"
    "cognitive_runtime.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved cognitive runtime: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry_output = (
    f"{session['session_path']}/"
    "cognitive_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        history,
        f,
        indent=4
    )

print(
    f"Saved cognitive telemetry: "
    f"{telemetry_output}"
)

print(
    "\nCognitive DPI Runtime Complete."
)
