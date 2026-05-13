import random


def reproduce_detector(parent):

    child = {
        "noise": parent["noise"],
        "trust": parent["trust"],
        "generation": parent[
            "generation"
        ] + 1
    }

    # ----------------------------------------
    # MUTATION
    # ----------------------------------------

    mutation = random.uniform(
        -0.01,
        0.01
    )

    child["noise"] += mutation

    child["noise"] = max(
        0.01,
        child["noise"]
    )

    return child


def should_remove_detector(
    detector
):

    if detector["trust"] < 0.20:

        return True

    if detector["noise"] > 0.25:

        return True

    return False
