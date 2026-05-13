import uuid
import numpy as np


class RecursiveDetector:

    def __init__(self, semantic_dim=128):

        self.id = str(uuid.uuid4())

        self.semantic_state = np.random.randn(semantic_dim)

        self.semantic_state /= np.linalg.norm(
            self.semantic_state
        )

        self.trust_map = {}

        self.memory = []

        self.prediction_field = np.zeros(semantic_dim)

        self.coherence = 1.0

    def observe(self, signal):

        imprint = signal + np.random.normal(
            0,
            0.01,
            len(signal)
        )

        self.semantic_state += imprint

        self.semantic_state /= np.linalg.norm(
            self.semantic_state
        )

        self.memory.append(imprint.tolist())

        return imprint

    def predict(self):

        prediction = (
            self.semantic_state
            + self.prediction_field
        )

        prediction /= np.linalg.norm(prediction)

        return prediction

    def update_prediction_field(
        self,
        federation_field
    ):

        self.prediction_field = (
            0.8 * self.prediction_field
            + 0.2 * federation_field
        )

    def compute_coherence(self, other):

        return float(
            np.dot(
                self.semantic_state,
                other.semantic_state
            )
        )

    def trust_update(
        self,
        other_id,
        coherence
    ):

        if other_id not in self.trust_map:
            self.trust_map[other_id] = 0.5

        self.trust_map[other_id] += (
            0.01 * coherence
        )

        self.trust_map[other_id] = np.clip(
            self.trust_map[other_id],
            0.0,
            1.0
        )
