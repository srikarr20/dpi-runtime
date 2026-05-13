from core.registry.registry import load_registry

from core.replay.replay import (
    load_session,
    compare_sessions
)

registry = load_registry()

if len(registry) < 2:

    print(
        "Need at least 2 sessions "
        "for comparison."
    )

    exit()

session_a_id = registry[-2]["session_id"]

session_b_id = registry[-1]["session_id"]

print("\n--- COMPARING SESSIONS ---\n")

print(f"Session A: {session_a_id}")

print(f"Session B: {session_b_id}")

session_a = load_session(session_a_id)

session_b = load_session(session_b_id)

comparison = compare_sessions(
    session_a,
    session_b
)

print("\n--- OBSERVABILITY DELTAS ---\n")

for key, value in comparison.items():

    print(f"{key}: {value}")
