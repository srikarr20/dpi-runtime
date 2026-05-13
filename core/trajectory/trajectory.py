import json
from pathlib import Path

TRAJECTORY_FILE = "outputs/telemetry/trajectory_history.json"

def append_observables(observables):

    trajectory_path = Path(TRAJECTORY_FILE)

    # ----------------------------------------
    # LOAD EXISTING HISTORY
    # ----------------------------------------

    if trajectory_path.exists():

        with open(trajectory_path, "r") as f:

            history = json.load(f)

    else:

        history = []

    # ----------------------------------------
    # APPEND NEW OBSERVABLES
    # ----------------------------------------

    history.append(observables)

    # ----------------------------------------
    # SAVE UPDATED HISTORY
    # ----------------------------------------

    with open(trajectory_path, "w") as f:

        json.dump(
            history,
            f,
            indent=4
        )

    print(f"Updated trajectory history: {TRAJECTORY_FILE}")
