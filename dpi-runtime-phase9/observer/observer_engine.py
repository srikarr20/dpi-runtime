import numpy as np

class ObserverEngine:

    def __init__(
        self,
        governance,
        metagovernance
    ):

        self.governance = governance

        self.metagovernance = metagovernance

        self.observer_fields = {}

        self.initialize_observers()

    # ------------------------------------------

    def initialize_observers(self):

        for region in (
            self.governance.regions.regions.keys()
        ):

            self.observer_fields[
                region
            ] = 0.5

    # ------------------------------------------

    def observe_systems(self):

        for region in (
            self.governance.regions.regions.keys()
        ):

            governance = (
                self.governance.stability[
                    region
                ]
            )

            meta = (
                self.metagovernance
                .meta_stability[
                    region
                ]
            )

            observer_signal = (
                0.5 * governance
                + 0.5 * meta
            )

            self.observer_fields[
                region
            ] = observer_signal

    # ------------------------------------------

    def recursive_feedback(self):

        for region in (
            self.governance.regions.regions.keys()
        ):

            signal = (
                self.observer_fields[
                    region
                ]
            )

            policies = (
                self.governance.policies[
                    region
                ]
            )

            adjustment = (
                signal - 0.5
            ) * 0.01

            for key in policies:

                policies[key] += adjustment

                policies[key] = max(
                    0.0,
                    min(
                        1.0,
                        policies[key]
                    )
                )

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- OBSERVER FIELDS ---\n"
        )

        for region, signal in (
            self.observer_fields.items()
        ):

            print(
                f"{region}: "
                f"{signal:.3f}"
            )
