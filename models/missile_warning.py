import datetime
import random

# class MissileWarning:
#     def __init__(self, state, simulator):
#         self.state = state
#         self.simulator = simulator

def step(simulator) -> None:
    simulator.state.current_time += simulator.state.US_warning

def roll_dice() -> bool:
    assert False

def log(simulator, event: str) -> None:
    with open(simulator.log_file_path, "a") as f:
        f.write(f"{simulator.state.current_time.isoformat()}, {event}\n")