import numpy as np
import matplotlib.pyplot as plt

from core.detector import Detector

from federation.federation import Federation

from topology.topology_graph import (
    TopologyGraph
)

# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

print(
    "\nRecursive Civilization Runtime Initializing...\n"
)

# --------------------------------------------------
# DETECTORS
# --------------------------------------------------

detectors = []

for i in range(25):

    detectors.append(
        Detector(
            detector_id=f"D{i}"
        )
    )

# --------------------------------------------------
# FEDERATION
# --------------------------------------------------

federation = Federation(
    detectors
)

# --------------------------------------------------
# TOPOLOGY
# --------------------------------------------------

topology = TopologyGraph(
    detectors,
    connectivity=0.25
)

topology.summary()

# --------------------------------------------------
# TRACKING
# --------------------------------------------------

coherence_history = []

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for epoch in range(100):

    print(
        f"\nEpoch {epoch}"
    )

    federation.update_global_field()

    field = federation.global_field

    epoch_coherence = []

    # ----------------------------------------------
    # DETECTOR EVOLUTION
    # ----------------------------------------------

    for d in detectors:

        d.update_prediction()

        d.update_semantic_state(
            field
        )

        coherence = (
            d.compute_coherence(
                field
            )
        )

        epoch_coherence.append(
            coherence
        )

        # ------------------------------------------
        # TOPOLOGY NEIGHBORS
        # ------------------------------------------

        neighbor_ids = topology.get_neighbors(
            d.id
        )

        # ------------------------------------------
        # TRUST DYNAMICS
        # ------------------------------------------

        for other in detectors:

            if other.id not in neighbor_ids:

                continue

            similarity = float(
                np.mean(
                    np.abs(
                        d.semantic_state
                        - other.semantic_state
                    )
                )
            )

            trust = max(
                0.0,
                1.0 - similarity
            )

            d.trust_map[
                other.id
            ] = trust

        # ------------------------------------------
        # MEMORY
        # ------------------------------------------

        d.memory.append(
            d.semantic_state.tolist()
        )

    # ----------------------------------------------
    # COHERENCE
    # ----------------------------------------------

    coherence = float(
        np.mean(epoch_coherence)
    )

    coherence_history.append(
        coherence
    )

    print(
        f"Federation Coherence: "
        f"{coherence:.4f}"
    )

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    coherence_history
)

plt.title(
    "Civilization Coherence Evolution"
)

plt.xlabel("Epoch")

plt.ylabel("Coherence")

plt.grid(True)

plt.savefig(
    "dpi-runtime-phase9/telemetry/"
    "civilization_coherence.png"
)

plt.close()

print(
    "\nSaved civilization coherence plot:"
)

print(
    "dpi-runtime-phase9/telemetry/"
    "civilization_coherence.png"
)

print(
    "\nRecursive Civilization Runtime Complete.\n"
)
