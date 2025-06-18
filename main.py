from src.ui import UI
from game_contracts.runner_client_abc import RunnerClientABC
import argparse
import asyncio


def parse_args():
    parser = argparse.ArgumentParser(description="Set up the game details.")
    parser.add_argument(
        "game_location",
        type=str,
        help="Location of the game (local or cloud).",
        default="local",
        nargs="?",
    )
    return parser.parse_args()


def get_runner(location: str) -> RunnerClientABC:
    if location == "local":
        from runners.local.runner_client import LocalRunnerClient

        return LocalRunnerClient()
    else:
        from runners.cloud.runner_client import CloudRunnerClient

        return CloudRunnerClient()


async def main():
    args = parse_args()
    game_location = args.game_location
    print(f"Game location: {game_location}")

    runner = get_runner(game_location)
    print(f"Using runner: {runner.__class__.__name__}")

    player_id = "player_id"
    ui = UI(player_id, runner)
    await ui.start()

    # Example: wait for a message and print it
    while True:
        msg = await ui.wait_for_server_response()
        print(f"Got message: {msg}")
        # add additional UI dispatch/rendering logic here


if __name__ == "__main__":
    asyncio.run(main())
