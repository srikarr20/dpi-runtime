def build_coalitions(detector_states):

    coalitions = {
        "stable_cluster": [],
        "adaptive_cluster": [],
        "exploratory_cluster": []
    }

    for detector_id, state in detector_states.items():

        semantic = state["semantic"]

        if semantic == "stable":

            coalitions[
                "stable_cluster"
            ].append(detector_id)

        elif semantic == "transitional":

            coalitions[
                "adaptive_cluster"
            ].append(detector_id)

        else:

            coalitions[
                "exploratory_cluster"
            ].append(detector_id)

    return coalitions
