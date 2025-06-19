import asyncio
from game_contracts.game_ui import GameUI


class ScenarioUI(GameUI):
    def __init__(self, player_id, game_id, runner_client):
        self.runner_client = runner_client
        self.queue = asyncio.Queue()
        self.client_id = None
        self.game_state = {}
        self.player_id = player_id
        self.game_id = game_id

    def initialize_server(self, game_id):
        self.game_state = self.runner_client.initialize_server(game_id)
        print(f"Game state initialized")

    async def start(self):
        asyncio.create_task(self.background_poll_loop())
        print("UI is running")

    def send_action_to_server(self, payload):
        return self.runner_client.send_action_to_server(payload)

    async def wait_for_server_response(self):
        return await self.queue.get()

    async def background_poll_loop(self):
        while True:
            msg = await self.runner_client.poll_for_server_response()
            await self.queue.put(msg)

    def ui_side_cleanup(self):
        print("Cleaning up UI resources.")

    def handle_message(self, incoming_message):

        if not self.client_id and incoming_message.get("client_id"):
            self.client_id = incoming_message["client_id"]
            print(f"Assigned client ID: {self.client_id}")
        if incoming_message.get("apply_action"):
            print(f"Action applied: {incoming_message['apply_action']}")
        if incoming_message.get("game_state"):
            print(f"Game state updated: {incoming_message['game_state']}")
        if incoming_message.get("error"):
            print(f"Error: {incoming_message['error']}")
        if incoming_message.get("game_over"):
            print("Game over, beginning game cleanup.")
            return self.ui_side_cleanup()
            # Optionally, you might want to exit or reset the game here
        return True
