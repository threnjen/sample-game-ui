from src.ui import ScenarioUI
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


def get_client_game_id(player_id: str, runner: RunnerClientABC) -> dict:
    new_game = input("Start a new game? (y/n): ").strip().lower() == "y"
    # pseudocode here to simulate a choice in what we are loading

    new_game = True if new_game == "y" else False
    game_configs = {"game_name": "sample_game", "player_id": player_id}

    if not new_game:
        available_games = runner.get_games_for_player(game_configs)
        if available_games:
            print(f"Available game ids for player {player_id}: {available_games}")
            game_id = available_games[
                0
            ]  # Just pick the first available game for simplicity
            print(f"Loading existing game: {game_id}")
            return {"game_id": game_id}
        else:
            print("No existing games. Starting a new game.")
            new_game = True

    return runner.setup_new_game(game_configs).get("game_id")


async def main():
    args = parse_args()
    game_location = args.game_location
    print(f"Game location: {game_location}")

    runner = get_runner(game_location)
    print(f"Using runner: {runner.__class__.__name__}")

    player_id = "player_id"

    game_id = get_client_game_id(player_id, runner)

    ui = ScenarioUI(player_id, game_id, runner)

    ui.initialize_server(game_id)

    await ui.start()
    # Example: wait for a message and print it
    while True:

        msg = await ui.wait_for_server_response()
        print(f"Got message: {msg}")
        # add additional UI dispatch/rendering logic here

        game_continues = ui.handle_message(msg)

        if not game_continues:
            break

        player_selection = input("Enter your action: ")
        # Example: send a message back to the server

        new_message_for_server = {"player 1": player_selection}
        await ui.send_action_to_server(new_message_for_server)

    print("Beginning UI side cleanup.")
    ui.ui_side_cleanup()


if __name__ == "__main__":
    asyncio.run(main())
