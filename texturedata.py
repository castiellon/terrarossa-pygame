from globals import *
import pygame

texture_data = {
    "player":{"type":"player", "file_path":"res/player.png","size":(TILESIZE, TILESIZE*2)},
    "player_jump":{"type":"player", "file_path":"res/player_jump.png","size":(TILESIZE, TILESIZE*2)},
    "player_run_left":{"type":"player", "file_path":"res/player_run_left.png","size":(TILESIZE, TILESIZE*2)},
    "player_run_right":{"type":"player", "file_path":"res/player_run_right.png","size":(TILESIZE, TILESIZE*2)},

    "grass":{"type":"block", "file_path":"res/grass.png","size":(TILESIZE, TILESIZE)},
    "dirt":{"type":"block", "file_path":"res/dirt.png","size":(TILESIZE, TILESIZE)},
    "stone":{"type":"block", "file_path":"res/stone.png","size":(TILESIZE, TILESIZE)}
}

def gen_textures() -> dict:
        textures = {}

        for name, data in texture_data.items():
            textures[name] = pygame.transform.scale(pygame.image.load(data["file_path"]).convert_alpha(), data["size"])
        return textures