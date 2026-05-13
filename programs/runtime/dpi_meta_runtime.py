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

from core.meta.meta_analyzer import (
    analyze_detector_behavior
)

from core.session.session import (
    create_runtime_session
)

# ----------------------------------------
# SESSION
# ----------------------------------------

session = create_runtime_session()

print(
    f"Meta Runtime Session: "
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
        "memory": deque(maxlen=5),
        "semantic_history": []
    },
    "B": {
        "noise": 0.10,
        "memory": deque(maxlen=5),
        "semantic_history": []
    },
    "C": {
        "noise": 0.15,
        "memory": deque(maxlen=5),
        "semantic_history": []
    }
}

history = {
    "A": [],
    "B": [],
    "C": []
}

meta_history = []

# ----------------------------------------
# META EVOLUTION
# ----------------------------------------

for step in range(50):

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

        detector[
            "semantic_history"
        ].append(semantic_state)

        # ----------------------------------------
        # META-ANALYSIS
        # ----------------------------------------

        meta_state = (
            analyze_detector_behavior(
                detector[
                    "semantic_history"
                ]
            )
        )

        # ----------------------------------------
        # META ADAPTATION
        # ----------------------------------------

        if meta_state == "volatile":

            detector["noise"] *= 0.92

        elif meta_state == "stabilized":

            detector["noise"] *= 1.01

        elif meta_state == "adaptive":

            detector["noise"] *= 0.98

        elif meta_state == "degraded":

            detector["noise"] *= 1.05

        detector["noise"] = max(
            0.01,
            detector["noise"]
        )

        observables["semantic_state"] = (
            semantic_state
        )

        observables["meta_state"] = (
            meta_state
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

        meta_history.append(
            {
                "detector": detector_id,
                "step": step,
                "meta_state": meta_state
            }
        )

        print(
            f"Detector {detector_id} | "
            f"Semantic: {semantic_state} | "
            f"Meta: {meta_state} | "
            f"Noise: "
            f"{detector['noise']:.4f}"
        )

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

for detector_id in history:

    noise_history = [
        h["noise_strength"]
        for h in history[detector_id]
    ]

    plt.plot(
        noise_history,
        label=f"Detector {detector_id}"
    )

plt.title(
    "Meta DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Noise Strength")

plt.grid(True)

plt.legend()

output_path = (
    f"{session['session_path']}/"
    "meta_runtime.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved meta runtime: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry = {
    "detectors": history,
    "meta_history": meta_history
}

telemetry_output = (
    f"{session['session_path']}/"
    "meta_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        telemetry,
        f,
        indent=4
    )

print(
    f"Saved meta telemetry: "
    f"{telemetry_output}"
)

print(
    "\nMeta DPI Runtime Complete."
)
