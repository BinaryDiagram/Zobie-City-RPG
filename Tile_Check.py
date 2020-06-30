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