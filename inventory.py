from globals import *
from items import *
from events import EventHandler
class Inventory:
    def __init__(self, app, textures) -> None:
        self.app = app
        self.screen = app.screen
        self.textures = textures
        #create initial slots
        self.slots = []
        for index in range(5):
            self.slots.append(Item())
        self.slots[0] = WandItem("wand", 1)
        self.slots[1] = WandItem("wand_2", 1)
        self.slots[2] = BlockItem("wood", 200)
        self.last_item_time = pygame.time.get_ticks()  # Track time of the last item addition
        self.item_interval = 2000  # 2 seconds interval

        self.active_slot = 0

        self.font = pygame.font.Font(None, 30)

    def use(self, player, pos, mob_group):
        if self.slots[self.active_slot].name != "default":
            if items[self.slots[self.active_slot].name].item_type == WandItem:
                self.slots[self.active_slot].use(player, mob_group) #wand
            else:
                self.slots[self.active_slot].use(player, pos) #block

    def add_item(self, item):
        if item.name == "default":
            return

        first_avaliable_slot = len(self.slots) #first empty slot
        target_slot = len(self.slots) #first slot of same name
        for index, slot in enumerate(self.slots):
            if slot.name == "default" and index < first_avaliable_slot:
                first_avaliable_slot = index
            if slot.name == item.name:
                target_slot = index
        if target_slot < len(self.slots):
            self.slots[target_slot].quantity += 1
        elif first_avaliable_slot < len(self.slots):
            self.slots[first_avaliable_slot] = items[item.name].item_type(item.name, 1)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_item_time >= self.item_interval:
            self.add_item(Item(name="wand"))
            self.add_item(Item(name="wand_2"))
            self.last_item_time = current_time  # Reset the timer

        
        if EventHandler.scrolled_up():  #slot picking
            self.active_slot -= 1
        elif EventHandler.scrolled_down():  #slot picking
            self.active_slot += 1
        if self.active_slot < 0:
            self.active_slot = len(self.slots) - 1
        elif self.active_slot > len(self.slots) -1 :
            self.active_slot = 0

           
    def draw(self):
        pygame.draw.rect(self.screen, "gray", pygame.Rect(0,0,(TILESIZE*2)*len(self.slots), TILESIZE*2))

        x_offset = TILESIZE/2
        y_offset = TILESIZE/2

        for i in range(len(self.slots)):
            if i == self.active_slot:
                pygame.draw.rect(self.screen, "white", pygame.Rect(i*(TILESIZE*2), 0, TILESIZE*2, TILESIZE*2))
            pygame.draw.rect(self.screen, "black", pygame.Rect(i*(TILESIZE*2), 0, TILESIZE*2, TILESIZE*2), 2)
                
            if self.slots[i].name != "default":
                self.screen.blit(self.textures[self.slots[i].name], ((x_offset + (TILESIZE*2)*i), y_offset))
                
                self.amount_text = self.font.render(str(self.slots[i].quantity), True, "black")
                self.screen.blit(self.amount_text, ((TILESIZE*2)*i + 5, 5))
        pygame.draw.rect(self.screen, "black", pygame.Rect(0,0,(TILESIZE*2)*len(self.slots), TILESIZE*2), 4)