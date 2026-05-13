import numpy as np


class RecursiveConsensusEngine:

    def __init__(self, federation):

        self.federation = federation

    def stabilize(self):

        field = (
            self.federation
            .compute_collective_field()
        )

        for d in self.federation.detectors:

            delta = (
                field - d.semantic_state
            )

            d.semantic_state += 0.05 * delta

            d.semantic_state /= np.linalg.norm(
                d.semantic_state
            )
