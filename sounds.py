import pygame
pygame.mixer.init()

AUDIO = {
    "orb":pygame.mixer.Sound('res/orb.x-wav'),
    "orb_2":pygame.mixer.Sound('res/orb_2.wav'),
    "stone":pygame.mixer.Sound('res/stone.x-wav'),
    "grass":pygame.mixer.Sound('res/grass.x-wav'),
    "corrupt_grass":pygame.mixer.Sound('res/grass.x-wav'),
    "crimson_grass":pygame.mixer.Sound('res/grass.x-wav'),
    "dirt":pygame.mixer.Sound('res/dirt.x-wav'),
    "wood":pygame.mixer.Sound('res/Dig_0.x-wav'),
    "jump":pygame.mixer.Sound('res/Jump_1.x-wav'),
    "zombie_1":pygame.mixer.Sound('res/Zombie_38.x-wav'),
    "zombie_2":pygame.mixer.Sound('res/Zombie_39.x-wav'),
}
for name,sound in AUDIO.items():
        if name != "orb":
            sound.set_volume(0.2)
        else:
              sound.set_volume(0.05)
    