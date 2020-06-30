import pygame
import sys

# Used for testing perpuses.
# zombies_killed = 12


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


# For testing:
# death_screen(zombies_killed)
