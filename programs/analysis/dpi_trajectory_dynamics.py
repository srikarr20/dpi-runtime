import matplotlib.pyplot as plt
import numpy as np

from core.registry.registry import load_registry
from core.replay.replay import load_session

# ----------------------------------------
# LOAD SESSION REGISTRY
# ----------------------------------------

registry = load_registry()

if len(registry) < 2:

    print(
        "Need multiple sessions "
        "for trajectory dynamics."
    )

    exit()

# ----------------------------------------
# OBSERVABILITY TRAJECTORIES
# ----------------------------------------

mean_intensity = []

variance = []

coherence_width = []

peak_count = []

noise_strength = []

session_indices = []

# ----------------------------------------
# LOAD ALL SESSIONS
# ----------------------------------------

for i, session in enumerate(registry):

    session_id = session["session_id"]

    data = load_session(session_id)

    observables = (
        data["observables"]["observables"]
    )

    mean_intensity.append(
        observables["mean_intensity"]
    )

    variance.append(
        observables["intensity_variance"]
    )

    coherence_width.append(
        observables["coherence_width"]
    )

    peak_count.append(
        observables["peak_count"]
    )

    noise_strength.append(
        observables.get(
            "noise_strength",
            0.0
        )
    )

    session_indices.append(i)

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

plt.plot(
    session_indices,
    coherence_width,
    marker='o',
    label="Coherence Width"
)

plt.plot(
    session_indices,
    peak_count,
    marker='o',
    label="Peak Count"
)

plt.plot(
    session_indices,
    noise_strength,
    marker='o',
    label="Noise Strength"
)

plt.title(
    "DPI Trajectory Dynamics"
)

plt.xlabel("Session Index")

plt.ylabel("Trajectory Metric")

plt.grid(True)

plt.legend()

output_path = (
    "outputs/images/"
    "trajectory_dynamics.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"Saved trajectory dynamics: "
    f"{output_path}"
)

# ----------------------------------------
# EVOLUTION SUMMARY
# ----------------------------------------

print("\n--- TRAJECTORY SUMMARY ---\n")

print(
    f"Sessions analyzed: "
    f"{len(registry)}"
)

print(
    f"Max coherence width: "
    f"{np.max(coherence_width):.4f}"
)

print(
    f"Max peak count: "
    f"{np.max(peak_count)}"
)

print(
    f"Max noise strength: "
    f"{np.max(noise_strength):.4f}"
)
