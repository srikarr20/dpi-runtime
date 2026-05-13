import json
import random

import numpy as np
import matplotlib.pyplot as plt

from core.telemetry.observables import (
    extract_observables
)

from core.semantic.semantic_classifier import (
    classify_semantic_state
)

from core.trust.trust_manager import (
    update_trust_score
)

from core.session.session import (
    create_runtime_session
)

from core.predictive.predictor import (
    predict_future_state
)

# ----------------------------------------
# SESSION
# ----------------------------------------

session = create_runtime_session()

print(
    f"Evolutionary Runtime Session: "
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
# ECOLOGY SETTINGS
# ----------------------------------------

MAX_POPULATION = 250

# ----------------------------------------
# EVOLUTION UTILITIES
# ----------------------------------------

def reproduce_detector(parent):

    child = {
        "noise": parent["noise"],
        "trust": parent["trust"],
        "generation": parent[
            "generation"
        ] + 1,
        "age": 0,
        "cooldown": 10,
        "energy": 1.0
    }

    # ----------------------------------------
    # MUTATION
    # ----------------------------------------

    mutation = random.uniform(
        -0.01,
        0.01
    )

    child["noise"] += mutation

    child["noise"] = max(
        0.01,
        child["noise"]
    )

    return child

# ----------------------------------------
# INITIAL CIVILIZATION
# ----------------------------------------

detectors = {
    "A": {
        "noise": 0.05,
        "trust": 0.5,
        "generation": 0,
        "age": 0,
        "cooldown": 0,
        "energy": 1.0
    },
    "B": {
        "noise": 0.10,
        "trust": 0.5,
        "generation": 0,
        "age": 0,
        "cooldown": 0,
        "energy": 1.0
    },
    "C": {
        "noise": 0.15,
        "trust": 0.5,
        "generation": 0,
        "age": 0,
        "cooldown": 0,
        "energy": 1.0
    }
}

history = []

population_sizes = []

next_id = 0

# ----------------------------------------
# EVOLUTION LOOP
# ----------------------------------------

for step in range(200):

    print(f"\nStep {step}")

    current_ids = list(
        detectors.keys()
    )

    for detector_id in current_ids:

        if detector_id not in detectors:

            continue

        detector = detectors[
            detector_id
        ]

        noise_strength = detector[
            "noise"
        ]

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

        semantic_state = (
            classify_semantic_state(
                peak_count=observables[
                    "peak_count"
                ],
                coherence_width=observables[
                    "coherence_width"
                ],
                intensity_variance=observables[
                    "intensity_variance"
                ]
            )
        )

        # ----------------------------------------
        # FUTURE PREDICTION
        # ----------------------------------------

        future_state = (
            predict_future_state(
                detector
            )
        )

        # ----------------------------------------
        # TRUST UPDATE
        # ----------------------------------------

        detector["trust"] = (
            update_trust_score(
                detector["trust"],
                semantic_state
            )
        )

        # ----------------------------------------
        # ECOLOGICAL DYNAMICS
        # ----------------------------------------

        detector["age"] += 1

        detector["energy"] -= 0.01

        detector["cooldown"] -= 1

        # entropy drift

        detector["trust"] *= 0.995

        # ----------------------------------------
        # PREDICTIVE ADAPTATION
        # ----------------------------------------

        if future_state == "collapse":

            detector["noise"] *= 0.95

            detector["energy"] += 0.02

        elif future_state == "fragile":

            detector["noise"] *= 0.98

        elif future_state == "dominant":

            detector["energy"] += 0.01

        # ----------------------------------------
        # REPRODUCTION
        # ----------------------------------------

        if (
            detector["trust"] > 0.90
            and detector["cooldown"] <= 0
            and detector["energy"] > 0.6
            and len(detectors) < MAX_POPULATION
        ):

            child = reproduce_detector(
                detector
            )

            child_id = (
                f"D{next_id}"
            )

            next_id += 1

            detectors[
                child_id
            ] = child

            detector["energy"] -= 0.25

            detector["cooldown"] = 10

            print(
                f"{detector_id} "
                f"spawned {child_id}"
            )

        # ----------------------------------------
        # ECOLOGICAL EXTINCTION
        # ----------------------------------------

        remove = False

        if detector["trust"] < 0.20:

            remove = True

        if detector["noise"] > 0.25:

            remove = True

        if detector["age"] > 80:

            remove = True

        if detector["energy"] <= 0:

            remove = True

        if remove:

            print(
                f"{detector_id} extinct"
            )

            del detectors[
                detector_id
            ]

            continue

        # ----------------------------------------
        # HISTORY
        # ----------------------------------------

        history.append(
            {
                "step": step,
                "detector": detector_id,
                "trust": detector[
                    "trust"
                ],
                "noise": detector[
                    "noise"
                ],
                "generation": detector[
                    "generation"
                ],
                "age": detector[
                    "age"
                ],
                "energy": detector[
                    "energy"
                ],
                "semantic": semantic_state,
                "future_state": future_state
            }
        )

        print(
            f"{detector_id} | "
            f"Trust: "
            f"{detector['trust']:.2f} | "
            f"Noise: "
            f"{detector['noise']:.3f} | "
            f"Gen: "
            f"{detector['generation']} | "
            f"Age: "
            f"{detector['age']} | "
            f"Energy: "
            f"{detector['energy']:.2f} | "
            f"Future: "
            f"{future_state}"
        )

    population_sizes.append(
        len(detectors)
    )

    print(
        f"Population Size: "
        f"{len(detectors)}"
    )

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

plt.plot(
    population_sizes
)

plt.title(
    "Recursive Predictive DPI Ecology"
)

plt.xlabel("Evolution Step")

plt.ylabel("Population Size")

plt.grid(True)

output_path = (
    f"{session['session_path']}/"
    "predictive_ecology.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"\nSaved predictive ecology: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE TELEMETRY
# ----------------------------------------

telemetry_output = (
    f"{session['session_path']}/"
    "predictive_telemetry.json"
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
    "\nRecursive Predictive DPI Runtime Complete."
)
