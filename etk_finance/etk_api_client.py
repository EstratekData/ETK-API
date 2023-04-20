import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description='ETK API client')

# Add a positional argument for the command
parser.add_argument('command', help='The command to execute')

# Add optional arguments for the command
parser.add_argument('--arg1', help='First argument for the command')
parser.add_argument('--arg2', help='Second argument for the command')

# Parse the command-line arguments
args = parser.parse_args()

# Check if the command is missing
if not hasattr(args, 'command'):
    print('Usage: etk-api-client.py <command> [--arg1 <arg1>] [--arg2 <arg2>]')
else:
    # Execute the command
    print(f'Executing command: {args.command}')
    print(f'Argument 1: {args.arg1}')
    print(f'Argument 2: {args.arg2}')