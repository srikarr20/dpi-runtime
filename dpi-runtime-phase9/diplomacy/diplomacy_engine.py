import numpy as np

class DiplomacyEngine:

    def __init__(
        self,
        regions
    ):

        self.regions = regions

        self.alliances = {}

        self.initialize_relations()

    # ------------------------------------------

    def initialize_relations(self):

        region_names = list(
            self.regions.regions.keys()
        )

        for r1 in region_names:

            self.alliances[r1] = {}

            for r2 in region_names:

                if r1 == r2:

                    continue

                self.alliances[r1][r2] = 0.5

    # ------------------------------------------

    def update_relations(self):

        region_names = list(
            self.regions.regions.keys()
        )

        for r1 in region_names:

            for r2 in region_names:

                if r1 == r2:

                    continue

                field1 = (
                    self.regions.region_fields[r1]
                )

                field2 = (
                    self.regions.region_fields[r2]
                )

                similarity = float(
                    np.mean(
                        np.abs(
                            field1 - field2
                        )
                    )
                )

                alliance_strength = max(
                    0.0,
                    1.0 - similarity
                )

                self.alliances[r1][r2] = (
                    alliance_strength
                )

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- DIPLOMATIC RELATIONS ---\n"
        )

        for region, relations in (
            self.alliances.items()
        ):

            print(f"{region}")

            for other, score in (
                relations.items()
            ):

                print(
                    f"  -> {other}: "
                    f"{score:.3f}"
                )
