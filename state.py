# state.py
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Any, List

@dataclass
class SensorState:
    name: str
    type: str
    operational: bool
    detection_accuracy: float
    false_alarm_rate: float
    last_detection_time: datetime = None
    current_status: str = "idle"
    confidence: float = 0.0

@dataclass
class CommandCenterState:
    name: str
    decision_delay_minutes: int
    last_report_time: datetime = None
    last_assessment: str = None
    confidence: float = 0.0

@dataclass
class EnvironmentState:
    tension_level: int
    adversary: str
    icbm_launch_prob_per_day: float
    slbm_launch_prob_per_day: float
    satellite_population: int
    satellite_misclassification_prob: float

@dataclass
class State:
    # Global simulation properties
    current_time: datetime
    timestep: timedelta
    end_time: datetime

    # Static environment info
    environment: EnvironmentState

    # Dynamic entities
    sensors: Dict[str, SensorState] = field(default_factory=dict)
    command_centers: Dict[str, CommandCenterState] = field(default_factory=dict)

    # Simulation metrics
    detections: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    false_alarms: int = 0
    true_detections: int = 0

    def advance_time(self):
        self.current_time += self.timestep

    def log_detection(self, sensor_name: str, detected: bool, confidence: float):
        self.detections.append({
            "time": self.current_time,
            "sensor": sensor_name,
            "detected": detected,
            "confidence": confidence
        })
        if detected:
            self.true_detections += 1

    def log_decision(self, center_name: str, decision: str, confidence: float):
        self.decisions.append({
            "time": self.current_time,
            "center": center_name,
            "decision": decision,
            "confidence": confidence
        })