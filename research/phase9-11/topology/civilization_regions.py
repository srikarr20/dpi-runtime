import numpy as np
import random

class CivilizationRegions:

    def __init__(
        self,
        detectors,
        num_regions=3
    ):

        self.detectors = detectors

        self.num_regions = num_regions

        self.regions = {}

        self.region_fields = {}

        self.initialize_regions()

    # ------------------------------------------

    def initialize_regions(self):

        for i in range(
            self.num_regions
        ):

            self.regions[
                f"Region-{i}"
            ] = []

        # --------------------------------------

        for detector in self.detectors:

            region = random.choice(
                list(
                    self.regions.keys()
                )
            )

            self.regions[
                region
            ].append(detector)

        # --------------------------------------

        self.update_region_fields()

    # ------------------------------------------

    def update_region_fields(self):

        for region, members in (
            self.regions.items()
        ):

            if len(members) == 0:

                self.region_fields[
                    region
                ] = np.zeros(16)

                continue

            states = []

            for detector in members:

                states.append(
                    detector.semantic_state
                )

            self.region_fields[
                region
            ] = np.mean(
                states,
                axis=0
            )

    # ------------------------------------------

    def get_region(
        self,
        detector
    ):

        for region, members in (
            self.regions.items()
        ):

            if detector in members:

                return region

        return None

    # ------------------------------------------

    def migrate_detector(
        self,
        detector,
        target_region
    ):

        current = self.get_region(
            detector
        )

        if current == target_region:

            return

        self.regions[
            current
        ].remove(detector)

        self.regions[
            target_region
        ].append(detector)

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- CIVILIZATION REGIONS ---\n"
        )

        for region, members in (
            self.regions.items()
        ):

            print(
                f"{region}: "
                f"{len(members)} detectors"
            )
