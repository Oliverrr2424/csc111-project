"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO
#from python_ta.contracts import check_contracts


#@check_contracts
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - name: A string representing the name of the location.
        - position: The coordinates of this location on the game map.
        - brief_desc: A brief description of the location.
        - long_desc: A detailed description of the location.
        - available_directions: A list of directions the player can move from this location.
        - items: A list of items available in this location.
        - visited: A boolean indicating whether the location has been visited before.

    Representation Invariants:
        - name != ''
        - isinstance(self.position, int)
        - len(self.available_directions) >= 0
        - all(isinstance(direction, str) for direction in self.available_directions)
        - all(isinstance(item, Item) for item in self.items)
        - isinstance(self.visited, bool)
    """

    def __init__(self, location_id: int, location_points: int, brief_desc: str, long_desc: str, available_directions: list,
                 items: list) -> None:
        self.location_id = location_id
        self.location_points = location_points
        self.brief_desc = brief_desc
        self.long_desc = long_desc
        self.available_directions = available_directions
        self.visited = False
        self.items = items
        """
        Initialize a new location.
        """

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.


#@check_contracts
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - start_position: The starting position of the item in the game world.
        - target_position: The target position where the item needs to be delivered or used.
        - target_points: The points awarded for delivering or using the item at its target position.
        - skills: The talent that the players could gain after picking up this item.

    Representation Invariants:
        - name != ''
        - start_position >= 0
        - target_position >= 0
        - target_points >= 0
    """

    def __init__(self, name: str, start: int, target: int, target_points: int, item_weights: int, item_description: str) -> None:
        """
        Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points
        self.item_weights = item_weights
        self.description = item_description


#@check_contracts
class Inventory:
    def __init__(self):
        self.items = []
        self.current_weight = 0
        self.max_weight = 10  # Set the maximum weight of the inventory

    def add_item(self, item: Item) -> bool:
        """Add an item to the inventory if it doesn't exceed the maximum weight.
        Returns True if the item was added, False otherwise."""
        if self.current_weight + item.item_weights <= self.max_weight:
            self.items.append(item)
            self.current_weight += item.item_weights
            return True
        return False

    def remove_item(self, item: Item):
        """Remove an item from the inventory and update the current weight."""
        if item in self.items:
            self.items.remove(item)
            self.current_weight -= item.item_weights

    def list_items(self):
        """Return a list of item names in the inventory."""
        return [item.name for item in self.items]

    def view_inventory(self):
        """Display the contents of the inventory, along with the total weight."""
        item_names = self.list_items()
        inventory_contents = ', '.join(item_names) if item_names else 'No items'
        return f"Inventory ({self.current_weight}/{self.max_weight} weight): {inventory_contents}"


#@check_contracts
class World:
    """
    A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map. Each integer represents a different
               location, and -1 represents an invalid, inaccessible space.
        - locations: a dictionary mapping integers to Location objects, representing all locations in the game world.
        - items: a dictionary mapping integers to Item objects, representing all items in the game world.

    Representation Invariants:
        - all(isinstance(row, list) for row in self.map)
        - all(isinstance(location_id, int) and location_id >= 0 for row in self.map for location_id in row if location_id != -1)
        - all(isinstance(location, Location) for location in self.locations.values())
        - all(isinstance(item, Item) for item in self.items.values())
    """

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        self.map = self.load_map(map_data)
        self.locations = {}
        self.items = {}
        self.load_locations(location_data)
        self.load_items(items_data)

    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """

        self.map = []  # Reset map to an empty list if you're initializing or updating the map
        for line in map_data:
            # Split line into numbers, convert to int, and append to self.map
            self.map.append([int(location_id) for location_id in line.split()])
        return self.map

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.

    def load_items(self, items_data: TextIO) -> None:
        """
        Load items from a text file into the game world.

        The file format is expected to be space-separated values:
        start_location need_location points weight name
        """
        self.items = {}

        while True:
            line = items_data.readline().strip()
            if not line:
                break

            parts = line.split()
            start_location = int(parts[0])
            target_location = int(parts[1])
            target_points = int(parts[2])
            weight = int(parts[3])
            name = parts[4].replace('_', ' ')

            description = ""
            desc_line = items_data.readline().strip()
            while desc_line != "END":
                description += desc_line + " "
                desc_line = items_data.readline().strip()

            self.items[start_location] = Item(name, start_location, target_location, target_points, weight, description)

    def load_locations(self, location_data: TextIO) -> None:
        """
        Load locations from a text file into the game world.

        The file format is expected to be:
        LOCATION
        <range start> <range end>
        <points for visiting>
        <brief description>
        <long description>
        END
        """
        self.locations = {}

        while True:
            line = location_data.readline().strip()
            if not line:  # End of file
                break

            if line == "LOCATION":
                range_line = location_data.readline().strip()
                range_start, range_end = map(int, range_line.split())

                points = int(location_data.readline().strip())
                brief_desc = location_data.readline().strip()

                long_desc = ""
                desc_line = location_data.readline().strip()
                while desc_line != "END":
                    long_desc += desc_line + " "
                    desc_line = location_data.readline().strip()

                available_directions = []  # Initialize as empty for now, adjust based on your design
                items = []  # Initialize as empty for now, adjust based on your design

                # Assign the location details to each ID within the specified range
                for location_id in range(range_start, range_end + 1):
                    self.locations[location_id] = Location(location_id, points, brief_desc, long_desc,
                                                           available_directions, items)

    def get_location_by_id(self, location_id):
        return self.locations.get(location_id, None)


#@check_contracts
class Player:
    """
    A Player in the Text Advantage game.

    Instance Attributes:
        - initial_x_point: The initial x-axis position that the player stands.
        - initial_y_point: The initial y-axis position that the player stands.
        - current_x: The current x-axis position that the player stands.
        - current_y: The current y-axis position that the player stands.
        - inventory: A list of the items that the player already found.
        - victory: A boolean indicating whether the player wins this game.
        - current_scores: A integer indicating the current scores of the player.


    Representation Invariants:
        - 0 <= initial_x_point <= 40
        - 0 <= initial_y_point <= 40
        - 0 <= current_x <= 40
        - 0 <= current_y <= 40
        - isinstance(self.victory, bool)
    """

    def __init__(self):

        self.current_x = 14
        self.current_y = 6
        self.inventory = Inventory()  # Initialize the inventory as an instance of Inventory class
        self.victory = False
        self.current_score = 0
        #self.current_location = None

    # def __init__(self, initial_x_point: int = 18, initial_y_point: int = 1):
    #     self.current_x = initial_x_point
    #     self.current_y = initial_y_point
    #     self.inventory = Inventory()  # Initialize the inventory as an instance of Inventory class
    #     self.victory = False
    #     self.current_score = 0
        #self.current_location = None
    def move_north(self, world: World):
        """Move the player one position north (up) if possible."""
        if self.current_y > 0 and world.map[self.current_y - 1][self.current_x] != -1:
            self.current_y -= 1

    def move_south(self, world: World):
        """Move the player one position south (down) if possible."""
        if self.current_y < len(world.map) - 1 and world.map[self.current_y + 1][self.current_x] != -1:
            self.current_y += 1

    def move_east(self, world: World):
        """Move the player one position east (right) if possible."""
        if self.current_x < len(world.map[0]) - 1 and world.map[self.current_y][self.current_x + 1] != -1:
            self.current_x += 1

    def move_west(self, world: World):
        """Move the player one position west (left) if possible."""
        if self.current_x > 0 and world.map[self.current_y][self.current_x - 1] != -1:
            self.current_x -= 1

    def examine(self, item_name: str) -> str:
        """Examine an item in the inventory if the player has 'Glasses'.
           Return the item's description in correct order."""
        if any(i.name == "Glasses" for i in self.inventory.items):
            for item in self.inventory.items:
                if item.name.lower() == item_name.lower():
                    return item.description
            return "Item not found in inventory."
        else:
            return "Unable to examine without Glasses."

    def pick_up_item(self, world, item_name: str) -> str:
        """Pick up an item from the current location and add it to the inventory."""
        current_location = world.get_location(self.current_x, self.current_y)
        if current_location:
            item_to_pick = next((item for item in current_location.items if item.name.lower() == item_name.lower()),
                                None)

            if item_to_pick:
                if self.inventory.add_item(item_to_pick):
                    current_location.items.remove(item_to_pick)
                    self.update_score(item_to_pick.target_points)
                    return f"{item_to_pick.name} has been added to your inventory. Score increased by {item_to_pick.target_points} points."
                else:
                    return "Inventory is full or too heavy."
            else:
                return "Item not found."
        return "You are not in a valid location to pick up items."

    def look_at_item(self, item_name: str) -> str:
        """Look at an item's description in the inventory."""
        for item in self.inventory.items:
            if item.name.lower() == item_name.lower():
                return item.description
        return "Item not found in inventory."

    def magnetic_body(self) -> str:
        """Activate the Magnetic Body ability."""
        # Placeholder for the Magnetic Body ability logic
        """
        TODO: implement the function
        """
        return "Magnetic Body activated."

    def view_score(self) -> str:
        """View the player's current score."""
        return f"Current score: {self.current_score}"

    def view_inventory(self) -> str:
        """Display the contents of the player's inventory, along with the total weight."""
        return self.inventory.view_inventory()

    def available_actions(self, world, y, x, player):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        actions = ["Look", "Inventory", "Quit"]

        if world.map[y - 1][x] != -1:
            actions.append("Go North")

        if world.map[y + 1][x] != -1:
            actions.append("Go South")

        if world.map[y][x + 1] != -1:
            actions.append("Go East")

        if world.map[y][x - 1] != -1:
            actions.append("Go West")

        for item in player.inventory.items:
            if item.name not in [i.name for i in player.inventory.items]:
                actions.append(f"Pick up {item.name}")

        if any(item.name == "Glasses" for item in player.inventory.items):
            actions.append("Examine")
        else:
            actions = [action for action in actions if action != "Examine"]

        if any(item.name == "Lucky exam pencil" for item in player.inventory.items):
            actions.append("Magnetic Body")
        else:
            actions = [action for action in actions if action != "Magnetic Body"]

        return actions

    def get_location(self, world, x: int, y: int) -> Optional[str]:
        """Return the description of the Location object associated with the coordinates (x, y) in the world map,
        if a valid location exists at that position. Return the long description on the first visit and the short
        description on subsequent visits. Locations represented by the number -1 on the map should return None."""
        if 0 <= x < len(world.map) and 0 <= y < len(world.map[0]):
            location_id = world.map[x][y]
            if location_id != -1:
                location = world.locations.get(location_id)
                if location:
                    if location.visited:
                        return location.brief_desc
                    else:
                        location.visited = True
                        return location.long_desc
        return "ok"

    def update_score(self, points: int):
        """Update the player's score by a certain number of points."""
        self.current_score += points
        self.check_victory_condition()

    def check_victory_condition(self):
        """Check if the player meets the conditions for victory."""
        if self.current_score >= 10:  # Assuming 60 points is the victory condition
            self.victory = True
            print("Congratulations! You have won the game.")
        else:
            self.victory = False

    def set_victory(self, status: bool):
        """Directly set the player's victory status."""
        self.victory = status

def main():
    print("1")
    # Create a new world instance
    with open("map.txt") as map_data, open("locations.txt") as location_data, open("items.txt") as items_data:
        world = World(map_data, location_data, items_data)

    # Initialize player
    player = Player()  # Player is initialized with default values

    # Main game loop
    while not player.victory:
        # Get the current location description
        initial_location_description = player.get_location(world, player.current_x, player.current_y)
        print(f"You are at: {initial_location_description}")

            # Display available actions
        actions = player.available_actions(world, player.current_y, player.current_x, player)
        print("Available actions:", ', '.join(actions))

            # Get user input
        command = input("What would you like to do? ").strip().lower()

            # Process user input
        if command.startswith("look at "):
            item_name = command.replace("look at ", "")
            feedback = player.look_at_item(item_name)
            print(feedback)
        if command == "go north":
            player.move_north(world)
        elif command == "go south":
            player.move_south(world)
        elif command == "go east":
            player.move_east(world)
        elif command == "go west":
            player.move_west(world)
        elif command == "inventory":
            print(player.view_inventory())
        elif command == "quit":
            print("Quitting game.")
            break
        elif command.startswith("pick up "):
            item_name = command.replace("pick up ", "")
            feedback = player.pick_up_item(player, item_name)
            print(feedback)
        elif command.startswith("examine "):
            item_name = command.replace("examine ", "")
            feedback = player.examine(item_name)
            print(feedback)
        elif command == "magnetic body":
            feedback = player.magnetic_body()
            print(feedback)
        else:
            print("Invalid action. Try again.")

            # Check for victory after each action
        player.check_victory_condition()  # This method checks and updates the player's victory status

        if player.victory:
            print("Congratulations, you have won the game!")
            break


if __name__ == "__main__":
    main()
