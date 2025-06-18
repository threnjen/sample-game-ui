import asyncio
from game_contracts.game_ui import GameUI


class UI(GameUI):
    def __init__(self, player_id, runner_client):
        self.runner_client = runner_client
        self.queue = asyncio.Queue()

    async def start(self):
        asyncio.create_task(self.background_poll_loop())
        print("UI is running")

    def send_action_to_server(self, actions):
        return self.runner_client.send_action_to_server(actions)

    async def wait_for_server_response(self):
        return await self.queue.get()

    async def background_poll_loop(self):
        while True:
            msg = await self.runner_client.poll_for_server_response()
            await self.queue.put(msg)
