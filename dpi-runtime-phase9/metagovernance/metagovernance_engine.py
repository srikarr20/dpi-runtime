import numpy as np

class MetaGovernanceEngine:

    def __init__(
        self,
        governance,
        constitution
    ):

        self.governance = governance

        self.constitution = constitution

        self.meta_stability = {}

        self.initialize_meta()

    # ------------------------------------------

    def initialize_meta(self):

        for region in (
            self.governance.regions.regions.keys()
        ):

            self.meta_stability[
                region
            ] = 0.5

    # ------------------------------------------

    def evaluate_systems(self):

        for region in (
            self.governance.regions.regions.keys()
        ):

            governance_stability = (
                self.governance.stability[
                    region
                ]
            )

            constitutional_history = (
                self.constitution
                .constitution_history[
                    region
                ]
            )

            drift = 0.0

            if len(constitutional_history) > 1:

                latest = constitutional_history[-1]

                previous = constitutional_history[-2]

                latest_values = np.array(
                    list(latest.values())
                )

                previous_values = np.array(
                    list(previous.values())
                )

                drift = float(
                    np.mean(
                        np.abs(
                            latest_values
                            - previous_values
                        )
                    )
                )

            stability = (
                governance_stability
                * (1.0 - drift)
            )

            self.meta_stability[
                region
            ] = stability

    # ------------------------------------------

    def regulate_constitutions(self):

        for region in (
            self.governance.regions.regions.keys()
        ):

            stability = (
                self.meta_stability[
                    region
                ]
            )

            if stability < 0.60:

                policies = (
                    self.governance.policies[
                        region
                    ]
                )

                for key in policies:

                    policies[key] *= 0.99

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- META GOVERNANCE ---\n"
        )

        for region, stability in (
            self.meta_stability.items()
        ):

            print(
                f"{region}: "
                f"{stability:.3f}"
            )
