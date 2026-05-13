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

from core.coalition.coalition_manager import (
    build_coalitions
)

from core.trust.trust_manager import (
    update_trust_score
)

from core.session.session import (
    create_runtime_session
)

# ----------------------------------------
# SESSION
# ----------------------------------------

session = create_runtime_session()

print(
    f"Cooperative Runtime Session: "
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

source_field = np.exp(
    -(detector_x)**2 / 20
)

# ----------------------------------------
# DETECTOR SOCIETY
# ----------------------------------------

detectors = {
    "A": {
        "noise": 0.05,
        "memory": deque(maxlen=5),
        "semantic_history": [],
        "trust": 0.50
    },
    "B": {
        "noise": 0.10,
        "memory": deque(maxlen=5),
        "semantic_history": [],
        "trust": 0.50
    },
    "C": {
        "noise": 0.15,
        "memory": deque(maxlen=5),
        "semantic_history": [],
        "trust": 0.50
    }
}

history = {
    "A": [],
    "B": [],
    "C": []
}

# ----------------------------------------
# EVOLUTION
# ----------------------------------------

for step in range(80):

    print(f"\nStep {step}")

    detector_states = {}

    # ----------------------------------------
    # DETECTOR EVOLUTION
    # ----------------------------------------

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

        meta_state = (
            analyze_detector_behavior(
                detector[
                    "semantic_history"
                ]
            )
        )

        role = (
            determine_detector_role(
                meta_state,
                detector["noise"]
            )
        )

        detector["trust"] = (
            update_trust_score(
                detector["trust"],
                semantic_state
            )
        )

        detector_states[detector_id] = {
            "semantic": semantic_state,
            "role": role,
            "trust": detector["trust"]
        }

        observables["semantic"] = (
            semantic_state
        )

        observables["meta"] = (
            meta_state
        )

        observables["role"] = role

        observables["trust"] = (
            detector["trust"]
        )

        observables["noise"] = (
            detector["noise"]
        )

        observables["step"] = step

        history[detector_id].append(
            observables
        )

    # ----------------------------------------
    # COALITIONS
    # ----------------------------------------

    coalitions = build_coalitions(
        detector_states
    )

    # ----------------------------------------
    # COALITION ADAPTATION
    # ----------------------------------------

    for detector_id in detectors:

        semantic = detector_states[
            detector_id
        ]["semantic"]

        role = detector_states[
            detector_id
        ]["role"]

        trust = detector_states[
            detector_id
        ]["trust"]

        detector = detectors[
            detector_id
        ]

        if semantic == "stable":

            detector["noise"] *= 1.02

        elif semantic == "transitional":

            detector["noise"] *= 0.97

        else:

            detector["noise"] *= 0.90

        # ----------------------------------------
        # TRUST STABILIZATION
        # ----------------------------------------

        if trust > 0.8:

            detector["noise"] *= 1.01

        elif trust < 0.3:

            detector["noise"] *= 0.95

        detector["noise"] = max(
            0.01,
            detector["noise"]
        )

    # ----------------------------------------
    # STATUS
    # ----------------------------------------

    print(
        f"Stable Coalition: "
        f"{coalitions['stable_cluster']}"
    )

    print(
        f"Adaptive Coalition: "
        f"{coalitions['adaptive_cluster']}"
    )

    print(
        f"Exploratory Coalition: "
        f"{coalitions['exploratory_cluster']}"
    )

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

for detector_id in history:

    trust_history = [
        h["trust"]
        for h in history[detector_id]
    ]

    plt.plot(
        trust_history,
        label=f"Detector {detector_id}"
    )

plt.title(
    "Cooperative DPI Runtime"
)

plt.xlabel("Evolution Step")

plt.ylabel("Trust Score")

plt.grid(True)

plt.legend()

output_path = (
    f"{session['session_path']}/"
    "cooperative_runtime.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved cooperative runtime: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry_output = (
    f"{session['session_path']}/"
    "cooperative_telemetry.json"
)

with open(telemetry_output, "w") as f:

    json.dump(
        history,
        f,
        indent=4
    )

print(
    f"Saved telemetry: "
    f"{telemetry_output}"
)

print(
    "\nCooperative DPI Runtime Complete."
)
