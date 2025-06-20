import asyncio
from game_contracts.game_ui_abc import GameUI


class ScenarioUI(GameUI):
    def __init__(self, player_id, game_id, runner_client):
        super().__init__(
            player_id=player_id,
            game_id=game_id,
            game_name="sample_game",
            runner_client=runner_client,
        )
        self.runner_client = runner_client
        self.client_id = None
        self.game_state = {}

    def ui_game_cleanup(self) -> bool:
        print("Cleaning up UI resources.")
        return True

    def handle_server_message(self, message):
        if not self.client_id and message.get("client_id"):
            self.client_id = message["client_id"]
            print(f"Assigned client ID: {self.client_id}")
        if message.get("apply_action"):
            print(f"Action applied: {message['apply_action']}")
        if message.get("game_state"):
            print(f"Game state updated: {message['game_state']}")
        if message.get("error"):
            print(f"Error: {message['error']}")
        if message.get("game_over"):
            print("Game over, beginning game cleanup.")
            return self.ui_game_cleanup()
            # Optionally, you might want to exit or reset the game here
        return True
