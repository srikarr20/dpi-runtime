class DistributedSemanticMemory:

    def __init__(self):

        self.semantic_archive = []

    def store(
        self,
        detector_id,
        semantic_state
    ):

        self.semantic_archive.append({
            "detector": detector_id,
            "state": semantic_state.tolist()
        })

    def retrieve_recent(self, n=10):

        return self.semantic_archive[-n:]
