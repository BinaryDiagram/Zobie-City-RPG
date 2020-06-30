import sys
import pygame
from pygame import mixer

# For testing:
# player_x, player_y, player_hp_total, player_mana_total, zx, zy, health_potion_total, mana_potion_total, pistol_bullets = 0, 0, 100, 0, 0, 0, 2, 2, 10
# zombie_hp_total = 100


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


# For testing.
# fight(player_x, player_y, player_hp_total, player_mana_total, zx, zy, zombie_hp_total, health_potion_total, mana_potion_total, pistol_bullets)
