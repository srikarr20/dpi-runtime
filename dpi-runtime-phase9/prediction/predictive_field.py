import numpy as np


class CooperativePredictionField:

    def __init__(self):

        self.field = None

    def generate(self, federation):

        predictions = []

        for d in federation.detectors:

            predictions.append(
                d.predict()
            )

        self.field = np.mean(
            predictions,
            axis=0
        )

        self.field /= np.linalg.norm(
            self.field
        )

        return self.field
