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
        self._initialize_server()
        self.game_state = {}

    def _ui_game_cleanup(self) -> bool:
        """Clean up UI resources.
        This method is called when the game is over or when the UI needs to be reset."""
        print("Cleaning up UI resources.")
        return True

    def handle_server_message(self, message: dict) -> bool:
        """Handle messages received from the server.
        This method processes the message and updates the UI or game state accordingly.

        The boolean that it returns indicates whether the game should continue running.
        Args:
            message (dict): The message received from the server, which may contain
                            client_id, apply_action, game_state, error, or game_over keys.
        """
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
            return self._ui_game_cleanup()
        return True
