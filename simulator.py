import importlib
import random
import yaml
from utils.config_loader import load_state_from_config

class Simulator:
    def __init__(self, args, log_file_path: str, result_base_path: str):
        random.seed(args.seed)
        self.args = args
        self.log_file_path = log_file_path
        self.result_base_path = result_base_path
        self.state = load_state_from_config(f"configs/{self.args.scenario}/{self.args.model}.yaml")

        # import relevant sim modules
        self.missile_warning = importlib.import_module(f"{args.scenario}.{args.model}.missile_warning", package=None)

    def simulate(self) -> None:
        while self.state.current_time < self.state.end_time:
            self.missile_warning.step(self)

    # def log(self, timestamp: datetime, event: str) -> None:
    #     with open(self.log_file_path, "a") as f:
    #         f.write(f"{timestamp.isoformat()}, {event}\n")