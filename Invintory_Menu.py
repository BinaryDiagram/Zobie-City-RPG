import pygame
from pygame import mixer
import sys

# For testing:
# player_hp_total, player_mana_total, health_potion_total, mana_potion_total, pistol_bullets, zombies_frozen = 100, 0, 2, 5, 10, False


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


# For testing
# invintory(player_hp_total, player_mana_total, health_potion_total, mana_potion_total, pistol_bullets, zombies_frozen)
