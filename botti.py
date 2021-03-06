import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.units import UnitTypeId
from sc2.ids.ability_id import AbilityId

class Tyoskentelijat(sc2.BotAI):
    async def on_step(self, iteration): 
        if iteration == 1:
            await self.chat_send('Mursut tulevat')
        await self.distribute_workers()
        await self.rakenna_spawningpool()
        await self.rakenna_extractoreja()
        await self.morphaa_overlordeja()
        await self.morphaa_droneja()

    async def rakenna_spawningpool(self):
        spawningpool_puuttuu = len(self.units.of_type(UnitTypeId.SPAWNINGPOOL)) <= 0
        if (spawningpool_puuttuu and self.can_afford(UnitTypeId.SPAWNINGPOOL) and not self.already_pending(UnitTypeId.SPAWNINGPOOL)):
            await self.chat_send('Rakennetaan spawning pool!')
            await self.build(UnitTypeId.SPAWNINGPOOL, self.start_location, max_distance=20)

    async def rakenna_extractoreja(self):
        extractorien_maara = len(self.units.of_type(UnitTypeId.EXTRACTOR))
        liian_vahan_extractoreja = extractorien_maara < 2
        if (not self.state.vespene_geyser.empty and liian_vahan_extractoreja and self.can_afford(UnitTypeId.EXTRACTOR) and not self.already_pending(UnitTypeId.EXTRACTOR)):
            valittu_geyseri = self.state.vespene_geyser.sorted_by_distance_to(self.start_location)[extractorien_maara]
            await self.chat_send('Rakennetaan extractori!')
            rakentaja = self.workers.random
            await self.do(rakentaja.build(UnitTypeId.EXTRACTOR, valittu_geyseri))

    async def morphaa_overlordeja(self):
        liian_vahan_overlordeja = len(self.units.of_type(UnitTypeId.OVERLORD)) < 5
        if (self.tarpeeksi_larvoja() and liian_vahan_overlordeja and self.can_afford(UnitTypeId.OVERLORD) and not self.already_pending(UnitTypeId.OVERLORD)):
            await self.chat_send('Morphataan overlordeja!')
            larva = self.units.of_type(UnitTypeId.LARVA).random
            treenaus = larva(AbilityId.LARVATRAIN_OVERLORD)
            await self.do(treenaus)
        
    async def morphaa_droneja(self):
        liian_vahan_droneja = len(self.units.of_type(UnitTypeId.DRONE)) < 16
        if (self.tarpeeksi_larvoja() and liian_vahan_droneja and self.can_afford(UnitTypeId.DRONE) and not self.already_pending(UnitTypeId.DRONE)):
            await self.chat_send('Morphataan droneja :)!')
            larva = self.units.of_type(UnitTypeId.LARVA).random
            treenaus = larva(AbilityId.LARVATRAIN_DRONE)
            await self.do(treenaus)

    def tarpeeksi_larvoja(self):
        return len(self.units.of_type(UnitTypeId.LARVA)) >= 1

run_game(maps.get("Triton LE"), [
    Bot(Race.Zerg, Tyoskentelijat()),
    Computer(Race.Zerg, Difficulty.Easy)
], realtime=True)
