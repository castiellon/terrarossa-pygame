from globals import *
from sprite import *
from sounds import *

class Item:
    def __init__(self, name: str = "default", quantity: int = 0) -> None:
        self.name = name
        self.quantity = quantity

    def use(self, *args, **kwargs):
        pass
    def __str__(self) -> str:
        return f"Name: {self.name}, Quantity: {self.quantity}"

class BlockItem(Item): #placable item
    def __init__(self, name: str, quantity: int = 0) -> None:
        super().__init__(name, quantity)
    def use(self, player, position: tuple): #placing the block
        if self.quantity>0:
            AUDIO[self.name].play()
            block_entity = items[self.name].use_type([player.group_list[group] for group in items[self.name].groups], position, player.textures[self.name])
            block_entity.name = self.name
            self.quantity -= 1
            
            #print(f"played sound for {self.name}")
            if self.quantity <= 0:
                self.name = "default"
        else:
            self.name = "default"

def calculate_direction(start_pos, end_pos):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return pygame.math.Vector2(0, 0)
    return pygame.math.Vector2(dx / distance, dy / distance)

class WandItem(Item):
    def __init__(self, name: str , quantity: int = 0) -> None:
        super().__init__(name, quantity)
        self.projectiles = {
            "wand":"orb",
            "wand_2":"orb_2" 
        }
    def use(self, player, mob_group):
        direction = calculate_direction(player.rect.center, player.get_adjusted_mouse_position())
        self.player = player
        self.mob_group = mob_group
        self.damage = items[self.name].damage
        self.projectile_speed = items[self.name].projectile_speed
        Orb([player.group_list["sprites"]], player.rect.center, player.textures[self.projectiles[self.name]], direction, {"mob_group":self.mob_group,
                                                                                                                          "player": self.player,
                                                                                                                          "wand":self})
        AUDIO[self.projectiles[self.name]].play()
        
        self.quantity -= 1
        if self.quantity <= 0:
            self.name = "default"





class ItemData:
    def __init__(self,
                name: str,
                quantity: int = 0,
                groups: list[str] = ["sprites", "block_group"],
                use_type: Entity = Entity,
                item_type: Item = Item,
                damage: int = 0,
                projectile_speed: int = 0) -> None:
        self.name = name
        self.quantity = quantity
        self.groups = groups
        self.use_type = use_type
        self.item_type = item_type
        self.damage = damage
        self.projectile_speed = projectile_speed

items: dict[str, ItemData] = {
    "grass":ItemData("grass", item_type=BlockItem),
    "corrupt_grass":ItemData("corrupt_grass", item_type=BlockItem),
    "crimson_grass":ItemData("crimson_grass", item_type=BlockItem),
    "dirt":ItemData("dirt", item_type=BlockItem),
    "stone":ItemData("stone", item_type=BlockItem),
    "wood":ItemData("wood", item_type=BlockItem),
    "wand":ItemData("wand",item_type=WandItem, damage=1, projectile_speed = 10),
    "wand_2":ItemData("wand_2",item_type=WandItem,damage=2, projectile_speed = 6)
}
print(items["wand"].projectile_speed)