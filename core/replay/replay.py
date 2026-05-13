from pathlib import Path

import json


def load_session(session_id):

    session_path = Path(
        f"outputs/sessions/{session_id}"
    )

    observables_path = (
        session_path / "observables.json"
    )

    manifest_path = (
        session_path / "session_manifest.json"
    )

    with open(observables_path, "r") as f:

        observables = json.load(f)

    with open(manifest_path, "r") as f:

        manifest = json.load(f)

    return {
        "manifest": manifest,
        "observables": observables
    }


def compare_sessions(
    session_a,
    session_b
):

    observables_a = (
        session_a["observables"]["observables"]
    )

    observables_b = (
        session_b["observables"]["observables"]
    )

    comparison = {}

    for key in observables_a:

        delta = (
            observables_b[key]
            - observables_a[key]
        )

        comparison[key] = delta

    return comparison
