import Main_Game
import Death_Screen
import Victory_Screen
import pygame
from pygame import mixer
import sys
import Rules

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
                        player_hp_total, necromancer_hp_total, zombies_killed = Main_Game.main_game()
                        # If the player dies send the player to the death screen
                        if player_hp_total <= 0:
                            Death_Screen.death_screen(zombies_killed)
                        # if the player wins send them to the victory screen.
                        if necromancer_hp_total <= 0 and player_hp_total > 0:
                            Victory_Screen.victory_screen(zombies_killed)
                # if the player selects the rules section send them to the rules
                if selector_y == 700:
                    Rules.rules()

        # This keeps the selector confined to the only two options on screen.
        if selector_y > 700:
            selector_y = 600
        if selector_y < 600:
            selector_y = 700

        pygame.display.update()

    return


title_screen()
