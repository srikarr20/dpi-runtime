import numpy as np

class Federation:

    def __init__(
        self,
        detectors
    ):

        self.detectors = detectors

        self.global_field = (
            np.zeros(16)
        )

    # ------------------------------------------

    def update_global_field(self):

        states = []

        for detector in self.detectors:

            states.append(
                detector.semantic_state
            )

        self.global_field = np.mean(
            states,
            axis=0
        )
