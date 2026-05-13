import json
import numpy as np
import matplotlib.pyplot as plt

from collections import deque

from core.telemetry.observables import (
    extract_observables
)

from core.semantic.semantic_classifier import (
    classify_semantic_state
)

from core.session.session import (
    create_runtime_session
)

# ----------------------------------------
# SESSION
# ----------------------------------------

session = create_runtime_session()

print(
    f"Semantic Runtime Session: "
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
        "memory": deque(maxlen=5)
    },
    "B": {
        "noise": 0.10,
        "memory": deque(maxlen=5)
    },
    "C": {
        "noise": 0.15,
        "memory": deque(maxlen=5)
    }
}

history = {
    "A": [],
    "B": [],
    "C": []
}

# ----------------------------------------
# SEMANTIC EVOLUTION
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

        detector["memory"].append(
            peak_count
        )

        memory_average = np.mean(
            detector["memory"]
        )

        # ----------------------------------------
        # SEMANTIC INTERPRETATION
        # ----------------------------------------

        semantic_state = (
            classify_semantic_state(
                peak_count=peak_count,
                coherence_width=observables[
                    "coherence_width"
                ],
                intensity_variance=observables[
                    "intensity_variance"
                ]
            )
        )

        # ----------------------------------------
        # SEMANTIC ADAPTATION
        # ----------------------------------------

        if semantic_state == "collapsed":

            detector["noise"] *= 1.05

        elif semantic_state == "stable":

            detector["noise"] *= 1.01

        elif semantic_state == "transitional":

            detector["noise"] *= 0.99

        elif semantic_state == "exploratory":

            detector["noise"] *= 0.94

        detector["noise"] = max(
            0.01,
            detector["noise"]
        )

        observables["semantic_state"] = (
            semantic_state
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
            f"Semantic State: "
            f"{semantic_state} | "
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
    "Semantic DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Memory-Averaged Peaks")

plt.grid(True)

plt.legend()

output_path = (
    f"{session['session_path']}/"
    "semantic_runtime.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved semantic runtime: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry_output = (
    f"{session['session_path']}/"
    "semantic_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        history,
        f,
        indent=4
    )

print(
    f"Saved semantic telemetry: "
    f"{telemetry_output}"
)

print(
    "\nSemantic DPI Runtime Complete."
)
