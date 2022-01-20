from discord import File
from discord.ext import commands

from src.encounter_map_commands.map_entity import MapEntity
from src.encounter_map_commands.map_utils import *


class MapCommands(commands.Cog):
    current_map = None
    map_entities = None

    @commands.command(help='Takes an image resizes it and adds a grid this is used as the current encounter map.')
    async def map_create(self, ctx, block_width, block_height, image_url):
        block_height = int(block_height)
        block_width = int(block_width)
        img = url_to_image(image_url)
        img = resize_map(img, block_width, block_height)
        draw_lines(img, UNIT_SIZE, UNIT_SIZE)
        self.current_map = img
        self.map_entities = []
        cv.imwrite(CURRENT_IMAGE_PATH, img)
        with open(CURRENT_IMAGE_PATH, 'rb') as fp:
            await ctx.channel.send(file=File(fp))
        await ctx.send('Success: The map has been created and set as the current map.')

    @commands.command(help='Places a new map entity on the current map')
    async def map_place(self, ctx, entity_name, entity_start_x, entity_start_y, entity_outline_color_string,
                        entity_icon_image_link):
        if self.current_map is None:
            await ctx.send('Failure: new Entity was not able to be added there is no existing map.')
        else:
            entity_ico = url_to_image(entity_icon_image_link)
            map_block_height = self.current_map.shape[0] // UNIT_SIZE
            entity = MapEntity(entity_name, int(entity_start_x), int(entity_start_y), entity_ico,
                               BGR_STRING_MAP[entity_outline_color_string], map_block_height)
            self.map_entities.append(entity)
            await ctx.send(f'Success: {entity.name} placed at {entity.get_cord_string()}.')

    @commands.command(help='Removes an existing entity from the current map.')
    async def map_remove(self, ctx, entity_name):
        if self.current_map is None:
            await ctx.send('Failure: new Entity was not able to be added there is no existing map.')
            return
        for e in self.map_entities:
            if e.name == entity_name:
                self.map_entities.remove(e)
                await ctx.send(f"Success: {entity_name} has been removed from the current map.")
                return
        await ctx.send(f'Failure: {entity_name} was not found in the list of entities.')

    @commands.command(help='Prints the current map to the screen')
    async def map_show(self, ctx):
        temporary_map = self.current_map.copy()
        draw_entities(temporary_map, self.map_entities)
        cv.imwrite(CURRENT_IMAGE_PATH, temporary_map)
        with open(CURRENT_IMAGE_PATH, 'rb') as fp:
            await ctx.channel.send(file=File(fp))

    @commands.command(help='provides a list of current entities on the map')
    async def map_entities(self, ctx):
        out_str = 'Current Map Entities:\n'
        for e in self.map_entities:
            out_str += f'{e.name} at position {e.get_cord_string()}\n'
        await ctx.send(out_str)

    @commands.command(help='Moves the entity whose name is given on the map by a specified cartesian x and y')
    async def map_move(self, ctx, entity_name, move_x, move_y):
        if self.current_map is None or self.map_entities is None:
            await ctx.send('Failure: There is no existing map.')
            return
        for e in self.map_entities:
            if e.name == entity_name:
                e.move(int(move_x), int(move_y))
                await ctx.send(f'Success: {e.name} has been moved to {e.get_cord_string()}')
                return
        await ctx.send(f'Failure: There is no entity of the name {entity_name}.')
