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

from diplomacy.diplomacy_engine import (
    DiplomacyEngine
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
# REGIONS
# --------------------------------------------------

regions = CivilizationRegions(
    detectors,
    num_regions=4
)

regions.summary()

# --------------------------------------------------
# DIPLOMACY
# --------------------------------------------------

diplomacy = DiplomacyEngine(
    regions
)

# --------------------------------------------------
# TRACKING
# --------------------------------------------------

coherence_history = []

alliance_history = []

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for epoch in range(200):

    print(
        f"\nEpoch {epoch}"
    )

    federation.update_global_field()

    regions.update_region_fields()

    diplomacy.update_relations()

    epoch_coherence = []

    alliance_scores = []

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

    # ----------------------------------------------
    # DIPLOMATIC ALLIANCES
    # ----------------------------------------------

    for region, relations in (
        diplomacy.alliances.items()
    ):

        for other, score in (
            relations.items()
        ):

            alliance_scores.append(score)

    avg_alliance = float(
        np.mean(alliance_scores)
    )

    alliance_history.append(
        avg_alliance
    )

    print(
        f"Federation Coherence: "
        f"{coherence:.4f}"
    )

    print(
        f"Alliance Stability: "
        f"{avg_alliance:.4f}"
    )

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    coherence_history,
    label="Coherence"
)

plt.plot(
    alliance_history,
    label="Alliance Stability"
)

plt.title(
    "Civilization Diplomacy Dynamics"
)

plt.xlabel("Epoch")

plt.ylabel("Metric")

plt.grid(True)

plt.legend()

plt.savefig(
    "dpi-runtime-phase9/telemetry/"
    "civilization_diplomacy.png"
)

plt.close()

print(
    "\nSaved diplomacy plot."
)

print(
    "\nRecursive Civilization Runtime Complete.\n"
)
