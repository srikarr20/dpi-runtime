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

from governance.governance_engine import (
    GovernanceEngine
)

from inheritance.inheritance_engine import (
    InheritanceEngine
)

from constitution.constitutional_engine import (
    ConstitutionalEngine
)

from metagovernance.metagovernance_engine import (
    MetaGovernanceEngine
)

from observer.observer_engine import (
    ObserverEngine
)

from integrator.quantum_integrator import (
    QuantumIntegrator
)

# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

print(
    "\nQuantum Integrator Runtime Initializing...\n"
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

# --------------------------------------------------
# REGIONS
# --------------------------------------------------

regions = CivilizationRegions(
    detectors,
    num_regions=4
)

# --------------------------------------------------
# DIPLOMACY
# --------------------------------------------------

diplomacy = DiplomacyEngine(
    regions
)

# --------------------------------------------------
# GOVERNANCE
# --------------------------------------------------

governance = GovernanceEngine(
    regions
)

# --------------------------------------------------
# INHERITANCE
# --------------------------------------------------

inheritance = InheritanceEngine(
    regions
)

# --------------------------------------------------
# CONSTITUTION
# --------------------------------------------------

constitution = ConstitutionalEngine(
    governance
)

# --------------------------------------------------
# META GOVERNANCE
# --------------------------------------------------

metagovernance = MetaGovernanceEngine(
    governance,
    constitution
)

# --------------------------------------------------
# OBSERVER ENGINE
# --------------------------------------------------

observer = ObserverEngine(
    governance,
    metagovernance
)

# --------------------------------------------------
# QUANTUM INTEGRATOR
# --------------------------------------------------

integrator = QuantumIntegrator(
    regions,
    observer
)

# --------------------------------------------------
# TRACKING
# --------------------------------------------------

coherence_history = []
observer_history = []
integrator_history = []

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for epoch in range(700):

    print(f"\nEpoch {epoch}")

    federation.update_global_field()

    regions.update_region_fields()

    diplomacy.update_relations()

    governance.update_governance()

    inheritance.archive_epoch()

    constitution.evolve_constitutions()

    metagovernance.evaluate_systems()

    metagovernance.regulate_constitutions()

    observer.observe_systems()

    observer.recursive_feedback()

    integrator.integrate_fields()

    integrator.distribute_feedback(
        detectors
    )

    integrator_coherence = (
        integrator
        .compute_integrator_coherence()
    )

    epoch_coherence = []

    observer_scores = []

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

        heritage_field = (
            inheritance.retrieve_heritage(
                region
            )
        )

        combined_field = (
            0.7 * regional_field
            + 0.3 * heritage_field
        )

        d.update_prediction()

        d.update_semantic_state(
            combined_field
        )

        coherence = (
            d.compute_coherence(
                combined_field
            )
        )

        epoch_coherence.append(
            coherence
        )

        # ------------------------------------------
        # TRUST TOPOLOGY
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

        d.memory.append(
            d.semantic_state.tolist()
        )

        policy = governance.policies[
            region
        ]

        migration_rate = (
            1.0
            - policy[
                "migration_control"
            ]
        ) * 0.02

        if random.random() < migration_rate:

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
    # AGGREGATE METRICS
    # ----------------------------------------------

    coherence_history.append(
        float(
            np.mean(epoch_coherence)
        )
    )

    observer_scores = list(
        observer.observer_fields.values()
    )

    observer_history.append(
        float(
            np.mean(observer_scores)
        )
    )

    integrator_history.append(
        integrator_coherence
    )

    # ----------------------------------------------
    # LOGGING
    # ----------------------------------------------

    print(
        f"Coherence: "
        f"{coherence_history[-1]:.4f}"
    )

    print(
        f"Observer Stability: "
        f"{observer_history[-1]:.4f}"
    )

    print(
        f"Integrator Coherence: "
        f"{integrator_coherence:.4f}"
    )

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(14, 7))

plt.plot(
    coherence_history,
    label="Detector Coherence"
)

plt.plot(
    observer_history,
    label="Observer Stability"
)

plt.plot(
    integrator_history,
    label="Integrator Coherence"
)

plt.title(
    "Quantum Integrator Runtime"
)

plt.xlabel("Epoch")

plt.ylabel("Metric")

plt.grid(True)

plt.legend()

plt.savefig(
    "dpi-runtime-phase9/telemetry/"
    "quantum_integrator.png"
)

plt.close()

print(
    "\nSaved quantum integrator plot."
)

print(
    "\nQuantum Integrator Runtime Complete.\n"
)
