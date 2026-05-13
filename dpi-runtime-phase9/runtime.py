import numpy as np

from core.detector import RecursiveDetector

from federation.federation import (
    DetectorFederation
)

from consensus.consensus import (
    RecursiveConsensusEngine
)

from prediction.predictive_field import (
    CooperativePredictionField
)

from trust.trust_ecology import (
    TrustEcology
)

from memory.distributed_memory import (
    DistributedSemanticMemory
)

# =====================================================
# INITIALIZE DETECTORS
# =====================================================

detectors = [
    RecursiveDetector()
    for _ in range(20)
]

# =====================================================
# FEDERATION
# =====================================================

federation = DetectorFederation(
    detectors
)

consensus = RecursiveConsensusEngine(
    federation
)

prediction_field = (
    CooperativePredictionField()
)

trust_ecology = TrustEcology(
    federation
)

memory = DistributedSemanticMemory()

# =====================================================
# RUNTIME LOOP
# =====================================================

for epoch in range(1000):

    signal = np.random.randn(128)

    for detector in detectors:

        detector.observe(signal)

        memory.store(
            detector.id,
            detector.semantic_state
        )

    federation.synchronize_predictions()

    trust_ecology.evolve()

    consensus.stabilize()

    field = prediction_field.generate(
        federation
    )

    coherence = (
        federation.federation_coherence()
    )

    print(
        f"[epoch {epoch}] "
        f"coherence={coherence:.4f}"
    )

print("")
print("===================================")
print("COLLECTIVE INTELLIGENCE STABILIZED")
print("===================================")
