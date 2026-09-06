class TrustEcology:

    def __init__(self, federation):

        self.federation = federation

    def evolve(self):

        detectors = (
            self.federation.detectors
        )

        for i in range(len(detectors)):
            for j in range(i + 1, len(detectors)):

                c = detectors[i].compute_coherence(
                    detectors[j]
                )

                detectors[i].trust_update(
                    detectors[j].id,
                    c
                )

                detectors[j].trust_update(
                    detectors[i].id,
                    c
                )
