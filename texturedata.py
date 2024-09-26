from globals import *
import pygame

texture_data = {
    "player":{"type":"player", "file_path":"res/player.png","size":(TILESIZE*2, TILESIZE*4)},
    "player_jump":{"type":"player", "file_path":"res/player_jump.png","size":(TILESIZE*2, TILESIZE*4)},
    "player_run_left":{"type":"player", "file_path":"res/player_run_left.png","size":(TILESIZE*2, TILESIZE*4)},
    "player_run_right":{"type":"player", "file_path":"res/player_run_right.png","size":(TILESIZE*2, TILESIZE*4)},

    "zombie_static":{"type":"mob", "file_path":"res/zombie.png","size":(TILESIZE*2, TILESIZE*3)},

    "grass":{"type":"block", "file_path":"res/grass.png","size":(TILESIZE, TILESIZE)},
    "dirt":{"type":"block", "file_path":"res/dirt.png","size":(TILESIZE, TILESIZE)},
    "stone":{"type":"block", "file_path":"res/stone.png","size":(TILESIZE, TILESIZE)},
    "wood":{"type":"block", "file_path":"res/wood.png","size":(TILESIZE, TILESIZE)},

    "wand":{"type":"block", "file_path":"res/wand.png","size":(TILESIZE, TILESIZE)},
    "wand_2":{"type":"block", "file_path":"res/wand_2.png","size":(TILESIZE, TILESIZE)},

    "orb":{"type":"block", "file_path":"res/orb.png","size":(TILESIZE, TILESIZE)},
    "orb_2":{"type":"block", "file_path":"res/orb_2.png","size":(TILESIZE, TILESIZE)},
}

def gen_textures() -> dict:
        textures = {}

        for name, data in texture_data.items():
            textures[name] = pygame.transform.scale(pygame.image.load(data["file_path"]).convert_alpha(), data["size"])
        return textures