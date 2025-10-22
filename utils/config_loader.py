import yaml
from datetime import datetime, timedelta
from state import State, RadarState, SatelliteState, CommandCenterState, EnvironmentState

def load_state_from_config(config_path: str) -> State:
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    sim_cfg = cfg["simulation"]
    env_cfg = cfg["environment"]

    # --- Create EnvironmentState ---
    environment = EnvironmentState(
        adversary=env_cfg["adversary"],
        DEFCON_level=env_cfg["DEFCON_level"],
        icbm_launch_prob_per_day=env_cfg["adversary_missile_activity"]["icbm_launch_prob_per_day"],
        slbm_launch_prob_per_day=env_cfg["adversary_missile_activity"]["slbm_launch_prob_per_day"],
        satellite_population=env_cfg["satellite_population"],
        satellite_misclassification_prob=env_cfg["satellite_misclassification_prob"],
    )

    # --- Create RadarStates ---
    radars = {}
    for radar_cfg in cfg["sensors"]["radars"]:
        radars[radar_cfg["name"]] = RadarState(
            name=radar_cfg["name"],
            type=radar_cfg["type"],
            operational=radar_cfg["operational"],
            detection_accuracy=radar_cfg["detection_accuracy"],
            false_alarm_rate=radar_cfg["false_alarm_rate"],
            orientation=radar_cfg["orientation"]
        )

    # --- Create SatelliteStates
    satellites = {}
    for satellite_cfg in cfg["sensors"]["satellites"]:
        satellites[satellite_cfg["name"]] = SatelliteState(
            name=satellite_cfg["name"],
            type=satellite_cfg["type"],
            operational=satellite_cfg["operational"],
            detection_accuracy=satellite_cfg["detection_accuracy"],
            false_alarm_rate=satellite_cfg["false_alarm_rate"]
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
        radars=radars,
        satellites=satellites,
        command_centers=command_centers,
    )

    return state
