from typing import Optional, TextIO
from game_data import World, Player, Location, Item, Inventory


def get_location(world, current_x: int, current_y: int) -> Optional[str]:
    location_id = world.map[current_x][current_y]
    print(location_id)
    if location_id != -1:
        print(1)
        location = world.locations.get(location_id)
        print(location)
        if location:
            if location.visited:
                return location.brief_desc
            else:
                location.visited = True
                return location.long_desc
    return None


with (open("map.txt") as map_data, open("locations.txt") as location_data, open("items.txt") as items_data):
    world = World(map_data, location_data, items_data)

    #current_x = 14
    #current_y = 6
    #print()

    #print(get_location(world, current_x, current_y))
            # Now your world object is initialized with the map, locations, and items.
            # You can proceed with your game logic from here.


