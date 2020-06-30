import sys
import pygame

"""This is a cut scean from the main game window to the fight window. It only places down black tiles."""

def fade_to_black():
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 120

    win = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Zombie City")
    icon = pygame.image.load('Art/four_way_stop.png')
    pygame.display.set_icon(icon)

    # Images
    blank_tile = pygame.image.load('Art/cut_scean_tiles.png')

    # Variables
    tile_x = 0
    tile_y = 0

    run = True
    while run:
        clock.tick(FPS)
        win.fill([250, 250, 250])

        for item in range(0, 47):
            win.blit(blank_tile, (tile_x, tile_y))
            pygame.display.update()
            pygame.time.wait(10)
            tile_x += 150
            if tile_x > 1050:
                tile_x = 0
                tile_y += 150
            if tile_y > 1000:
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        pygame.display.update()
    return


# fade_to_black()
