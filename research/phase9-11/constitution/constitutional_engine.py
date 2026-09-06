import random
import copy

class ConstitutionalEngine:

    def __init__(
        self,
        governance
    ):

        self.governance = governance

        self.constitution_history = {}

        self.initialize_history()

    # ------------------------------------------

    def initialize_history(self):

        for region in (
            self.governance.regions.regions.keys()
        ):

            self.constitution_history[
                region
            ] = []

    # ------------------------------------------

    def evolve_constitutions(self):

        for region, policies in (
            self.governance.policies.items()
        ):

            mutation_strength = 0.01

            new_policy = copy.deepcopy(
                policies
            )

            for key in new_policy:

                delta = random.uniform(
                    -mutation_strength,
                    mutation_strength
                )

                new_policy[key] += delta

                new_policy[key] = max(
                    0.0,
                    min(
                        1.0,
                        new_policy[key]
                    )
                )

            self.governance.policies[
                region
            ] = new_policy

            self.constitution_history[
                region
            ].append(
                copy.deepcopy(
                    new_policy
                )
            )

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- CONSTITUTIONAL EVOLUTION ---\n"
        )

        for region, history in (
            self.constitution_history.items()
        ):

            print(
                f"{region}: "
                f"{len(history)} constitutional states"
            )
