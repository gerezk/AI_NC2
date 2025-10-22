import argparse
import random
import sys
from pathlib import Path

def main():
    import simulator

    boolean = lambda x: (str(x).lower() == 'true')
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenario', type=str, help='One of {CMS}')
    parser.add_argument('--model', type=str, help='One of {historical, modern, AI_1, AI_2, AI_3}')
    parser.add_argument('--seed', type=int, default=random.randrange(sys.maxsize), help='Random seed')
    parser.add_argument('--log', type=boolean, default=False, help='If true, save log files')
    args = parser.parse_args()

    # Check arguments
    assert args.scenario in ['CMS']
    assert args.model in ['historical', 'modern', 'AI_1', 'AI_2', 'AI_3']

    # Base result directory
    results_dir = Path("results") / args.scenario / args.model
    results_dir.mkdir(parents=True, exist_ok=True)  # Creates all intermediate dirs if needed
    result_base_path = results_dir.as_posix() + "/"

    # Log directory and file path
    log_file_path = None
    if args.log:
        log_file_path = Path('log') / args.scenario / args.model / f'{args.scenario}_{args.model}_{args.seed}.log'
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        if log_file_path.is_file(): # delete log file if already exists
            Path.unlink(log_file_path)

    # Execute simulation
    simulation = simulator.Simulator(args, log_file_path, result_base_path)
    # simulation.simulate()

if __name__ == '__main__':
    main()

# example command: python3 main.py --scenario=CMS --model=historical --log=true