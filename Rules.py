import pygame
import sys


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

# rules()
