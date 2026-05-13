def determine_detector_role(
    meta_state,
    noise_strength
):

    # ----------------------------------------
    # STABILIZATION SPECIALISTS
    # ----------------------------------------

    if (
        meta_state == "stabilized"
        and noise_strength < 0.07
    ):

        return "stabilizer"

    # ----------------------------------------
    # EXPLORATORY SPECIALISTS
    # ----------------------------------------

    if (
        meta_state == "volatile"
        or noise_strength > 0.12
    ):

        return "explorer"

    # ----------------------------------------
    # COORDINATION SPECIALISTS
    # ----------------------------------------

    if meta_state == "adaptive":

        return "mediator"

    # ----------------------------------------
    # DEFAULT
    # ----------------------------------------

    return "generalist"
