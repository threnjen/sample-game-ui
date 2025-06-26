import argparse
import asyncio

from game_contracts.runner_client_abc import RunnerClientABC

from src.ui import ScenarioUI


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
        from runners.local.client_runner import LocalRunnerClient

        return LocalRunnerClient()
    else:
        from runners.cloud.client_runner import CloudRunnerClient

        return CloudRunnerClient()


def get_client_game_id(player_id: str, runner: RunnerClientABC) -> dict:
    new_game = input("Start a new game? (y/n): ").strip().lower() == "y"
    # pseudocode here to simulate a choice in what we are loading

    new_game = True if new_game == "y" else False
    game_configs = {"player_id": player_id}

    if not new_game:
        available_games = runner.get_games_for_player(game_configs)
        if available_games:
            print(
                f"Available game ids for player with details {player_id}: {available_games}"
            )
            game_ids = list(available_games.keys())
            game_id = game_ids[0]  # Just pick the first available game for simplicity
            print(f"Loading existing game: {game_id}")
            return {"game_id": game_id}
        else:
            print("No existing games. Starting a new game.")
            new_game = True

    return runner.setup_new_game(game_configs)


async def main():
    args = parse_args()
    game_location = args.game_location
    print(f"Game location: {game_location}")

    runner = get_runner(game_location)
    print(f"Using runner: {runner.__class__.__name__}")

    player_id = (
        "1234567890"  # This could be dynamically/randomly set or passed as an argument
    )

    game_id = get_client_game_id(player_id, runner).get("game_id")
    print(f"Game ID: {game_id}")

    ui = ScenarioUI(player_id, game_id, runner)

    await ui.start()  # Initialize the UI and connect to the server
    print("UI initialized and connected to the server.")

    while True:

        msg = await ui.wait_for_server_response()
        print(f"Got message: {msg}")
        # add additional UI dispatch/rendering logic here

        game_continues = ui.handle_server_message(msg)

        if not game_continues:
            break

        player_selection = input("Enter your action: ")
        # Example: send a message back to the server

        new_message_for_server = {"player 1": player_selection}
        ui.send_action_to_server(new_message_for_server)


if __name__ == "__main__":
    asyncio.run(main())
