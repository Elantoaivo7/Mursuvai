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
        await self.rakenna_extractor(iteration)

    async def rakenna_spawningpool(self):
        spawningpool_puuttuu = len(self.units.of_type(UnitTypeId.SPAWNINGPOOL)) <= 0
        if (spawningpool_puuttuu and self.can_afford(UnitTypeId.SPAWNINGPOOL) and not self.already_pending(UnitTypeId.SPAWNINGPOOL)):
            await self.chat_send('Rakennetaan spawning pool!')
            await self.build(UnitTypeId.SPAWNINGPOOL, self.start_location, max_distance=20)

    async def rakenna_extractor(self, iteration):
        extractor_puuttuu = len(self.units.of_type(UnitTypeId.EXTRACTOR)) <= 0
        if (not self.state.vespene_geyser.empty and extractor_puuttuu and self.can_afford(UnitTypeId.EXTRACTOR) and not self.already_pending(UnitTypeId.EXTRACTOR)):
            lahin_geyseri = self.state.vespene_geyser.first
            await self.chat_send('Rakennetaan extractori!')
            rakentaja = self.workers.random
            await self.do(rakentaja.build(UnitTypeId.EXTRACTOR, lahin_geyseri))

run_game(maps.get("Triton LE"), [
    Bot(Race.Zerg, Tyoskentelijat()),
    Computer(Race.Zerg, Difficulty.Easy)
], realtime=True)