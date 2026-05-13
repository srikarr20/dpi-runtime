import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ----------------------------------------
# LOAD REGIME DATA
# ----------------------------------------

with open(
    "outputs/telemetry/regime_map.json",
    "r"
) as f:

    regime_data = json.load(f)

# ----------------------------------------
# FEATURES
# ----------------------------------------

X = []

y = []

for item in regime_data:

    X.append([
        item["noise_strength"],
        item["coherence_width"],
        item["peak_count"],
        item["variance"]
    ])

    y.append(item["regime"])

X = np.array(X)

y = np.array(y)

# ----------------------------------------
# TRAIN / TEST SPLIT
# ----------------------------------------

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42
    )
)

# ----------------------------------------
# RANDOM FOREST MODEL
# ----------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------------------
# PREDICTIONS
# ----------------------------------------

predictions = model.predict(X_test)

# ----------------------------------------
# REPORT
# ----------------------------------------

print("\n--- CLASSIFICATION REPORT ---\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# ----------------------------------------
# FORECAST SWEEP
# ----------------------------------------

forecast_noise = np.linspace(
    0.0,
    0.25,
    100
)

forecast_labels = []

for noise in forecast_noise:

    synthetic_features = np.array([[
        noise,
        noise * 20,
        noise * 1000,
        noise * 0.2
    ]])

    prediction = model.predict(
        synthetic_features
    )[0]

    forecast_labels.append(prediction)

# ----------------------------------------
# NUMERIC REGIME MAP
# ----------------------------------------

regime_to_numeric = {
    "stable": 0,
    "transitional": 1,
    "unstable": 2
}

numeric_forecast = [
    regime_to_numeric[r]
    for r in forecast_labels
]

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

plt.figure(figsize=(14, 8))

plt.plot(
    forecast_noise,
    numeric_forecast
)

plt.title(
    "Predictive DPI Regime Forecast"
)

plt.xlabel("Noise Strength")

plt.ylabel("Predicted Regime")

plt.yticks(
    [0, 1, 2],
    ["stable", "transitional", "unstable"]
)

plt.grid(True)

output_path = (
    "outputs/images/"
    "predictive_regime_forecast.png"
)

plt.savefig(output_path)

plt.close()

print(
    f"Saved predictive forecast: "
    f"{output_path}"
)

# ----------------------------------------
# SAVE FORECAST DATA
# ----------------------------------------

forecast_output = []

for i in range(len(forecast_noise)):

    forecast_output.append({
        "noise_strength": float(
            forecast_noise[i]
        ),
        "predicted_regime": (
            forecast_labels[i]
        )
    })

with open(
    "outputs/telemetry/"
    "predictive_forecast.json",
    "w"
) as f:

    json.dump(
        forecast_output,
        f,
        indent=4
    )

print(
    "Saved predictive telemetry: "
    "outputs/telemetry/"
    "predictive_forecast.json"
)
