import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.units import UnitTypeId

class Tyoskentelijat(sc2.BotAI):
    async def on_step(self, iteration): 
        if iteration == 1:
            await self.chat_send('Mursut tulevat')
        await self.distribute_workers()
        await self.rakenna_spawningpool()

    async def rakenna_spawningpool(self):
        if (self.can_afford(UnitTypeId.SPAWNINGPOOL) and not self.already_pending(UnitTypeId.SPAWNINGPOOL)):
            await self.chat_send('Rakennetaan spawning pool!')
            await self.build(UnitTypeId.SPAWNINGPOOL, self.start_location, max_distance=20)

run_game(maps.get("Triton LE"), [
    Bot(Race.Zerg, Tyoskentelijat()),
    Computer(Race.Zerg, Difficulty.Easy)
], realtime=True)