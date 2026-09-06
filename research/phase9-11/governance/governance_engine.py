import numpy as np

class GovernanceEngine:

    def __init__(
        self,
        regions
    ):

        self.regions = regions

        self.policies = {}

        self.stability = {}

        self.initialize_governance()

    # ------------------------------------------

    def initialize_governance(self):

        for region in (
            self.regions.regions.keys()
        ):

            self.policies[region] = {
                "migration_control": 0.5,
                "trust_regulation": 0.5,
                "coherence_target": 0.8
            }

            self.stability[region] = 0.5

    # ------------------------------------------

    def update_governance(self):

        for region in (
            self.regions.regions.keys()
        ):

            field = (
                self.regions.region_fields[
                    region
                ]
            )

            coherence = float(
                np.mean(
                    np.abs(field)
                )
            )

            target = (
                self.policies[region][
                    "coherence_target"
                ]
            )

            error = abs(
                target - coherence
            )

            stability = max(
                0.0,
                1.0 - error
            )

            self.stability[
                region
            ] = stability

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- GOVERNANCE STATUS ---\n"
        )

        for region, stability in (
            self.stability.items()
        ):

            print(
                f"{region}: "
                f"{stability:.3f}"
            )
