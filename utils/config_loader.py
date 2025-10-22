# utils/config_loader.py
import yaml
from datetime import datetime, timedelta
from state import State, SensorState, CommandCenterState, EnvironmentState

def load_state_from_config(config_path: str) -> State:
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    sim_cfg = cfg["simulation"]
    env_cfg = cfg["environment"]

    # --- Create EnvironmentState ---
    environment = EnvironmentState(
        tension_level=env_cfg["tension_level"],
        adversary=env_cfg["adversary"],
        icbm_launch_prob_per_day=env_cfg["adversary_missile_activity"]["icbm_launch_prob_per_day"],
        slbm_launch_prob_per_day=env_cfg["adversary_missile_activity"]["slbm_launch_prob_per_day"],
        satellite_population=env_cfg["satellite_population"],
        satellite_misclassification_prob=env_cfg["satellite_misclassification_prob"],
    )

    # --- Create SensorStates ---
    sensors = {}
    for radar_cfg in cfg["sensors"]["radars"]:
        sensors[radar_cfg["name"]] = SensorState(
            name=radar_cfg["name"],
            type=radar_cfg["type"],
            operational=radar_cfg["operational"],
            detection_accuracy=radar_cfg["detection_accuracy"],
            false_alarm_rate=radar_cfg["false_alarm_rate"]
        )
    for radar_cfg in cfg["sensors"]["south_radars"]:
        sensors[radar_cfg["name"]] = SensorState(
            name=radar_cfg["name"],
            type="FPS",
            operational=radar_cfg["operational"],
            detection_accuracy=radar_cfg["detection_accuracy"],
            false_alarm_rate=radar_cfg["false_alarm_rate"]
        )

    # --- Command Centers ---
    command_centers = {}
    for cc_cfg in cfg["command_centers"]:
        command_centers[cc_cfg["name"]] = CommandCenterState(
            name=cc_cfg["name"],
            decision_delay_minutes=cc_cfg["decision_delay_minutes"]
        )

    # --- Build State ---
    state = State(
        current_time=datetime.fromisoformat(sim_cfg["start_date"]),
        timestep=timedelta(minutes=sim_cfg["timestep_minutes"]),
        end_time=datetime.fromisoformat(sim_cfg["end_date"]),
        environment=environment,
        sensors=sensors,
        command_centers=command_centers,
    )

    return state
