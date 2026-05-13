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

from core.autonomous.governance import (
    determine_detector_role
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
# DETECTOR ECOSYSTEM
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

role_history = []

# ----------------------------------------
# AUTONOMOUS EVOLUTION
# ----------------------------------------

for step in range(60):

    print(f"\nStep {step}")

    # ----------------------------------------
    # GLOBAL OBSERVABILITY LOAD
    # ----------------------------------------

    global_load = np.random.uniform(
        0.8,
        1.2
    )

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
        # SEMANTIC STATE
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
        # META STATE
        # ----------------------------------------

        meta_state = (
            analyze_detector_behavior(
                detector[
                    "semantic_history"
                ]
            )
        )

        # ----------------------------------------
        # AUTONOMOUS ROLE
        # ----------------------------------------

        role = (
            determine_detector_role(
                meta_state,
                detector["noise"]
            )
        )

        # ----------------------------------------
        # ROLE-BASED ADAPTATION
        # ----------------------------------------

        if role == "stabilizer":

            detector["noise"] *= 1.01

        elif role == "explorer":

            detector["noise"] *= 0.92

        elif role == "mediator":

            detector["noise"] *= 0.97

        elif role == "generalist":

            detector["noise"] *= 1.00

        # ----------------------------------------
        # GLOBAL LOAD RESPONSE
        # ----------------------------------------

        detector["noise"] *= global_load

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

        observables["role"] = role

        observables["memory_average"] = (
            float(memory_average)
        )

        observables["noise_strength"] = (
            float(detector["noise"])
        )

        observables["global_load"] = (
            float(global_load)
        )

        observables["step"] = step

        history[detector_id].append(
            observables
        )

        role_history.append(
            {
                "detector": detector_id,
                "step": step,
                "role": role
            }
        )

        print(
            f"Detector {detector_id} | "
            f"Role: {role} | "
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
    "Autonomous DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Noise Strength")

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

telemetry = {
    "detectors": history,
    "role_history": role_history
}

telemetry_output = (
    f"{session['session_path']}/"
    "autonomous_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        telemetry,
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
