from collections import namedtuple

__transl_x = 123888
__transl_y = 158000
__scale = 459

Point = namedtuple('Point', ['x', 'y'])


def sav_to_map(x: float, y: float) -> Point:
    """
    Convert coordinates from the system in .sav files to in-game
    coordinate system in Paldex
    """
    # Translate
    newX = x + __transl_x
    newY = y - __transl_y

    # NOTE: The X and Y coordinates are flipped on purpose
    # Scale down
    return Point(x=round(newY/__scale), y=round(newX/__scale))


def map_to_sav(x: int, y: int) -> Point:
    """
    Convert coordinates from the in-game coordinates system in
    Paldex to the system in .sav files
    """
    # Scale up
    newX = x * __scale
    newY = y * __scale

    # NOTE: The X and Y coordinates are flipped on purpose
    # Translate
    return Point(x=newY - __transl_x, y=newX + __transl_y)
