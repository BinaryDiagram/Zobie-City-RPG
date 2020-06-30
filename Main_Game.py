import math
import random
import time
import Tile_Check
import fight_screen
import Invintory_Menu
import Fight_Cut_Scean
import Boss_Fight_Scean
import pygame
import sys
from pygame import mixer


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
            player_x, player_y = Tile_Check.boss_tile_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = Tile_Check.north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = Tile_Check.south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 5:
                player_x, player_y = Tile_Check.north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = Tile_Check.north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = Tile_Check.north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 5:
                player_x, player_y = Tile_Check.south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = Tile_Check.south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = Tile_Check.south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compatible_tile == south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 3:
                player_x, player_y = Tile_Check.north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 4:
                player_x, player_y = Tile_Check.north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_3_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_3_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_3_north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == east_3_north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == east_3_south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == east_3_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_3_south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_3_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_3_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.east_west_north_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.east_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == west_3_north_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == west_3_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == west_3_south_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_south_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 1:
                player_x, player_y = Tile_Check.north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)
            if rand_int == 2:
                player_x, player_y = Tile_Check.north_south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.south_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == north_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.south_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_east_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_west_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

        if compat_tile == south_west_compatible_tiles:
            if rand_int == 0:
                player_x, player_y = Tile_Check.north_east_collision_check(player_x, player_y, draw_x, draw_y, character_pushback)

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
                    player_hp_total, player_mana_total, health_potion_total, mana_potion_total, pistol_bullets, zombie_frozen = Invintory_Menu.invintory(
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
        player_x, player_y = Tile_Check.tile_check(X, Y, player_x, player_y, player_pushback)
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
                                Fight_Cut_Scean.fade_to_black()
                                pygame.time.wait(100)
                                fight_music.play(-1)
                                # run the cut sceen
                                # print("player zombie collison")
                                player_x, player_y, player_hp_total, player_mana_total, zx, zy, zs, z_hp, zombies_killed, health_potion_total, \
                                mana_potion_total, pistol_bullets = fight_screen.fight(player_x, player_y, player_hp_total, player_mana_total, zx, zy, z_hp, zombies_killed, health_potion_total, mana_potion_total, pistol_bullets)
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
                        zx, zy = Tile_Check.tile_check(X, Y, zx, zy, zombie_pushback)
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
                Fight_Cut_Scean.fade_to_black()
                pygame.time.wait(100)
                boss_fight.play(-1)
                player_x, player_y, player_hp_total, player_mana_total, necro_x, necro_y, necromancer_hp_total,\
                health_potion_total, mana_potion_total, pistol_bullets = Boss_Fight_Scean.fight(player_x, player_y,
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


# main_game()
