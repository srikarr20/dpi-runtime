from datetime import datetime
from uuid import uuid4

from pathlib import Path

import json

from core.registry.registry import append_session


def create_runtime_session():

    session_id = str(uuid4())

    timestamp = datetime.utcnow().isoformat()

    session_path = Path(
        f"outputs/sessions/{session_id}"
    )

    session_path.mkdir(
        parents=True,
        exist_ok=True
    )

    manifest = {
        "session_id": session_id,
        "timestamp": timestamp,
        "schema_version": "0.1"
    }

    manifest_path = (
        session_path / "session_manifest.json"
    )

    with open(manifest_path, "w") as f:

        json.dump(
            manifest,
            f,
            indent=4
        )

    session_metadata = {
        "session_id": session_id,
        "timestamp": timestamp,
        "session_path": str(session_path),
        "manifest_path": str(manifest_path)
    }

    append_session(session_metadata)

    return session_metadata
