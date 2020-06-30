import sys
import pygame
from pygame import mixer

"""This page is almost a copy of the page from the fight_screen except that it is made for the necromancer instead. 
we ran into a glitch where when the player would try to run from the necromancer they would end up outside of the map 
and would be forced back into the necromancer We got around this by having the player return to the start of the game 
when they run from the necromancer. I would like to go back and fix this later but the logic illudes me for now."""

# for testing
# player_x, player_y, player_hp_total, player_mana_total, player_val_x, player_val_y, zx, zy, health_potion_total, mana_potion_total, pistol_bullets = 0, 0, 100, 0, 0, 0, 0, 0, 2, 2, 10
# zombie_hp_total = 200


def fight(player_x, player_y, player_hp_total, player_mana_total, player_val_x, player_val_y, necro_x, necro_y, necromancer_hp_total, health_potion_total, mana_potion_total, pistol_bullets):
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


# fight(player_x, player_y, player_hp_total, player_mana_total, player_val_x, player_val_y, zx, zy, zombie_hp_total, health_potion_total, mana_potion_total, pistol_bullets)
