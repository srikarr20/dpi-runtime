from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel
from typing import Dict


class ObservabilityMetrics(BaseModel):

    peak_intensity: float
    mean_intensity: float
    intensity_variance: float
    center_of_mass: float
    coherence_width: float
    peak_count: int
    noise_strength: float = 0.0


class TelemetryEvent(BaseModel):

    schema_version: str = "0.1"

    runtime_id: str

    timestamp: str

    observables: ObservabilityMetrics


def build_telemetry_event(observables: Dict):

    metrics = ObservabilityMetrics(**observables)

    event = TelemetryEvent(
        runtime_id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        observables=metrics
    )

    return event
