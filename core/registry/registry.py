from pathlib import Path

import json


REGISTRY_PATH = (
    "outputs/sessions/session_registry.json"
)


def load_registry():

    registry_file = Path(REGISTRY_PATH)

    if not registry_file.exists():

        return []

    with open(registry_file, "r") as f:

        return json.load(f)


def append_session(session_metadata):

    registry = load_registry()

    registry.append(session_metadata)

    with open(REGISTRY_PATH, "w") as f:

        json.dump(
            registry,
            f,
            indent=4
        )


def list_sessions():

    registry = load_registry()

    for session in registry:

        print(
            f"{session['session_id']} "
            f"| {session['timestamp']}"
        )
