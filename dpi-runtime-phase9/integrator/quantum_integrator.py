import numpy as np

class QuantumIntegrator:

    def __init__(
        self,
        regions,
        observer
    ):

        self.regions = regions

        self.observer = observer

        self.global_field = np.zeros(16)

        self.integrator_coherence = 0.0

    # ------------------------------------------

    def integrate_fields(self):

        regional_fields = []

        for region in (
            self.regions.regions.keys()
        ):

            field = (
                self.regions.region_fields[
                    region
                ]
            )

            observer_signal = (
                self.observer.observer_fields[
                    region
                ]
            )

            integrated = (
                field * observer_signal
            )

            regional_fields.append(
                integrated
            )

        self.global_field = np.mean(
            regional_fields,
            axis=0
        )

    # ------------------------------------------

    def compute_integrator_coherence(self):

        magnitude = np.mean(
            np.abs(
                self.global_field
            )
        )

        self.integrator_coherence = (
            float(magnitude)
        )

        return (
            self.integrator_coherence
        )

    # ------------------------------------------

    def distribute_feedback(
        self,
        detectors
    ):

        for d in detectors:

            d.semantic_state = (
                0.95 * d.semantic_state
                + 0.05 * self.global_field
            )

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- QUANTUM INTEGRATOR ---\n"
        )

        print(
            f"Integrator Coherence: "
            f"{self.integrator_coherence:.4f}"
        )
