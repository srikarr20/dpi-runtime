import numpy as np
import copy

class InheritanceEngine:

    def __init__(
        self,
        regions
    ):

        self.regions = regions

        self.civilization_memory = {}

        self.initialize_memory()

    # ------------------------------------------

    def initialize_memory(self):

        for region in (
            self.regions.regions.keys()
        ):

            self.civilization_memory[
                region
            ] = []

    # ------------------------------------------

    def archive_epoch(self):

        for region in (
            self.regions.regions.keys()
        ):

            field = copy.deepcopy(
                self.regions.region_fields[
                    region
                ]
            )

            self.civilization_memory[
                region
            ].append(field)

    # ------------------------------------------

    def retrieve_heritage(
        self,
        region
    ):

        history = (
            self.civilization_memory[
                region
            ]
        )

        if len(history) == 0:

            return np.zeros(16)

        return np.mean(
            history,
            axis=0
        )

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- CIVILIZATION MEMORY ---\n"
        )

        for region, history in (
            self.civilization_memory.items()
        ):

            print(
                f"{region}: "
                f"{len(history)} epochs stored"
            )
