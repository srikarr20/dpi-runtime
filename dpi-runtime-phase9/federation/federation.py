import numpy as np


class DetectorFederation:

    def __init__(self, detectors):

        self.detectors = detectors

        self.global_field = None

    def compute_collective_field(self):

        states = []

        for d in self.detectors:
            states.append(d.semantic_state)

        self.global_field = np.mean(
            states,
            axis=0
        )

        self.global_field /= np.linalg.norm(
            self.global_field
        )

        return self.global_field

    def synchronize_predictions(self):

        field = self.compute_collective_field()

        for d in self.detectors:
            d.update_prediction_field(field)

    def federation_coherence(self):

        total = 0
        count = 0

        for i in range(len(self.detectors)):
            for j in range(i + 1, len(self.detectors)):

                c = self.detectors[i].compute_coherence(
                    self.detectors[j]
                )

                total += c
                count += 1

        if count == 0:
            return 0

        return total / count
