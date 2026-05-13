import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

from core.telemetry.observables import extract_observables

# ----------------------------------------
# DETECTOR PLANE
# ----------------------------------------

detector_x = np.linspace(-20, 20, 3000)

# ----------------------------------------
# STORAGE
# ----------------------------------------

vectors = []
labels = []
regions = []

# ----------------------------------------
# EVOLUTION LOOP
# ----------------------------------------

steps = 25

for step in range(steps):

    # ----------------------------------------
    # EVOLVING PARAMETERS
    # ----------------------------------------

    noise_strength = step * 0.025

    modulation_strength = max(
        1.0 - (step * 0.03),
        0.05
    )

    # ----------------------------------------
    # SOURCE FIELD
    # ----------------------------------------

    source_field = np.exp(
        -(detector_x)**2 / 20
    )

    # ----------------------------------------
    # MODULATION
    # ----------------------------------------

    coherence_pattern = (
        np.cos(detector_x * 2)
        * modulation_strength
    )

    # ----------------------------------------
    # NOISE
    # ----------------------------------------

    noise = np.random.normal(
        0,
        noise_strength,
        size=len(detector_x)
    )

    # ----------------------------------------
    # FIELD
    # ----------------------------------------

    field = (
        source_field
        * coherence_pattern
    )

    field += noise

    # ----------------------------------------
    # INTENSITY
    # ----------------------------------------

    intensity = np.abs(field)**2

    intensity /= np.max(intensity)

    # ----------------------------------------
    # OBSERVABLES
    # ----------------------------------------

    observables = extract_observables(
        detector_x,
        intensity
    )

    vector = [

        observables["peak_intensity"],
        observables["mean_intensity"],
        observables["intensity_variance"],
        observables["center_of_mass"],
        observables["coherence_width"],
        observables["peak_count"]

    ]

    vectors.append(vector)

    labels.append(step)

    # ----------------------------------------
    # REGION CLASSIFICATION
    # ----------------------------------------

    if observables["coherence_width"] < 4:

        region = "stable"

    elif observables["coherence_width"] < 8:

        region = "transitional"

    else:

        region = "unstable"

    regions.append(region)

# ----------------------------------------
# PCA
# ----------------------------------------

vectors = np.array(vectors)

pca = PCA(n_components=2)

projection = pca.fit_transform(vectors)

# ----------------------------------------
# COLOR MAP
# ----------------------------------------

color_map = {

    "stable": "green",
    "transitional": "orange",
    "unstable": "red"
}

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(12, 8))

for i in range(len(labels)):

    x = projection[i, 0]
    y = projection[i, 1]

    region = regions[i]

    plt.scatter(
        x,
        y,
        color=color_map[region],
        s=140
    )

    plt.text(
        x + 1,
        y + 1,
        str(labels[i]),
        fontsize=9
    )

# ----------------------------------------
# TRAJECTORY PATH
# ----------------------------------------

plt.plot(
    projection[:, 0],
    projection[:, 1],
    alpha=0.5
)

# ----------------------------------------
# LEGEND
# ----------------------------------------

for region, color in color_map.items():

    plt.scatter(
        [],
        [],
        color=color,
        label=region,
        s=120
    )

plt.legend()

# ----------------------------------------
# LABELS
# ----------------------------------------

plt.title(
    "DPI Trajectory Region Classification"
)

plt.xlabel(
    "Principal Component 1"
)

plt.ylabel(
    "Principal Component 2"
)

plt.grid(True)

# ----------------------------------------
# SAVE
# ----------------------------------------

output_path = (
    "outputs/images/trajectory_regions.png"
)

plt.savefig(output_path)

print(
    f"Saved trajectory regions: {output_path}"
)

plt.close()

# ----------------------------------------
# SAVE REGION DATA
# ----------------------------------------

region_output = []

for i in range(len(labels)):

    region_output.append({

        "step": labels[i],
        "region": regions[i]

    })

with open(
    "outputs/trajectories/trajectory_regions.json",
    "w"
) as f:

    json.dump(
        region_output,
        f,
        indent=4
    )

print(
    "Saved trajectory region metadata."
)
