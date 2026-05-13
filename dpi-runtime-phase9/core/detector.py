import numpy as np

class Detector:

    def __init__(
        self,
        detector_id
    ):

        self.id = detector_id

        self.semantic_state = (
            np.random.rand(16)
        )

        self.prediction = (
            np.random.rand(16)
        )

        self.trust_map = {}

        self.memory = []

    # ------------------------------------------

    def update_prediction(self):

        drift = np.random.normal(
            0,
            0.02,
            16
        )

        self.prediction += drift

    # ------------------------------------------

    def update_semantic_state(
        self,
        federation_field
    ):

        delta = (
            federation_field
            - self.semantic_state
        )

        self.semantic_state += (
            0.05 * delta
        )

    # ------------------------------------------

    def compute_coherence(
        self,
        federation_field
    ):

        return float(
            np.mean(
                np.abs(
                    federation_field
                    - self.semantic_state
                )
            )
        )
