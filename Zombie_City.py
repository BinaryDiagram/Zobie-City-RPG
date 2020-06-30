import pygame
from pygame import mixer
import sys
import math
import random
import time


def main_game():
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 120

    win = pygame.display.set_mode((1000, 1000))

    X, Y = pygame.display.get_surface().get_size()
    # print("Title Screen Canvas size: ", X, Y)

    start_of_game = time.time()

    # SFX
    tile_sound = mixer.Sound('SFX/tile_discovery.wav')
    combat_sound = mixer.Sound('SFX/combat_start.wav')

    boss_fight = mixer.Sound("SFX/boss_fight.wav")
    fight_music = mixer.Sound("SFX/fight.wav")
    bgm = mixer.Sound("SFX/zombie_city_bgm.wav")
    bgm.play(-1)


    # images
    character_img = pygame.image.load('Art/character.png')
    zombie_img = pygame.image.load('Art/zombie.png')
    zombie75_img = pygame.image.load('Art/zombie75.png')
    zombie50_img = pygame.image.load('Art/zombie50.png')
    zombie25_img = pygame.image.load('Art/zombie25.png')
    frozen_zombie = pygame.image.load('Art/frozen_zombie.png')
    east_west_north_road = pygame.image.load('Art/east_west_north_road.png')
    east_west_road = pygame.image.load('Art/east_west_road.png')
    east_west_south_road = pygame.image.load('Art/east_west_south_road.png')
    north_south_east_road = pygame.image.load('Art/north_south_east_road.png')
    north_south_road = pygame.image.load('Art/north_south_road.png')
    north_south_west = pygame.image.load('Art/north_south_west_road.png')
    north_west_road = pygame.image.load('Art/north_west_road.png')
    north_east_road = pygame.image.load('Art/north_east_road.png')
    south_west_road = pygame.image.load('Art/south_west_road.png')
    south_east_road = pygame.image.load('Art/south_east_road.png')
    four_way_img = pygame.image.load('Art/four_way_stop.png')
    boss_lair_tile = pygame.image.load('Art/boss_tile.png')
    necromancer = pygame.image.load('Art/necromancer.png')
    necromancer75 = pygame.image.load('Art/necromancer75.png')
    necromancer50 = pygame.image.load('Art/necromancer50.png')
    necromancer25 = pygame.image.load('Art/necromancer25.png')


    # Fonts and texts
    character_font = pygame.font.Font('freesansbold.ttf', 20)
    searching_font = pygame.font.Font('freesansbold.ttf', 50)
    searching_text = searching_font.render("Searching...", True, (201, 172, 28))
    found_health_potion = character_font.render("You found a health potion", True, (201, 172, 28))
    found_mana_potion = character_font.render("You found a mana potion", True, (201, 172, 28))
    found_bullets = character_font.render("You found 5 bullets", True, (201, 172, 28))
    search_direction_text = character_font.render("Press enter to search the area.", True, (0, 0, 0))
    tab_direction_text = character_font.render("Press tab to oppen you invintory", True, (0, 0, 0))
    arrow_keys_direction_text = character_font.render("Use the arrow keys to move around the map.", True, (0, 0, 0))

    # Player variables
    player_x_change, player_y_change, player_vel, player_pushback = 0, 0, 2, 3
    player_x, player_y = (X / 2) - 10, (Y / 2) - 10
    pz_collision = 20
    player_hp_total = 100
    player_mana_total = 50

#TODO change the item list into a dictionary so we wont have to pass a million arguments through functions.
# then modify the item menu and fight page so it can work with dictionarys.
    searching = False
    health_potion_found = False
    mana_potion_found = False
    bullets_found = False
    health_potion_total, mana_potion_total, pistol_bullets = 0, 0, 5

    # Variables for creating new tiles from which road the player takes
    tile_size = 143
    half_tile_size = 72

    # tile top left points at various location so the screen can be split into a grid
    tile_0_0_x = ((X/2) - half_tile_size) - (2 * tile_size)
    tile_1_0_x = ((X/2) - half_tile_size) - tile_size
    tile_2_0_x = (X/2) - half_tile_size
    tile_3_0_x = ((X/2) - half_tile_size) + tile_size
    tile_4_0_x = ((X/2) - half_tile_size) + (2 * tile_size)
    tile_5_0_x = ((X / 2) - half_tile_size) + (3 * tile_size) - 20

    tile_0_0_y = ((Y / 2) - half_tile_size) - (2 * tile_size)
    tile_0_1_y = ((Y / 2) - half_tile_size) - tile_size
    tile_0_2_y = (Y / 2) - half_tile_size
    tile_0_3_y = ((Y / 2) - half_tile_size) + tile_size
    tile_0_4_y = ((Y / 2) - half_tile_size) + (2 * tile_size)
    tile_0_5_y = ((Y / 2) - half_tile_size) + (3 * tile_size) - 20

    tile_x = [tile_0_0_x, tile_1_0_x, tile_2_0_x, tile_3_0_x, tile_4_0_x, tile_5_0_x]
    tile_y = [tile_0_0_y, tile_0_1_y, tile_0_2_y, tile_0_3_y, tile_0_4_y, tile_0_5_y]

    # Variables to start the game off with
    quadrent_x, quadrent_y = 0, 0
    origonal_player_quadrent = [2, 2]
    previous_quadrent = origonal_player_quadrent

    # lists that contain compatible roads for certain directions.
    west_compatible_tiles = [east_west_north_road, east_west_road, east_west_south_road, north_south_east_road, north_east_road, south_east_road]
    south_compatible_tiles = [east_west_north_road, north_south_road, north_south_west, north_east_road, north_west_road]
    east_compatible_tiles = [east_west_north_road, east_west_road, east_west_south_road, north_south_west, south_west_road, north_west_road]
    north_compatible_tiles = [east_west_south_road, north_south_road, north_south_west, south_east_road, south_west_road]
    north_3_west_compatible_tiles = [east_west_road, east_west_south_road, south_east_road]
    north_3_east_compatible_tiles = [east_west_road, east_west_south_road, south_west_road]
    north_3_north_compatible_tiles = [east_west_south_road, south_east_road, south_west_road]
    east_3_north_compatible_tiles = [north_south_road, north_south_west, south_west_road]
    east_3_south_compatible_tiles = [north_south_road, north_south_west, north_west_road]
    east_3_east_compatible_tiles = [north_south_west, north_west_road, south_west_road]
    south_3_south_compatible_tiles = [east_west_north_road, north_east_road, north_west_road]
    south_3_east_compatible_tiles = [east_west_north_road, east_west_road, north_west_road]
    south_3_west_compatible_tiles = [east_west_north_road, east_west_road, north_east_road]
    west_3_north_compatible_tiles = [north_south_east_road, north_south_road, south_east_road]
    west_3_west_compatible_tiles = [north_south_east_road, south_east_road, north_east_road]
    west_3_south_compatible_tiles = [north_south_road, north_east_road, north_south_east_road]
    # TODO the roads with only one variable probably can just use the origonal variables.
    north_east_compatible_tiles = [south_west_road]
    north_west_compatible_tiles = [south_east_road]
    south_east_compatible_tiles = [north_west_road]
    south_west_compatible_tiles = [north_east_road]
    boss_tile = [boss_lair_tile]
    boss_tile_set = ''

    # the number of items in the compatible roads lists
    east_west_num = 5
    north_south_num = 4
    sides_num = 2

    max_tiles = 5
    # Tile dictionarys
    tile_set = {}
    draw_x = {}
    draw_y = {}
    compatible_tile = {}
    rand_int = {}
    #Zombie dictionarys / Zombie variables
    # zombie spawn variables for 2,2 need to be all False or we spawn on top of a zombie and fight right off the bat.
    zombie_dice_roll = {}
    zombie_spawn = {}
    zombie_x = {}
    zombie_y = {}
    zombie_rand_move = {}
    z_quadrent_x = {}
    z_quadrent_y = {}
    zombie_hp_total = {}
    for item in range(0, max_tiles):
        for item2 in range(0, max_tiles):
            # Tile Variables
            tile_set.update({'{0}, {1}'.format(item, item2): ''})
            draw_x.update({'{0}, {1}'.format(item, item2): ''})
            draw_y.update({'{0}, {1}'.format(item, item2): ''})
            compatible_tile.update({'{0}, {1}'.format(item, item2): ''})
            rand_int.update({'{0}, {1}'.format(item, item2): ''})
            # Zombie Variables
            zombie_spawn.update({'{0}, {1}'.format(item, item2): ''})
            zombie_rand_move.update({'{0}, {1}'.format(item, item2): random.randint(0, 3)})
            zombie_dice_roll.update({'{0}, {1}'.format(item, item2): random.randint(1, 6)})
            zombie_x.update({'{0}, {1}'.format(item, item2): ''})
            zombie_y.update({'{0}, {1}'.format(item, item2): ''})
            z_quadrent_x.update({'{0}, {1}'.format(item, item2): ''})
            z_quadrent_y.update({'{0}, {1}'.format(item, item2): ''})
            zombie_hp_total.update({'{0}, {1}'.format(item, item2): 100})

    # update the 2, 2 locations with variables that wont spawn a zombie.
    zombie_spawn.update({'{0}, {1}'.format(2, 2): False})
    zombie_rand_move.update({'{0}, {1}'.format(2, 2): None})
    zombie_dice_roll.update({'{0}, {1}'.format(2, 2): 0})
    zombie_x.update({'{0}, {1}'.format(2, 2): 0})
    zombie_y.update({'{0}, {1}'.format(2, 2): 0})

    # Zombie variables
    zombie_time_delay = 3
    zombie_pushback = 2
    z_movement_speed = .25
    z_chase_distance = 200
    zombie_frozen = False
    zombie_freeze_time = 0
    zombies_killed = 0

    # Necromancer Variables
    necro_x, necro_y = 0, 0
    necromancer_hp_total = 200
    necromancer_summoning_timer = time.time()

    def draw_player(x, y):
        win.blit(character_img, (x, y))
        return

    def player_health_count(player_hp_total):
        # Fight Text
        player_hp_text = character_font.render("Player Health:" + str(player_hp_total), True, (0, 0, 0))
        win.blit(player_hp_text, (50, 50))
        return

    def player_mana_count(player_mana_total):
        # Fight Text
        player_mana_text = character_font.render("Player Mana:" + str(player_mana_total), True, (0, 0, 0))
        win.blit(player_mana_text, (50, 75))
        return

    def spawn_zombie(x, y, zombie_hp_total, zombie_frozen):
        # print("made it to function")
        # print("x is", x, 'y is', y)
        if zombie_hp_total >= 76:
            win.blit(zombie_img, (x, y))
        elif zombie_hp_total >= 51:
            win.blit(zombie75_img, (x, y))
        elif zombie_hp_total >= 26:
            win.blit(zombie50_img, (x, y))
        elif zombie_hp_total <= 25:
            win.blit(zombie25_img, (x, y))
        if zombie_frozen:
            win.blit(frozen_zombie, (x, y))
        return

    def player_zombie_distance(player_x, player_y, zx, zy):
        # TODO figure out why this number needs to be 25!! LOL
        # I honestly dont know why 25 works but it does.
        zx = zx + 25
        zy = zy + 25
        distance = math.sqrt((math.pow((zx + 8)-(player_x + 32), 2)) + (math.pow((zy + 8)-(player_y + 32), 2)))
        return distance

    """ For each type of road there is a different collision check we need to make, this function holds all the different 
    code we will need to check the players and zombies position against collision."""
    def tile_collision(player_x, player_y, rand_int, compatible_tile, draw_x, draw_y, character_pushback):

        if compatible_tile == boss_tile:
            player_x, player_y = boss_tile_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 5:
                player_x, player_y = north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 5:
                player_x, player_y = south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_3_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_3_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_3_north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == east_3_north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == east_3_south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == east_3_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_3_south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_3_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_3_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == west_3_north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == west_3_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == west_3_south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        return player_x, player_y

    """This function searches for new items on the tile the player is on and if they "make too much noise" a zombie will
    spawn on the tile they are searching on."""
    def search(player_x, player_y, health_potion_total, mana_potion_total, pistol_bullets, health_potion_found, mana_potion_found, bullets_found):
        dice_roll = random.randint(0, 5)
        if dice_roll == 0:
            # Spawn zombie
            if zombie_spawn.get("{0}, {1}".format(player_x, player_y)) != True:
                zombie_x.update({'{0}, {1}'.format(player_x, player_y): tile_x[player_x] + half_tile_size})
                zombie_y.update({'{0}, {1}'.format(player_x, player_y): tile_y[player_y] + half_tile_size})
                zombie_spawn.update({'{0}, {1}'.format(player_x, player_y): True})
                zombie_hp_total.update({'{0}, {1}'.format(player_x, player_y): 100})
        if dice_roll == 4 or dice_roll == 5:
            rand_item = random.randint(0, 2)
            if rand_item == 0:
                if health_potion_total <= 4:
                    health_potion_total += 1
                    health_potion_found = True
                else:
                    pass
            if rand_item == 1:
                if mana_potion_total <= 4:
                    mana_potion_total += 1
                    mana_potion_found = True
                else:
                    pass
            if rand_item == 2:
                if pistol_bullets <= 10:
                    pistol_bullets += 5
                    bullets_found = True
                else:
                    pass

        else:
            pass
        return health_potion_total, mana_potion_total, pistol_bullets, health_potion_found, mana_potion_found, bullets_found

    run = True
    while run:
        clock.tick(FPS)
        win.fill([124, 124, 124])

        # Directions text
        win.blit(arrow_keys_direction_text, (550, 50))
        win.blit(tab_direction_text, (600, 70))
        win.blit(search_direction_text, (600, 90))

        # Player Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            # key controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # print("Left Arrow Key Pressed.")
                    player_x_change = -player_vel
                if event.key == pygame.K_RIGHT:
                    # print("Right Arrow Key Pressed.")
                    player_x_change = player_vel
                if event.key == pygame.K_UP:
                    # print("Up Arrow Key Pressed.")
                    player_y_change = -player_vel
                if event.key == pygame.K_DOWN:
                    # print("Down Arrow Key Pressed.")
                    player_y_change = player_vel
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_TAB:
                    player_hp_total, player_mana_total, health_potion_total, mana_potion_total, pistol_bullets, zombie_frozen = invintory(
                        player_hp_total, player_mana_total, health_potion_total, mana_potion_total, pistol_bullets, zombie_frozen)
                    if zombie_frozen:
                        zombie_freeze_time = time.time()
                if event.key == pygame.K_RETURN:
                    health_potion_total, mana_potion_total, pistol_bullets, health_potion_found, mana_potion_found, bullets_found = search(current_player_quadrent[0], current_player_quadrent[1],
                                                                    health_potion_total, mana_potion_total, pistol_bullets, health_potion_found, mana_potion_found, bullets_found)
                    searching = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    # print("Left or Right arrow was released")
                    player_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # print("Left or Right arrow was released")
                    player_y_change = 0

        # Track which player_quadrent the player is in so we can draw tiles there.
        if player_x >= 0:
            quadrent_x = 0
        if player_x >= tile_1_0_x:
            quadrent_x = 1
        if player_x >= tile_2_0_x:
            quadrent_x = 2
        if player_x >= tile_3_0_x:
            quadrent_x = 3
        if player_x >= tile_4_0_x:
            quadrent_x = 4

        if player_y >= 0:
            quadrent_y = 0
        if player_y >= tile_0_1_y:
            quadrent_y = 1
        if player_y >= tile_0_2_y:
            quadrent_y = 2
        if player_y >= tile_0_3_y:
            quadrent_y = 3
        if player_y >= tile_0_4_y:
            quadrent_y = 4

        current_player_quadrent = [quadrent_x, quadrent_y]
        # print("player Quadrent: ", current_player_quadrent)

        """ Check the players position agianst each possible tile location if the player is in a tile location that is 
         not set, set the tile. if there is a zombie that is supposed to spawn there spawn it. Each time the player 
          enters a new tile location there is a chance that it will be the bosses lair."""
        for x in range(0, max_tiles):
            for y in range(0, max_tiles):
                if current_player_quadrent == [x, y]:
                    if tile_set.get("{0}, {1}".format(x, y)) != "set":
                        tile_sound.play()
                        boss_rand_int = random.randint(0, 5)
                        # print("x_y", x, y)
                        # print("dandy", "{0}, {1}".format(x, y))
                        draw_x.update({'{0}, {1}'.format(x, y): tile_x[x]})
                        draw_y.update({'{0}, {1}'.format(x, y): tile_y[y]})
                        tile_set.update({'{0}, {1}'.format(x, y): "set"})
                        if zombie_spawn.get("{0}, {1}".format(x, y)) != True:
                            if zombie_dice_roll.get("{0}, {1}".format(x, y)) == 5 or zombie_dice_roll.get("{0}, {1}".format(x, y)) == 6:
                                zombie_x.update({'{0}, {1}'.format(x, y): tile_x[x] + half_tile_size})
                                zombie_y.update({'{0}, {1}'.format(x, y): tile_y[y] + half_tile_size})
                                zombie_spawn.update({'{0}, {1}'.format(x, y): True})
                        # Center tile check
                        if current_player_quadrent == [2, 2]:
                            zombie_spawn.update({'{0}, {1}'.format(2, 2): False})
                            print("player started in 2, 2")
                        elif boss_rand_int == 0:
                            if boss_tile_set == "":
                                necro_loc_x, necro_loc_y = draw_x.get('{0}, {1}'.format(x, y)), draw_y.get('{0}, {1}'.format(x, y))
                                necro_x, necro_y = necro_loc_x + half_tile_size - 10, necro_loc_y + half_tile_size - 10
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): boss_tile})
                                boss_tile_set = "set"
                            # Inside tiles check
                            elif player_x >= tile_1_0_x and player_x < tile_4_0_x and player_y >= tile_0_1_y and player_y < tile_0_4_y:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, east_west_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, east_west_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, north_south_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_compatible_tiles})
                                elif previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, north_south_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_compatible_tiles})
                            # North 3 tile check
                            elif player_y < tile_0_1_y and player_x >= tile_1_0_x and player_x < tile_4_0_x:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_3_west_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_3_east_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_3_north_compatible_tiles})
                            # East 3 tile check
                            elif player_y >= tile_0_1_y and player_y < tile_0_4_y and player_x >= tile_4_0_x:
                                if previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_3_south_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_3_east_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_3_north_compatible_tiles})
                            # South 3 tile check
                            elif player_y >= tile_0_4_y and player_x >= tile_1_0_x and player_x < tile_4_0_x:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_3_west_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_3_east_compatible_tiles})
                                elif previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_3_south_compatible_tiles})
                            # West 3 tile check
                            elif player_y >= tile_0_1_y and player_y < tile_0_4_y and player_x < tile_1_0_x:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_3_west_compatible_tiles})
                                elif previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_3_south_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_3_north_compatible_tiles})
                            # North East Corner
                            elif player_y < tile_0_1_y and player_x >= tile_4_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): north_east_compatible_tiles})
                            # South East Corner
                            elif player_y >= tile_0_4_y and player_x >= tile_4_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): south_east_compatible_tiles})
                            # South West Corner
                            elif player_y >= tile_0_4_y and player_x < tile_1_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): south_west_compatible_tiles})
                            # North West Corner
                            elif player_y < tile_0_1_y and player_x < tile_1_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): north_west_compatible_tiles})
                        else:
                            # Inside tiles check
                            if player_x >= tile_1_0_x and player_x < tile_4_0_x and player_y >= tile_0_1_y and player_y < tile_0_4_y:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, east_west_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, east_west_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, north_south_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_compatible_tiles})
                                elif previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, north_south_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_compatible_tiles})
                            # North 3 tile check
                            elif player_y < tile_0_1_y and player_x >= tile_1_0_x and player_x < tile_4_0_x:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_3_west_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_3_east_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): north_3_north_compatible_tiles})
                            # East 3 tile check
                            elif player_y >= tile_0_1_y and player_y < tile_0_4_y and player_x >= tile_4_0_x:
                                if previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_3_south_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_3_east_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): east_3_north_compatible_tiles})
                            # South 3 tile check
                            elif player_y >= tile_0_4_y and player_x >= tile_1_0_x and player_x < tile_4_0_x:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_3_west_compatible_tiles})
                                elif previous_quadrent == [x - 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_3_east_compatible_tiles})
                                elif previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): south_3_south_compatible_tiles})
                            # West 3 tile check
                            elif player_y >= tile_0_1_y and player_y < tile_0_4_y and player_x < tile_1_0_x:
                                if previous_quadrent == [x + 1, y]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_3_west_compatible_tiles})
                                elif previous_quadrent == [x, y - 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_3_south_compatible_tiles})
                                elif previous_quadrent == [x, y + 1]:
                                    rand_int.update({'{0}, {1}'.format(x, y): random.randint(0, sides_num)})
                                    compatible_tile.update({'{0}, {1}'.format(x, y): west_3_north_compatible_tiles})
                            # North East Corner
                            elif player_y < tile_0_1_y and player_x >= tile_4_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): north_east_compatible_tiles})
                            # South East Corner
                            elif player_y >= tile_0_4_y and player_x >= tile_4_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): south_east_compatible_tiles})
                            # South West Corner
                            elif player_y >= tile_0_4_y and player_x < tile_1_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): south_west_compatible_tiles})
                            # North West Corner
                            elif player_y < tile_0_1_y and player_x < tile_1_0_x:
                                rand_int.update({'{0}, {1}'.format(x, y): 0})
                                compatible_tile.update({'{0}, {1}'.format(x, y): north_west_compatible_tiles})

                    else:
                        break

        # Draw the center tile and check to see if the player collides with the tile.
        player_x, player_y = tile_check(X, Y, player_x, player_y, player_pushback)
        win.blit(four_way_img, (X / 2 - 72, Y / 2 - 72))

        """check to see if there is a tile that is supposed to be on the location, if there is draw it and check to see
         if the player is colliding with the edges."""
        for x in range(0, max_tiles):
            for y in range(0, max_tiles):
                compat_tile = compatible_tile.get("{0}, {1}".format(x, y))
                rand_rand_int = rand_int.get("{0}, {1}".format(x, y))
                dx = draw_x.get("{0}, {1}".format(x, y))
                dy = draw_y.get("{0}, {1}".format(x, y))
                # print("compatable tiles: ", compat_tile, "rand int: ", rand_rand_int, "dx: ", dx, "dy: ", dy)
                try:
                    win.blit(compat_tile[rand_rand_int], (dx, dy))
                except TypeError:
                    # print("TypeError: drawing tiles")
                    pass
                # print(player_x, player_y)
                player_x, player_y = tile_collision(player_x, player_y, rand_rand_int, compat_tile, dx, dy, player_pushback)

        """This is all of the zombie movement and collision logic. Every few seconds the zombies pick a new direction
        to wander as long as the player is not too close to chase. This is where the zombies check to see if they 
        collide with walls or not."""
        zombie_movement_timer = (time.time() - start_of_game)
        for x in range(0, max_tiles):
            for y in range(0, max_tiles):
                z_hp = zombie_hp_total.get('{0}, {1}'.format(x, y))
                zs = zombie_spawn.get('{0}, {1}'.format(x, y))
                zx = zombie_x.get('{0}, {1}'.format(x, y))
                zy = zombie_y.get('{0}, {1}'.format(x, y))
                # print("type of zx", zx)
                # print("type of zy", zy)

                # Find what quadrent the zombie is in
                try:
                    if zx >= 0:
                        z_quadrent_x.update({'{0}, {1}'.format(x, y): 0})
                    if zx >= tile_1_0_x:
                        z_quadrent_x.update({'{0}, {1}'.format(x, y): 1})
                    if zx >= tile_2_0_x:
                        z_quadrent_x.update({'{0}, {1}'.format(x, y): 2})
                    if zx >= tile_3_0_x:
                        z_quadrent_x.update({'{0}, {1}'.format(x, y): 3})
                    if zx >= tile_4_0_x:
                        z_quadrent_x.update({'{0}, {1}'.format(x, y): 4})

                    if zy >= 0:
                        z_quadrent_y.update({'{0}, {1}'.format(x, y): 0})
                    if zy >= tile_0_1_y:
                        z_quadrent_y.update({'{0}, {1}'.format(x, y): 1})
                    if zy >= tile_0_2_y:
                        z_quadrent_y.update({'{0}, {1}'.format(x, y): 2})
                    if zy >= tile_0_3_y:
                        z_quadrent_y.update({'{0}, {1}'.format(x, y): 3})
                    if zy >= tile_0_4_y:
                        z_quadrent_y.update({'{0}, {1}'.format(x, y): 4})
                except TypeError:
                    pass

                # print(x, z_quadrent_x.get('{0}, {1}'.format(x, y)), y, z_quadrent_y.get('{0}, {1}'.format(x, y)))

                zxq = z_quadrent_x.get('{0}, {1}'.format(x, y))
                zyq = z_quadrent_y.get('{0}, {1}'.format(x, y))

                # Get the draw positions and other variables of the quadrent so we can draw the collision.
                zdx = draw_x.get("{0}, {1}".format(zxq, zyq))
                zdy = draw_y.get("{0}, {1}".format(zxq, zyq))
                # print("zdx: ", zdx, "zdy: ", zdy)
                zrand_rand_int = rand_int.get("{0}, {1}".format(zxq, zyq))
                zcompat_tile = compatible_tile.get("{0}, {1}".format(zxq, zyq))
                # print("rand int:", zrand_rand_int, "compatible tiles: ", zcompat_tile)

                try:
                    # Spawn the zombie if it exists.
                    if zs:
                        spawn_zombie(zx, zy, z_hp, zombie_frozen)
                except TypeError:
                    # print("TypeError: Drawing zombies")
                    pass

                zombie_frozen_timer = (time.time() - zombie_freeze_time)
                if zombie_frozen_timer <= 3:
                    if zombie_frozen:
                        pass

                else:
                    zombie_frozen = False
#TODO redo this code the zombie are slipping through cracks. make it so they reset or dont slip through cracks
# TODO figure out why there are invizable zombies?
                    if zombie_movement_timer >= zombie_time_delay:
                        # pick random direciton
                        zombie_rand_move.update({'{0}, {1}'.format(x, y): random.randint(0, 3)})

                    try:
                        if zombie_movement_timer <= zombie_time_delay:
                            # check to see if the zombie and player collide if they do activate the fight scean.
                            p_z_d = player_zombie_distance(player_x, player_y, zx, zy)
                            if p_z_d <= pz_collision:
                                bgm.stop()
                                combat_sound.play()
                                fade_to_black()
                                pygame.time.wait(100)
                                fight_music.play(-1)
                                # run the cut sceen
                                # print("player zombie collison")
                                player_x, player_y, player_hp_total, player_mana_total, zx, zy, zs, z_hp, zombies_killed, health_potion_total, \
                                mana_potion_total, pistol_bullets = fight(player_x, player_y, player_hp_total, player_mana_total, zx, zy, z_hp, zombies_killed, health_potion_total, mana_potion_total, pistol_bullets)
                                zombie_spawn.update({'{0}, {1}'.format(x, y): zs})
                                zombie_x.update({'{0}, {1}'.format(x, y): zx})
                                zombie_y.update({'{0}, {1}'.format(x, y): zy})
                                zombie_hp_total.update({'{0}, {1}'.format(x, y): z_hp})
                # We need to shut down player movement here otherwise when you exit the fight you will still be moving
                                player_x_change, player_y_change = 0, 0
                                fight_music.stop()
                                bgm.play(-1)

                            # Zombie moves in the direction of the player.
                            if p_z_d <= z_chase_distance:
                                if player_x > zx:
                                    zx += z_movement_speed
                                if player_x < zx:
                                    zx -= z_movement_speed
                                if player_y > zy:
                                    zy += z_movement_speed
                                if player_y < zy:
                                    zy -= z_movement_speed

                            # Other wise the zombie will move randomly.
                            else:
                                """Each if statement here checks to see if the tile in the direction the zombie is going 
                                to move is set or not. if it is then the zombie can move in that dircetion if not
                                then the zombie will stand still."""
                                if zombie_rand_move.get('{0}, {1}'.format(x, y)) == 0:
                                    if tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)), z_quadrent_y.get('{0}, {1}'.format(x, y)))) == "set":
                                        # print("x+1 set")
                                        zx += z_movement_speed
                                    else:
                                        zx = zx
                                        pass

                                if zombie_rand_move.get('{0}, {1}'.format(x, y)) == 1:
                                    if tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)), z_quadrent_y.get('{0}, {1}'.format(x, y)))) == "set":
                                        # print("x-1")
                                        zx -= z_movement_speed
                                    else:
                                        zx = zx
                                if zombie_rand_move.get('{0}, {1}'.format(x, y)) == 2:
                                    if tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)), z_quadrent_y.get('{0}, {1}'.format(x, y)))) == "set":
                                        # print("y+1")
                                        zy += z_movement_speed
                                    else:
                                        zy = zy
                                if zombie_rand_move.get('{0}, {1}'.format(x, y)) == 3:
                                    if tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)), z_quadrent_y.get('{0}, {1}'.format(x, y)))) == "set":
                                        # print("y-1")
                                        zy -= z_movement_speed
                                    else:
                                        zy = zy
                            # TODO figure out why this is here!
                            # if tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)), z_quadrent_y.get('{0}, {1}'.format(x, y)))) != "set":
                            #     if tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)) + 1, z_quadrent_y.get('{0}, {1}'.format(x, y)))) == "set":
                            #         zx += z_movement_speed
                            #     elif tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)) - 1, z_quadrent_y.get('{0}, {1}'.format(x, y)))) == "set":
                            #         zx -= z_movement_speed
                            #     elif tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)), z_quadrent_y.get('{0}, {1}'.format(x, y)) + 1)) == "set":
                            #         zy += z_movement_speed
                            #     elif tile_set.get('{0}, {1}'.format(z_quadrent_x.get('{0}, {1}'.format(x, y)), z_quadrent_y.get('{0}, {1}'.format(x, y)) - 1)) == "set":
                            #         zy -= z_movement_speed
                    except TypeError:
                        # print("TypeError: moving zombies")
                        pass

                    zombie_x.update({'{0}, {1}'.format(x, y): zx})
                    zombie_y.update({'{0}, {1}'.format(x, y): zy})
                    zx = zombie_x.get('{0}, {1}'.format(x, y))
                    zy = zombie_y.get('{0}, {1}'.format(x, y))

                    # This is where we test to see if the zombies collied with the walls.
                    try:
    # TODO zombies are running into isues with collison outside of the center tiles.
                        zx, zy = tile_collision(zx, zy, zrand_rand_int, zcompat_tile, zdx,
                                                                        zdy, zombie_pushback)
                        zx, zy = tile_check(X, Y, zx, zy, zombie_pushback)
                    except TypeError:
                        # print("TypeError: Drawing zombies")
                        pass

                    zombie_x.update({'{0}, {1}'.format(x, y): zx})
                    zombie_y.update({'{0}, {1}'.format(x, y): zy})
                    zx = zombie_x.get('{0}, {1}'.format(x, y))
                    zy = zombie_y.get('{0}, {1}'.format(x, y))

                    try:
                        if zx <= tile_0_0_x:
                            zombie_x.update({'{0}, {1}'.format(x, y): zx + zombie_pushback})
                        if zx >= tile_5_0_x:
                            zombie_x.update({'{0}, {1}'.format(x, y): zx - zombie_pushback})
                        if zy <= tile_0_0_y:
                            zombie_y.update({'{0}, {1}'.format(x, y): zy + zombie_pushback})
                        if zy >= tile_0_5_y:
                            zombie_y.update({'{0}, {1}'.format(x, y): zy - zombie_pushback})
                    except TypeError:
                        # print("TypeError: zombie bounderies")
                        pass

        # Necromancer logic.
        if boss_tile_set == "set":
            if necromancer_hp_total >= 151:
                win.blit(necromancer, (necro_x, necro_y))
            elif necromancer_hp_total >= 101:
                win.blit(necromancer75, (necro_x, necro_y))
            elif necromancer_hp_total >= 51:
                win.blit(necromancer50, (necro_x, necro_y))
            elif necromancer_hp_total <= 50:
                win.blit(necromancer25, (necro_x, necro_y))

            # Check necromancer distance from player then check collision.
            necro_player_distance = player_zombie_distance(player_x, player_y, necro_x, necro_y)
            if necro_player_distance <= pz_collision:
                # run the cut sceen
                # print("player necromancer collison")
                bgm.stop()
                combat_sound.play()
                fade_to_black()
                pygame.time.wait(100)
                boss_fight.play(-1)
                player_x, player_y, player_hp_total, player_mana_total, necro_x, necro_y, necromancer_hp_total,\
                health_potion_total, mana_potion_total, pistol_bullets = boss_fight(player_x, player_y,
                player_hp_total, player_mana_total, player_x_change, player_y_change, necro_x, necro_y,
                                        necromancer_hp_total, health_potion_total, mana_potion_total, pistol_bullets)
                player_x_change, player_y_change = 0, 0
                boss_fight.stop()
                bgm.play(-1)
            # If the necromancer dies exit the main game loop
            if necromancer_hp_total <= 0:
                # print('congrats you servived.')
                run = False
            """the necromancer summoms zombies about every 10 seconds, he only spawns zombies from tiles that have
            a zombie to spawn"""
            necromancer_summoning_stopper = (time.time() - necromancer_summoning_timer)
            if necromancer_summoning_stopper >= 10:
                for x in range(0, max_tiles):
                    necromancer_summoning_stopper = (time.time() - necromancer_summoning_timer)
                    if necromancer_summoning_stopper < 10:
                        break
                    for y in range(0, max_tiles):
                        if tile_set.get('{0}, {1}'.format(x, y)) == 'set':
                            if zombie_spawn.get('{0}, {1}'.format(x, y)) != True:
                                zombie_x.update({'{0}, {1}'.format(x, y): tile_x[x] + half_tile_size})
                                zombie_y.update({'{0}, {1}'.format(x, y): tile_y[y] + half_tile_size})
                                zombie_spawn.update({'{0}, {1}'.format(x, y): True})
                                necromancer_summoning_timer = time.time()
                                necromancer_summoning_stopper = (time.time() - necromancer_summoning_timer)
                                if necromancer_summoning_stopper <= 5:
                                    break

        # Restart the zombie movment timer
        if zombie_movement_timer >= zombie_time_delay:
            start_of_game = time.time()

        # outer bounds player check.
        if player_x <= tile_0_0_x:
            player_x += player_pushback
        if player_x >= tile_5_0_x:
            player_x -= player_pushback
        if player_y <= tile_0_0_y:
            player_y += player_pushback
        if player_y >= tile_0_5_y:
            player_y -= player_pushback

        # if the player dies exit the main game loop
        if player_hp_total <= 0:
            run = False
            break

        # place this at the end because if it were anywhere else it would update too soon.
        previous_quadrent = current_player_quadrent

        # Draw the player after they move.
        player_x += player_x_change
        player_y += player_y_change
        # Draw player information
        player_health_count(player_hp_total)
        player_mana_count(player_mana_total)
        draw_player(player_x, player_y)

        # text that is delayed for searching.
        if searching:
            win.blit(searching_text, (375, 375))
            pygame.display.update()
            pygame.time.wait(1000)
            searching = False
        if health_potion_found:
            win.blit(found_health_potion, (400, 475))
            pygame.display.update()
            pygame.time.wait(1000)
            health_potion_found = False
        if mana_potion_found:
            win.blit(found_mana_potion, (400, 475))
            pygame.display.update()
            pygame.time.wait(1000)
            mana_potion_found = False
        if bullets_found:
            win.blit(found_bullets, (400, 475))
            pygame.display.update()
            pygame.time.wait(1000)
            bullets_found = False

        pygame.display.update()
    return player_hp_total, necromancer_hp_total, zombies_killed


def invintory(player_hp_total, player_mana_total, health_potion_total, mana_potion_total, pistol_bullets, zombies_frozen):
    # print("you are dead.")
    pygame.init()

    win = pygame.display.set_mode((1000, 1000))

    X, Y = pygame.display.get_surface().get_size()
    # print("Canvas size: ", X, Y)
    print("invintory screen")

    #SFX
    freeze_spell_sfx = mixer.Sound('SFX/freeze_spell.wav')
    health_potion_sfx = mixer.Sound('SFX/health_potion.wav')
    mana_potion_sfx = mixer.Sound('SFX/mana_potion.wav')

    # IMG variables
    invintory_menu_bg = pygame.image.load('Art/invintory_background.png')
    health_potion_img = pygame.image.load('Art/health_potion.png')
    mana_potion_img = pygame.image.load('Art/mana_potion.png')
    invintory_selector_img = pygame.image.load('Art/invintory_selector.png')
    pistol_img = pygame.image.load('Art/pistol.png')
    freeze_spell_img = pygame.image.load('Art/freeze_spell.png')


    # Fonts and Texts
    player_hp_font = pygame.font.Font('freesansbold.ttf', 20)
    health_potion_font = pygame.font.Font('freesansbold.ttf', 20)
    mana_potion_font = pygame.font.Font('freesansbold.ttf', 20)
    command_font = pygame.font.Font('freesansbold.ttf', 20)
    title_font = pygame.font.Font('freesansbold.ttf', 50)
    items_spells_title = title_font.render("Items/Spells", True, (0, 0, 0))
    command = command_font.render("press tab to return to game", True, (0, 0, 0))
    health_potion_name = command_font.render("Health Potion", True, (0, 0, 0))
    mana_potion_name = command_font.render("Mana Potion", True, (0, 0, 0))
    pistol_name_text = command_font.render("Pistol Bullets", True, (0, 0, 0))
    freeze_spell_name_text = command_font.render("Freeze Zombies", True, (0, 0, 0))
    freeze_spell_cost = command_font.render("50MP", True, (0, 0, 0))

    # Menu Variables
    selector_x, selector_y = 220, 215
    column_left_x = 225
    column_center_x = 425
    column_right_x = 625
    row_first_y = 225
    row_second_y = 325

    run = True
    while run:
        # Menu text that changes
        player_hp = player_hp_font.render("Player Health:" + str(player_hp_total), True, (0, 0, 0))
        player_mana = player_hp_font.render("Player Mana:" + str(player_mana_total), True, (0, 0, 0))
        health_potion_text = health_potion_font.render(" : " + str(health_potion_total), True, (0, 0, 0))
        mana_potion_text = mana_potion_font.render(" : " + str(mana_potion_total), True, (0, 0, 0))
        pistol_text = mana_potion_font.render(" : " + str(pistol_bullets), True, (0, 0, 0))

        # Draw
        win.fill([124, 124, 124])
        win.blit(player_hp, (50, 50))
        win.blit(player_mana, (50, 75))

        win.blit(command, (700, 50))
        win.blit(invintory_menu_bg, (125, 125))
        win.blit(items_spells_title, (350, 140))

        win.blit(health_potion_name, (column_left_x, 195))
        win.blit(health_potion_img, (column_left_x, row_first_y))
        win.blit(health_potion_text, (275, 250))

        win.blit(mana_potion_name, (column_left_x, 295))
        win.blit(mana_potion_img, (column_left_x, row_second_y))
        win.blit(mana_potion_text, (275, 350))

        win.blit(pistol_name_text, (column_center_x, 195))
        win.blit(pistol_img, (column_center_x, row_first_y))
        win.blit(pistol_text, (465, 245))

        win.blit(freeze_spell_name_text, (column_right_x, 195))
        win.blit(freeze_spell_img, (column_right_x, row_first_y))
        win.blit(freeze_spell_cost, (column_right_x + 60, 245))

        win.blit(invintory_selector_img, (selector_x, selector_y))

        # Player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    run = False
                    break
                if event.key == pygame.K_DOWN:
                    selector_y += 100
                if event.key == pygame.K_UP:
                    selector_y -= 100
                if event.key == pygame.K_LEFT:
                    selector_x -= 200
                if event.key == pygame.K_RIGHT:
                    selector_x += 200
                if event.key == pygame.K_RETURN:
                    if selector_x == 220 and selector_y == 215:
                        if health_potion_total > 0:
                            health_potion_sfx.play()
                            health_potion_total -= 1
                            player_hp_total += 50
                        else:
                            pass
                    if selector_x == 220 and selector_y == 315:
                        if mana_potion_total > 0:
                            mana_potion_sfx.play()
                            mana_potion_total -= 1
                            player_mana_total += 50
                        else:
                            pass
                    if selector_x == 620 and selector_y == 215:
                        if not zombies_frozen:
                            if player_mana_total >= 50:
                                freeze_spell_sfx.play()
                                player_mana_total -= 50
                                zombies_frozen = True
                            else:
                                pass

        # Selector boundries that keep it in the menu
        if selector_y >= 750:
            selector_y = 215
        if selector_y <= 214:
            selector_y = 715
        if selector_x >= 621:
            selector_x = 220
        if selector_x <= 219:
            selector_x = 620

        # print('selector x,y pos', selector_x, selector_y)
        pygame.display.update()
    return player_hp_total, player_mana_total, health_potion_total, mana_potion_total, pistol_bullets, zombies_frozen


"""This page holds all of the logic for the collisions for each tile type."""

colision_measurment = 14
tile_size = 143
half_tile_size = 72


def tile_check(X, Y, initial_player_x, initial_player_y, player_pushback):
    """we are using 14 as the colision distance because the buildings are 24 px away and the player has a 20 px wide
    body so we need to subtract 10 from the distance the buildings are drawn to get an accurate collision."""
    # we are adding 10 to the players x and y to find the players center.
    p_center_x, p_center_y = initial_player_x + 10, initial_player_y + 10
    x_origonal, y_origonal = initial_player_x, initial_player_y
    player_final_x, player_final_y = initial_player_x, initial_player_y
    tile_x, tile_y = (X / 2) - 72, (Y / 2) - 72

    # Collision check for inside of the starting tile.
    if p_center_x >= tile_x and p_center_x <= ((X / 2) + 72) and p_center_y >= tile_y and p_center_y <= ((Y / 2) + 72):
        # print("in the center tile")
        # Check to see if the player runs into any buildings.
        # print("top left of the center")
        if p_center_x <= ((X / 2) - colision_measurment) and p_center_y <= ((Y / 2) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal + player_pushback
        # print("bottom left of the center")
        elif p_center_x <= ((X / 2) - colision_measurment) and p_center_y >= ((Y / 2) + colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal - player_pushback
        # print("top right of the center")
        elif p_center_x >= ((X / 2) + colision_measurment) and p_center_y <= ((Y / 2) - colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal + player_pushback
        # print("bottom right of the center")
        elif p_center_x >= ((X / 2) + colision_measurment) and p_center_y >= ((Y / 2) + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal - player_pushback
    return player_final_x, player_final_y


def east_west_north_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_ewnc_x, p_ewnc_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the east west north tile.
    if p_ewnc_x >= tile_x and p_ewnc_x <= tile_x + tile_size and p_ewnc_y >= tile_y and p_ewnc_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top left of the center
        if p_ewnc_x <= ((tile_x + half_tile_size) - colision_measurment) and p_ewnc_y <= ((tile_y + half_tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal + player_pushback
        # bottom
        elif p_ewnc_y >= ((tile_y + half_tile_size) + colision_measurment) and p_ewnc_y <= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
        # bottom bottom
        elif p_ewnc_y >= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # top right of the center
        elif p_ewnc_x >= ((tile_x + half_tile_size) + colision_measurment) and p_ewnc_y <= ((tile_y + half_tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal + player_pushback
    return player_final_x, player_final_y


def east_west_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_ewc_x, p_ewc_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the east west tile.
    if p_ewc_x >= tile_x and p_ewc_x <= tile_x + tile_size and p_ewc_y >= tile_y and p_ewc_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top
        if p_ewc_y <= ((tile_y + half_tile_size) - colision_measurment) and p_ewc_y >= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # bottom
        elif p_ewc_y >= ((tile_y + half_tile_size) + colision_measurment) and p_ewc_y <= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
        # bottom bottom
        elif p_ewc_y >= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # top top
        elif p_ewc_y <= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
    return player_final_x, player_final_y


def east_west_south_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_ewsc_x, p_ewsc_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the east west south tile.
    if p_ewsc_x >= tile_x and p_ewsc_x <= tile_x + tile_size and p_ewsc_y >= tile_y and p_ewsc_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top
        if p_ewsc_y <= ((tile_y + half_tile_size) - colision_measurment) and p_ewsc_y >= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # bottom right of the center
        elif p_ewsc_x >= ((tile_x + half_tile_size) + colision_measurment) and p_ewsc_y >= ((tile_y + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal - player_pushback
        # bottom left of the center
        elif p_ewsc_x <= ((tile_x + half_tile_size) - colision_measurment) and p_ewsc_y >= ((tile_y + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal - player_pushback
        # top top
        elif p_ewsc_y <= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
    return player_final_x, player_final_y


def north_south_east_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_nsec_x, p_nsec_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the north south east tile.
    if p_nsec_x >= tile_x and p_nsec_x <= tile_x + tile_size and p_nsec_y >= tile_y and p_nsec_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top right of the center
        if p_nsec_y <= ((tile_y + half_tile_size) - colision_measurment) and p_nsec_x >= ((tile_x + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal + player_pushback
        # bottom right of the center
        elif p_nsec_x >= ((tile_x + half_tile_size) + colision_measurment) and p_nsec_y >= ((tile_y + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal - player_pushback
        # left of the center
        elif p_nsec_x <= ((tile_x + half_tile_size) - colision_measurment) and p_nsec_x >= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
        # left left
        elif p_nsec_x <= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
    return player_final_x, player_final_y


def north_south_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_nsc_x, p_nsc_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the north south tile.
    if p_nsc_x >= tile_x and p_nsc_x <= tile_x + tile_size and p_nsc_y >= tile_y and p_nsc_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # right of the center
        if p_nsc_x >= ((tile_x + half_tile_size) + colision_measurment) and p_nsc_x <= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
        # left of the center
        elif p_nsc_x <= ((tile_x + half_tile_size) - colision_measurment) and p_nsc_x >= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
        # left left
        elif p_nsc_x <= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
        # right right
        elif p_nsc_x >= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
    return player_final_x, player_final_y


def north_south_west_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_nswc_x, p_nswc_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the north south west tile.
    if p_nswc_x >= tile_x and p_nswc_x <= tile_x + tile_size and p_nswc_y >= tile_y and p_nswc_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top left of the center
        if p_nswc_y <= ((tile_y + half_tile_size) - colision_measurment) and p_nswc_x <= ((tile_x + half_tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal + player_pushback
            # bottom left of the center
        elif p_nswc_x <= ((tile_x + half_tile_size) - colision_measurment) and p_nswc_y >= ((tile_y + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal - player_pushback
            # right of the center
        elif p_nswc_x >= ((tile_x + half_tile_size) + colision_measurment) and p_nswc_x <= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
            # right right
        elif p_nswc_x >= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
    return player_final_x, player_final_y


# TODO There is a bug where you can go through the walls on the corners if you try hard enough. I think its because the
# wall are triggered one at a time so it only registers one wall and not the other.
def north_west_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_nwc_x, p_nwc_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the north west tile.
    if p_nwc_x >= tile_x and p_nwc_x <= tile_x + tile_size and p_nwc_y >= tile_y and p_nwc_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top left of the center
        if p_nwc_y <= ((tile_y + half_tile_size) - colision_measurment) and p_nwc_x <= ((tile_x + half_tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal + player_pushback
        # bottom
        elif p_nwc_y >= ((tile_y + half_tile_size) + colision_measurment) and p_nwc_y <= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
        # bottom bottom
        elif p_nwc_y >= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # right
        elif p_nwc_x >= ((tile_x + half_tile_size) + colision_measurment) and p_nwc_x <= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
        # right right
        elif p_nwc_x >= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
    return player_final_x, player_final_y


def north_east_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_nec_x, p_nec_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the north east tile.
    if p_nec_x >= tile_x and p_nec_x <= tile_x + tile_size and p_nec_y >= tile_y and p_nec_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top right of the center
        if p_nec_y <= ((tile_y + half_tile_size) - colision_measurment) and p_nec_x >= ((tile_x + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal + player_pushback
        # print("bottom")
        elif p_nec_y >= ((tile_y + half_tile_size) + colision_measurment) and p_nec_y <= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
        # print("bottom bottom")
        elif p_nec_y >= ((tile_y + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # print("left")
        elif p_nec_x <= ((tile_x + half_tile_size) - colision_measurment) and p_nec_x >= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
        # print("left left")
        elif p_nec_x <= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
    return player_final_x, player_final_y


def south_east_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_sec_x, p_sec_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the east west north tile.
    if p_sec_x >= tile_x and p_sec_x <= tile_x + tile_size and p_sec_y >= tile_y and p_sec_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # bottom right of the center
        if p_sec_y >= ((tile_y + half_tile_size) + colision_measurment) and p_sec_x >= ((tile_x + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal - player_pushback
        # top
        elif p_sec_y <= ((tile_y + half_tile_size) - colision_measurment) and p_sec_y >= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # top top
        elif p_sec_y <= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
        # left
        elif p_sec_x <= ((tile_x + half_tile_size) - colision_measurment) and p_sec_x >= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
        # left left
        elif p_sec_x <= (tile_x + colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
    return player_final_x, player_final_y


def south_west_collision_check(player_x, player_y, tile_x, tile_y, player_pushback):
    p_sec_x, p_sec_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the south west tile.
    if p_sec_x >= tile_x and p_sec_x <= tile_x + tile_size and p_sec_y >= tile_y and p_sec_y <= tile_y + tile_size:
        # Check to see if the player runs into any buildings.
        # bottom left of the center
        if p_sec_y >= ((tile_y + half_tile_size) + colision_measurment) and p_sec_x <= ((tile_x + half_tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal - player_pushback
        # top
        elif p_sec_y <= ((tile_y + half_tile_size) - colision_measurment) and p_sec_y >= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal + player_pushback
        # top top
        elif p_sec_y <= (tile_y + colision_measurment):
            player_final_x, player_final_y = x_origonal, y_origonal - player_pushback
        # right
        elif p_sec_x >= ((tile_x + half_tile_size) + colision_measurment) and p_sec_x <= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal - player_pushback, y_origonal
        # right right
        elif p_sec_x >= ((tile_x + tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + player_pushback, y_origonal
    return player_final_x, player_final_y


def boss_tile_check(player_x, player_y, draw_x, draw_y, character_pushback):
    """we are using 14 as the colision distance because the buildings are 24 px away and the player has a 20 px wide
    body so we need to subtract 10 from the distance the buildings are drawn to get an accurate collision."""
    # we are adding 10 to the players x and y to find the players center.
    p_center_x, p_center_y = player_x + 10, player_y + 10
    player_final_x, player_final_y = player_x, player_y
    x_origonal, y_origonal = player_x, player_y

    # Collision check for inside of the boss tile.
    if p_center_x >= draw_x and p_center_x <= draw_x + tile_size and p_center_y >= draw_y and p_center_y <= draw_y + tile_size:
        # Check to see if the player runs into any buildings.
        # top left of the center
        if p_center_x <= ((draw_x + half_tile_size) - colision_measurment) and p_center_y <= ((draw_y + half_tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal + character_pushback, y_origonal + character_pushback
        # bottom left of the center
        elif p_center_x <= ((draw_x + half_tile_size) - colision_measurment) and p_center_y >= ((draw_y + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal + character_pushback, y_origonal - character_pushback
        # top right of the center
        elif p_center_x >= ((draw_x + half_tile_size) + colision_measurment) and p_center_y <= ((draw_y + half_tile_size) - colision_measurment):
            player_final_x, player_final_y = x_origonal - character_pushback, y_origonal + character_pushback
        # bottom right of the center
        elif p_center_x >= ((draw_x + half_tile_size) + colision_measurment) and p_center_y >= ((draw_y + half_tile_size) + colision_measurment):
            player_final_x, player_final_y = x_origonal - character_pushback, y_origonal - character_pushback
    return player_final_x, player_final_y


"""This page is almost a copy of the page from the fight_screen except that it is made for the necromancer instead. 
we ran into a glitch where when the player would try to run from the necromancer they would end up outside of the map 
and would be forced back into the necromancer We got around this by having the player return to the start of the game 
when they run from the necromancer. I would like to go back and fix this later but the logic illudes me for now."""


def boss_fight(player_x, player_y, player_hp_total, player_mana_total, player_val_x, player_val_y, necro_x, necro_y, necromancer_hp_total, health_potion_total, mana_potion_total, pistol_bullets):
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 120

    win = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Zombie City")
    icon = pygame.image.load('Art/four_way_stop.png')
    pygame.display.set_icon(icon)

    #SFX
    fist_sfx = mixer.Sound('SFX/fist_hit.wav')
    pistol_sfx = mixer.Sound('SFX/pistol.wav')

    X, Y = pygame.display.get_surface().get_size()
    # print("Title Screen Canvas size: ", X, Y)

    # images
    character_img = pygame.image.load('Art/characterFull.png')
    necromancer_img = pygame.image.load('Art/necromancerFull.png')
    necromancer75_img = pygame.image.load('Art/necromancerFull75.png')
    necromancer50_img = pygame.image.load('Art/necromancerFull50.png')
    necromancer25_img = pygame.image.load('Art/necromancerFull25.png')
    menu_img = pygame.image.load('Art/fight_bar.png')
    selector_img = pygame.image.load('Art/selector.png')
    hitmarker = pygame.image.load('Art/hitmarker.png')
    health_potion_img = pygame.image.load('Art/health_potion.png')
    mana_potion_img = pygame.image.load('Art/mana_potion.png')
    invintory_selector_img = pygame.image.load('Art/invintory_selector.png')
    pistol_img = pygame.image.load('Art/pistol.png')

    # Fight Menu Fonts
    character_font = pygame.font.Font('freesansbold.ttf', 20)
    menu_font = pygame.font.Font('freesansbold.ttf', 40)

    # Main Menu Text
    attack_button_text = menu_font.render("Attack", True, (33, 151, 68))
    run_button_text = menu_font.render("Run", True, (33, 151, 68))
    item_button_text = menu_font.render("Item", True, (33, 151, 68))
    magic_button_text = menu_font.render("Magic", True, (33, 151, 68))

    # Attack Menu Text
    fists_button_text = menu_font.render("Fists", True, (33, 151, 68))
    pistol_button_text = menu_font.render("Pistol", True, (33, 151, 68))

    # Item Menu Text
    health_potion_font = pygame.font.Font('freesansbold.ttf', 20)
    mana_potion_font = pygame.font.Font('freesansbold.ttf', 20)

    # Magic Menu Text
    none_available_button_text = menu_font.render("None Available", True, (33, 151, 68))

    # Combat Variables
        # Player Variables
    player_fists_dmg = 10
    player_pistol_dmg = 20
    player_turn = True
    player_attack_hits = False
    fists_attack_hits = False
    pistol_attack_hits = False
        # Necromancer Variables
    necro_dmg = 10
    necro_attack_hits = False

    # return variables
    # Right now we arnt using this because of the glitch.
    player_necro_disengague = 30

    # Menu Variables
    selecter_on_row_one_y = 530
    selecter_on_row_two_y = 590
    menu_left_column_x = 150
    menu_right_column_x = 450
    selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
    main_menu = True
    attack_menu = False
    item_menu = False
    magic_menu = False

    def player_health_count():
        # Fight Text
        player_hp_text = character_font.render("Player Health:" + str(player_hp_total), True, (0, 0, 0))
        win.blit(player_hp_text, (50, 250))
        return

    def player_mana_count():
        # Fight Text
        player_mana_text = character_font.render("Player Mana:" + str(player_mana_total), True, (0, 0, 0))
        win.blit(player_mana_text, (50, 275))
        return

    def zombie_health_count():
        necromancer_hp_text = character_font.render("Necromancer Health:" + str(necromancer_hp_total), True, (0, 0, 0))
        win.blit(necromancer_hp_text, ((X / 2) + 150, 25))
        return

    run = True
    while run:
        # Item Menu Text Recurring
        health_potion_text = health_potion_font.render(" = " + str(health_potion_total), True, (0, 0, 0))
        mana_potion_text = mana_potion_font.render(" : " + str(mana_potion_total), True, (0, 0, 0))

        # Attack Menu Text
        pistol_button_text = menu_font.render("Pistol: " + str(pistol_bullets), True, (33, 151, 68))

        clock.tick(FPS)
        win.fill([124, 124, 124])

        # Main images for the fight screen
        win.blit(character_img, (50, (Y / 2) - 200))
        if necromancer_hp_total >= 151:
            win.blit(necromancer_img, ((X / 2) + 150, 50))
        elif necromancer_hp_total >= 101:
            win.blit(necromancer75_img, ((X / 2) + 150, 50))
        elif necromancer_hp_total >= 51:
            win.blit(necromancer50_img, ((X / 2) + 150, 50))
        elif necromancer_hp_total <= 50:
            win.blit(necromancer25_img, ((X / 2) + 150, 50))
        win.blit(menu_img, (150, 525))

        # Text for the fight screen
        win.blit(attack_button_text, (160, 535))
        win.blit(run_button_text, (160, 595))
        win.blit(item_button_text, (510, 535))
        win.blit(magic_button_text, (510, 595))

        if player_turn:
            # print("player Turn")
            # Player Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        sys.exit()
                    # Attack Menue ----
                    if attack_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_one_y:
                                player_attack_hits = True
                                fists_attack_hits = True
                                player_turn = False
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_two_y:
                                if pistol_bullets > 0:
                                    player_attack_hits = True
                                    pistol_attack_hits = True
                                    player_turn = False
                                else:
                                    pass
                        if event.key == pygame.K_TAB:
                            selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
                            attack_menu = False
                            main_menu = True
                    # Item Menu -----
                    if item_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_one_y:
                                if health_potion_total > 0:
                                    player_hp_total += 50
                                    health_potion_total -= 1
                                    player_turn = False
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_two_y:
                                if mana_potion_total > 0:
                                    player_mana_total += 50
                                    mana_potion_total -= 1
                                    player_turn = False
                        if event.key == pygame.K_TAB:
                            selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
                            item_menu = False
                            main_menu = True
                    # Magic Menu -----
                    if magic_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            pass
                        if event.key == pygame.K_TAB:
                            selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
                            magic_menu = False
                            main_menu = True
                    # Main Menu ----
                    if main_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_two_y:
# TODO fix the bug that when the player runs at the necromancer from an x and y direction they cant run away
#                                 if player_val_x < 0 and player_val_y == 0:
#                                     player_x += player_necro_disengague
#                                 if player_val_x > 0 and player_val_y == 0:
#                                     player_x -= player_necro_disengague
#                                 if player_val_y < 0 and player_val_x == 0:
#                                     player_y += player_necro_disengague
#                                 if player_val_y > 0 and player_val_x == 0:
#                                     player_y += player_necro_disengague
#                                 if player_val_x < 0 and player_val_y < 0 and player_x > necro_x and player_y < necro_y:
#                                     player_x += player_necro_disengague
#                                     player_y += player_necro_disengague
#                                 if player_val_x < 0 and player_val_y > 0 and player_x > necro_x and player_y > necro_y:
#                                     player_x += player_necro_disengague
#                                     player_y -= player_necro_disengague
#                                 if player_val_y < 0 and player_val_x > 0 and player_x > necro_x and player_y > necro_y:
#                                     player_x -= player_necro_disengague
#                                     player_y += player_necro_disengague
#                                 if player_val_y < 0 and player_val_x < 0 and player_x < necro_x and player_y > necro_y:
#                                     player_x += player_necro_disengague
#                                     player_y += player_necro_disengague
#                                 if player_val_x > 0 and player_val_y > 0 and player_x < necro_x and player_y > necro_y:
#                                     player_x -= player_necro_disengague
#                                     player_y -= player_necro_disengague
#                                 if player_val_x > 0 and player_val_y < 0 and player_x < necro_x and player_y < necro_y:
#                                     player_x -= player_necro_disengague
#                                     player_y += player_necro_disengague
#                                 if player_val_y > 0 and player_val_x < 0 and player_x < necro_x and player_y < necro_y:
#                                     player_x += player_necro_disengague
#                                     player_y -= player_necro_disengague
#                                 if player_val_y > 0 and player_val_x > 0 and player_x > necro_x and player_y < necro_y:
#                                     player_x -= player_necro_disengague
#                                     player_y -= player_necro_disengague
                                player_x = X/2 - 10
                                player_y = Y/2 - 10
                                run = False
                                break
                            if selector_x == menu_right_column_x and selector_y == selecter_on_row_two_y:
                                magic_menu = True
                                main_menu = False
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_one_y:
                                attack_menu = True
                                main_menu = False
                            if selector_x == menu_right_column_x and selector_y == selecter_on_row_one_y:
                                item_menu = True
                                main_menu = False



        # This is the new menu that pops up after the player selects the attack option
        # maby make the menu pop out to the right so we can use a diffrent x an y value for events.
        if main_menu:
            # Selector
            win.blit(selector_img, (selector_x, selector_y))
        if attack_menu:
            win.blit(menu_img, (150, 525))
            win.blit(fists_button_text, (menu_left_column_x + 10, 535))
            win.blit(pistol_button_text, (menu_left_column_x + 10, 595))
            win.blit(selector_img, (selector_x, selector_y))
        if item_menu:
            win.blit(menu_img, (150, 525))
            win.blit(health_potion_img, (menu_left_column_x + 30, 535))
            win.blit(health_potion_text, (menu_left_column_x + 100, 555))
            win.blit(mana_potion_img, (menu_left_column_x + 30, 600))
            win.blit(mana_potion_text, (menu_left_column_x + 100, 620))
            win.blit(invintory_selector_img, (selector_x, selector_y))
        if magic_menu:
            win.blit(menu_img, (150, 525))
            win.blit(none_available_button_text, (menu_left_column_x + 10, 535))
            win.blit(selector_img, (selector_x, selector_y))

        if player_hp_total <= 0:
            run = False
            break

        # Graphics for hit markers
        if player_attack_hits:
            if fists_attack_hits:
                fist_sfx.play()
                necromancer_hp_total -= player_fists_dmg
                win.blit(hitmarker, (650, 150))
                zombie_health_count()
                player_health_count()
                pygame.display.update()
                pygame.time.wait(500)
                fists_attack_hits = False
                player_attack_hits = False
            if pistol_attack_hits:
                pistol_sfx.play()
                necromancer_hp_total -= player_pistol_dmg
                win.blit(hitmarker, (650, 50))
                win.blit(hitmarker, (700, 100))
                zombie_health_count()
                player_health_count()
                pygame.display.update()
                pygame.time.wait(500)
                pistol_bullets -= 1
                pistol_attack_hits = False
                player_attack_hits = False

        if necromancer_hp_total > 0:
            if player_turn == False:
                # print("zombie turn")
                necro_attack_hits = True
                player_turn = True

        if necromancer_hp_total <= 0:
            necro_attack_hits = False
            necro_x, necro_y = 0, 0
            run = False
            break

        if necro_attack_hits:
            fist_sfx.play()
            player_hp_total -= necro_dmg
            win.blit(hitmarker, (100, 300))
            pygame.display.update()
            pygame.time.wait(500)
            necro_attack_hits = False

        if selector_x <= 100:
            selector_x = 450
        if selector_x >= 500:
            selector_x = 150
        if selector_y < selecter_on_row_one_y:
            selector_y = selecter_on_row_two_y
        if selector_y > selecter_on_row_two_y:
            selector_y = selecter_on_row_one_y

        # print(selector_x, selector_y)
        player_health_count()
        player_mana_count()
        zombie_health_count()
        pygame.display.update()
    return player_x, player_y, player_hp_total, player_mana_total, necro_x, necro_y, necromancer_hp_total, health_potion_total, mana_potion_total, pistol_bullets


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


def fight(player_x, player_y, player_hp_total, player_mana_total, zx, zy, zombie_hp_total, zombies_killed, health_potion_total, mana_potion_total, pistol_bullets):
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 120

    win = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Zombie City")
    icon = pygame.image.load('Art/four_way_stop.png')
    pygame.display.set_icon(icon)

    X, Y = pygame.display.get_surface().get_size()
    # print("Title Screen Canvas size: ", X, Y)

    # SFX
    fist_sfx = mixer.Sound('SFX/fist_hit.wav')
    pistol_sfx = mixer.Sound('SFX/pistol.wav')

    # images
    character_img = pygame.image.load('Art/characterFull.png')
    zombie_img = pygame.image.load('Art/zombieFull.png')
    zombie75_img = pygame.image.load('Art/zombieFull75.png')
    zombie50_img = pygame.image.load('Art/zombieFull50.png')
    zombie25_img = pygame.image.load('Art/zombieFull25.png')
    menu_img = pygame.image.load('Art/fight_bar.png')
    selector_img = pygame.image.load('Art/selector.png')
    hitmarker = pygame.image.load('Art/hitmarker.png')
    health_potion_img = pygame.image.load('Art/health_potion.png')
    mana_potion_img = pygame.image.load('Art/mana_potion.png')
    invintory_selector_img = pygame.image.load('Art/invintory_selector.png')
    pistol_img = pygame.image.load('Art/pistol.png')

    # Fight Menu Fonts
    character_font = pygame.font.Font('freesansbold.ttf', 20)
    menu_font = pygame.font.Font('freesansbold.ttf', 40)

    # Main Menu Text
    attack_button_text = menu_font.render("Attack", True, (33, 151, 68))
    run_button_text = menu_font.render("Run", True, (33, 151, 68))
    item_button_text = menu_font.render("Item", True, (33, 151, 68))
    magic_button_text = menu_font.render("Magic", True, (33, 151, 68))

    # Attack Menu Text
    fists_button_text = menu_font.render("Fists", True, (33, 151, 68))
    pistol_button_text = menu_font.render("Pistol", True, (33, 151, 68))

    # Item Menu Text
    health_potion_font = pygame.font.Font('freesansbold.ttf', 20)
    mana_potion_font = pygame.font.Font('freesansbold.ttf', 20)

    # Magic Menu Text
    none_available_button_text = menu_font.render("None Available", True, (33, 151, 68))

    # Combat Variables
        # Player Variables
    player_fists_dmg = 10
    player_pistol_dmg = 20
    player_turn = True
    player_attack_hits = False
    fists_attack_hits = False
    pistol_attack_hits = False
        # Zombie Variables
    zombie_dmg = 5
    zombie_attack_hits = False

    # return variables
    player_zombie_disengague = 15
    zombie_spawn = True

    # Menu Variables
    selecter_on_row_one_y = 530
    selecter_on_row_two_y = 590
    menu_left_column_x = 150
    menu_right_column_x = 450
    selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
    main_menu = True
    attack_menu = False
    item_menu = False
    magic_menu = False

    # We have these in functions because we use them multiple times.
    def player_health_count():
        # Fight Text
        player_hp_text = character_font.render("Player Health:" + str(player_hp_total), True, (0, 0, 0))
        win.blit(player_hp_text, (50, 250))
        return

    def player_mana_count():
        # Fight Text
        player_mana_text = character_font.render("Player Mana:" + str(player_mana_total), True, (0, 0, 0))
        win.blit(player_mana_text, (50, 275))
        return

    def zombie_health_count():
        zombie_hp_text = character_font.render("Zombie Health:" + str(zombie_hp_total), True, (0, 0, 0))
        win.blit(zombie_hp_text, ((X / 2) + 150, 25))
        return

    run = True
    while run:
        # Item Menu Text Recurring
        health_potion_text = health_potion_font.render(" = " + str(health_potion_total), True, (0, 0, 0))
        mana_potion_text = mana_potion_font.render(" : " + str(mana_potion_total), True, (0, 0, 0))

        # Attack Menu Text Recurring
        pistol_button_text = menu_font.render("Pistol: " + str(pistol_bullets), True, (33, 151, 68))

        clock.tick(FPS)
        win.fill([124, 124, 124])

        # Main images for the fight screen
        win.blit(character_img, (50, (Y / 2) - 200))
        # Zombie degridation as they get hurt
        if zombie_hp_total >= 76:
            win.blit(zombie_img, ((X / 2) + 150, 50))
        elif zombie_hp_total >= 51:
            win.blit(zombie75_img, ((X / 2) + 150, 50))
        elif zombie_hp_total >= 26:
            win.blit(zombie50_img, ((X / 2) + 150, 50))
        elif zombie_hp_total <= 25:
            win.blit(zombie25_img, ((X / 2) + 150, 50))
        win.blit(menu_img, (150, 525))

        # Text for the main menu
        win.blit(attack_button_text, (160, 535))
        win.blit(run_button_text, (160, 595))
        win.blit(item_button_text, (510, 535))
        win.blit(magic_button_text, (510, 595))

        if player_turn:
            # print("player Turn")
            # Player Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        sys.exit()
                    # Attack Menu keys ----
                    if attack_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_one_y:
                                player_attack_hits = True
                                fists_attack_hits = True
                                player_turn = False
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_two_y:
                                if pistol_bullets > 0:
                                    player_attack_hits = True
                                    pistol_attack_hits = True
                                    player_turn = False
                                else:
                                    pass
                        if event.key == pygame.K_TAB:
                            selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
                            attack_menu = False
                            main_menu = True
                    # Item Menu keys -----
                    if item_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_one_y:
                                if health_potion_total > 0:
                                    player_hp_total += 50
                                    health_potion_total -= 1
                                    player_turn = False
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_two_y:
                                if mana_potion_total > 0:
                                    player_mana_total += 50
                                    mana_potion_total -= 1
                                    player_turn = False
                        if event.key == pygame.K_TAB:
                            selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
                            item_menu = False
                            main_menu = True
                    # Magic Menu keys -----
                    if magic_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            pass
                        if event.key == pygame.K_TAB:
                            selector_x, selector_y = menu_left_column_x, selecter_on_row_one_y
                            magic_menu = False
                            main_menu = True
                    # Main Menu keys ----
                    if main_menu:
                        if event.key == pygame.K_UP:
                            selector_y -= 60
                        if event.key == pygame.K_DOWN:
                            selector_y += 60
                        if event.key == pygame.K_RIGHT:
                            selector_x += 300
                        if event.key == pygame.K_LEFT:
                            selector_x -= 300
                        if event.key == pygame.K_RETURN:
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_two_y:
                                if zx >= player_x:
                                    zx += player_zombie_disengague
                                    player_x -= player_zombie_disengague
                                if zx <= player_x:
                                    zx -= player_zombie_disengague
                                    player_x += player_zombie_disengague
                                if zy >= player_y:
                                    zy += player_zombie_disengague
                                    player_y -= player_zombie_disengague
                                if zy <= player_y:
                                    zy += player_zombie_disengague
                                    player_y -= player_zombie_disengague
                                run = False
                                break
                            if selector_x == menu_right_column_x and selector_y == selecter_on_row_two_y:
                                magic_menu = True
                                main_menu = False
                            if selector_x == menu_left_column_x and selector_y == selecter_on_row_one_y:
                                attack_menu = True
                                main_menu = False
                            if selector_x == menu_right_column_x and selector_y == selecter_on_row_one_y:
                                item_menu = True
                                main_menu = False



        # This is the new menu that pops up after the player selects an option
        if main_menu:
            win.blit(selector_img, (selector_x, selector_y))
        if attack_menu:
            win.blit(menu_img, (150, 525))
            win.blit(fists_button_text, (menu_left_column_x + 10, 535))
            win.blit(pistol_button_text, (menu_left_column_x + 10, 595))
            win.blit(selector_img, (selector_x, selector_y))
        if item_menu:
            win.blit(menu_img, (150, 525))
            win.blit(health_potion_img, (menu_left_column_x + 30, 535))
            win.blit(health_potion_text, (menu_left_column_x + 100, 555))
            win.blit(mana_potion_img, (menu_left_column_x + 30, 600))
            win.blit(mana_potion_text, (menu_left_column_x + 100, 620))
            win.blit(invintory_selector_img, (selector_x, selector_y))
        if magic_menu:
            win.blit(menu_img, (150, 525))
            win.blit(none_available_button_text, (menu_left_column_x + 10, 535))
            win.blit(selector_img, (selector_x, selector_y))

        if player_hp_total <= 0:
            run = False
            break

        # Graphics for hit markers
        if player_attack_hits:
            if fists_attack_hits:
                fist_sfx.play()
                zombie_hp_total -= player_fists_dmg
                win.blit(hitmarker, (650, 150))
                zombie_health_count()
                player_health_count()
                pygame.display.update()
                pygame.time.wait(500)
                fists_attack_hits = False
                player_attack_hits = False
            if pistol_attack_hits:
                pistol_sfx.play()
                zombie_hp_total -= player_pistol_dmg
                win.blit(hitmarker, (650, 50))
                win.blit(hitmarker, (700, 100))
                zombie_health_count()
                player_health_count()
                pygame.display.update()
                pygame.time.wait(500)
                pistol_bullets -= 1
                pistol_attack_hits = False
                player_attack_hits = False

        # here we look at the zombies hp and determin what to do.
        if zombie_hp_total > 0:
            if player_turn == False:
                # print("zombie turn")
                zombie_attack_hits = True
                player_turn = True

        if zombie_hp_total <= 0:
            zombie_attack_hits = False
            zombie_spawn = False
            zx, zy = '', ''
            zombies_killed += 1
            run = False
            break

        if zombie_attack_hits:
            fist_sfx.play()
            player_hp_total -= zombie_dmg
            win.blit(hitmarker, (100, 300))
            pygame.display.update()
            pygame.time.wait(500)
            zombie_attack_hits = False

        # This is the boundry section for the selector so it stays within the menus.
        if selector_x <= 100:
            selector_x = 450
        if selector_x >= 500:
            selector_x = 150
        if selector_y < selecter_on_row_one_y:
            selector_y = selecter_on_row_two_y
        if selector_y > selecter_on_row_two_y:
            selector_y = selecter_on_row_one_y

        # Update the main window so its showing all of the changes to the games state.
        # print(selector_x, selector_y)
        player_health_count()
        player_mana_count()
        zombie_health_count()
        pygame.display.update()
    return player_x, player_y, player_hp_total, player_mana_total, zx, zy, zombie_spawn, zombie_hp_total, zombies_killed, health_potion_total, mana_potion_total, pistol_bullets


def victory_screen(zombies_killed):
    # print("you are dead.")
    pygame.init()

    win = pygame.display.set_mode((1000, 1000))

    X, Y = pygame.display.get_surface().get_size()
    print("Canvas size: ", X, Y)
    print("report screen")

    # Images
    four_way_img = pygame.image.load('Art/four_way_stop.png')

    # Fonts and Text
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title = title_font.render("You have servived.", True, (33, 151, 68))

    title_font2 = pygame.font.Font('freesansbold.ttf', 100)
    title2 = title_font2.render("The Zombie City", True, (33, 151, 68))

    command_font = pygame.font.Font('freesansbold.ttf', 50)
    command = command_font.render("press enter to return to title", True, (255, 255, 255))
    zombies_killed_count = command_font.render("You killed: " + str(zombies_killed) + " zobmies", True, (255, 255, 255))

    run = True
    while run:
        win.blit(title, (50, 50))
        win.blit(title2, (100, 170))
        win.blit(zombies_killed_count, (225, 320))
        win.blit(command, (150, 600))
        win.blit(four_way_img, (X / 2 - 72, Y / 2 - 72))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                    break

        pygame.display.update()
    return


def death_screen(zombies_killed):
    # print("you are dead.")
    pygame.init()

    win = pygame.display.set_mode((1000, 1000))

    X, Y = pygame.display.get_surface().get_size()
    # print("Canvas size: ", X, Y)
    # print("report screen")

    # Images for this page
    four_way_img = pygame.image.load('Art/four_way_stop.png')

    # fonts and text for this page
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title = title_font.render("You have died.", True, (33, 151, 68))

    title_font2 = pygame.font.Font('freesansbold.ttf', 100)
    title2 = title_font2.render("The Zombie City", True, (33, 151, 68))

    title_font3 = pygame.font.Font('freesansbold.ttf', 100)
    title3 = title_font2.render("DEVOURED YOU!!", True, (252, 0, 0))

    command_font = pygame.font.Font('freesansbold.ttf', 50)
    command = command_font.render("press enter to return to title", True, (255, 255, 255))
    zombies_killed_count = command_font.render("You killed: " + str(zombies_killed) + " zobmies", True, (255, 255, 255))


    run = True
    while run:
        win.blit(title, (150, 50))
        win.blit(title2, (100, 170))
        win.blit(title3, (65, 300))
        win.blit(zombies_killed_count, (225, 600))
        win.blit(command, (175, 700))
        win.blit(four_way_img, (X / 2 - 72, Y / 2 - 72))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                    break

        pygame.display.update()
    return


def rules():
    pygame.init()

    win = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Zombie City")
    icon = pygame.image.load('Art/four_way_stop.png')
    pygame.display.set_icon(icon)

    # text and fonts for this page
    command_font = pygame.font.Font('freesansbold.ttf', 50)
    text_font = pygame.font.Font('freesansbold.ttf', 20)
    hello = command_font.render("Hello and welcome to zombie city", True, (255, 255, 255))
    basics = text_font.render("In this game you will fight zombies until you find and defeat the necromancer!", True, (255, 255, 255))
    arrows = text_font.render("The arow keys will move you around the map and invintory screens.", True, (255, 255, 255))
    enter = text_font.render("Enter will let you search for new items while on the map. Just be careful you may make too ", True, (255, 255, 255))
    enter2 = text_font.render("much noise and attract a zombie!", True, (255, 255, 255))
    enter3 = text_font.render("Enter will also be how you select items and attackes while in the invintory menu and when ", True, (255, 255, 255))
    enter4 = text_font.render("fighting.", True, (255, 255, 255))
    tab = text_font.render("The tab key will take you back to the previous menu.", True, (255, 255, 255))
    out_tro = text_font.render("That is all! Search for bigger weapons, eplore the map to find the necromancer and kill", True, (255, 255, 255))
    out_tro2 = text_font.render("him! Easier said than done!", True, (255, 255, 255))

    run = True
    while run:
        win.fill([0, 0, 0])

        win.blit(hello, (100, 100))
        win.blit(basics, (50, 200))
        win.blit(arrows, (50, 250))
        win.blit(enter, (50, 300))
        win.blit(enter2, (50, 320))
        win.blit(enter3, (50, 370))
        win.blit(enter4, (50, 390))
        win.blit(tab, (50, 440))
        win.blit(out_tro, (50, 490))
        win.blit(out_tro2, (50, 510))

        # Button input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            # key controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    run = False
                    break

        pygame.display.update()
    return


pygame.init()

win = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Zombie City")
icon = pygame.image.load('Art/four_way_stop.png')
pygame.display.set_icon(icon)
four_way_img = pygame.image.load('Art/four_way_stop.png')
selector = pygame.image.load("Art/selector.png")

# back ground sound
mixer.music.load("SFX/zombie_city_bgm.wav")
mixer.music.play(-1)

X, Y = pygame.display.get_surface().get_size()
# print("Title Screen Canvas size: ", X, Y)

title_font = pygame.font.Font('freesansbold.ttf', 100)
title = title_font.render("Welcome to", True, (33, 151, 68))

title_font2 = pygame.font.Font('freesansbold.ttf', 100)
title2 = title_font2.render("Zombie City", True, (33, 151, 68))

command_font = pygame.font.Font('freesansbold.ttf', 50)
new_game = command_font.render("New Game", True, (255, 255, 255))
rules = command_font.render("Rules", True, (255, 255, 255))


def title_screen():
    # Used to start the selector at a certain spot.
    selector_x = 375
    selector_y = 600

    run = True
    while run:
        # Drawing the screen
        win.fill([0, 0, 0])
        win.blit(title, ((X / 2) - 280, (Y / 3) - 250))
        win.blit(title2, ((X / 2) - 300, (Y / 3) - 125))
        win.blit(new_game, (375, 600))
        win.blit(rules, (375, 700))
        win.blit(four_way_img, (X / 2 - 72, Y / 2 - 72))
        win.blit(selector, (selector_x, selector_y))

        # Player Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            # key controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selector_y += 100
                if event.key == pygame.K_DOWN:
                    selector_y -= 100
            if event.type == pygame.KEYDOWN:
                # if the player selects new game create a new game
                if selector_y == 600:
                    if event.key == pygame.K_RETURN:
                        mixer.music.stop()
                        player_hp_total, necromancer_hp_total, zombies_killed = main_game()
                        # If the player dies send the player to the death screen
                        if player_hp_total <= 0:
                            death_screen(zombies_killed)
                        # if the player wins send them to the victory screen.
                        if necromancer_hp_total <= 0 and player_hp_total > 0:
                            victory_screen(zombies_killed)
                # if the player selects the rules section send them to the rules
                if selector_y == 700:
                    rules()

        # This keeps the selector confined to the only two options on screen.
        if selector_y > 700:
            selector_y = 600
        if selector_y < 600:
            selector_y = 700

        pygame.display.update()

    return


title_screen()