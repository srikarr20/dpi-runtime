import random

class TopologyGraph:

    def __init__(
        self,
        detectors,
        connectivity=0.3
    ):

        self.detectors = detectors

        self.connectivity = connectivity

        self.graph = {}

        self.initialize_graph()

    # ------------------------------------------

    def initialize_graph(self):

        for detector in self.detectors:

            neighbors = []

            for other in self.detectors:

                if other.id == detector.id:

                    continue

                if random.random() < self.connectivity:

                    neighbors.append(
                        other.id
                    )

            self.graph[
                detector.id
            ] = neighbors

    # ------------------------------------------

    def get_neighbors(
        self,
        detector_id
    ):

        return self.graph.get(
            detector_id,
            []
        )

    # ------------------------------------------

    def summary(self):

        print(
            "\n--- TOPOLOGY SUMMARY ---\n"
        )

        for detector, neighbors in self.graph.items():

            print(
                f"{detector}: "
                f"{len(neighbors)} neighbors"
            )
