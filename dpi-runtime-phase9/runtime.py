import numpy as np
import matplotlib.pyplot as plt
import random

from core.detector import Detector

from federation.federation import Federation

from topology.topology_graph import (
    TopologyGraph
)

from topology.civilization_regions import (
    CivilizationRegions
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

for i in range(30):

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
    connectivity=0.20
)

topology.summary()

# --------------------------------------------------
# CIVILIZATION REGIONS
# --------------------------------------------------

regions = CivilizationRegions(
    detectors,
    num_regions=4
)

regions.summary()

# --------------------------------------------------
# TRACKING
# --------------------------------------------------

coherence_history = []

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for epoch in range(150):

    print(
        f"\nEpoch {epoch}"
    )

    federation.update_global_field()

    regions.update_region_fields()

    epoch_coherence = []

    # ----------------------------------------------
    # DETECTOR EVOLUTION
    # ----------------------------------------------

    for d in detectors:

        region = regions.get_region(d)

        regional_field = (
            regions.region_fields[
                region
            ]
        )

        d.update_prediction()

        d.update_semantic_state(
            regional_field
        )

        coherence = (
            d.compute_coherence(
                regional_field
            )
        )

        epoch_coherence.append(
            coherence
        )

        # ------------------------------------------
        # TOPOLOGY
        # ------------------------------------------

        neighbor_ids = topology.get_neighbors(
            d.id
        )

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

        # ------------------------------------------
        # MIGRATION
        # ------------------------------------------

        if random.random() < 0.01:

            target = random.choice(
                list(
                    regions.regions.keys()
                )
            )

            regions.migrate_detector(
                d,
                target
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
    "Civilization Region Coherence"
)

plt.xlabel("Epoch")

plt.ylabel("Coherence")

plt.grid(True)

plt.savefig(
    "dpi-runtime-phase9/telemetry/"
    "civilization_regions.png"
)

plt.close()

print(
    "\nSaved civilization regions plot."
)

print(
    "\nRecursive Civilization Runtime Complete.\n"
)
