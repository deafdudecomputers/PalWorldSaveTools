from collections import namedtuple

# Old coordinate system (before v4.11 update)
__transl_x_old = 123888
__transl_y_old = 158000
__scale_old = 459

# New coordinate system (after v4.11 update)
__transl_x_new = 276020
__transl_y_new = -15000
__scale_new = 724

Point = namedtuple('Point', ['x', 'y'])

def sav_to_map(x: float, y: float, new: bool = False) -> Point:
    if new:
        transl_x = __transl_x_new
        transl_y = __transl_y_new
        scale = __scale_new
    else:
        transl_x = __transl_x_old
        transl_y = __transl_y_old
        scale = __scale_old

    newX = x + transl_x
    newY = y - transl_y

    return Point(x=round(newY / scale), y=round(newX / scale))

def map_to_sav(x: int, y: int, new: bool = False) -> Point:
    if new:
        transl_x = __transl_x_new
        transl_y = __transl_y_new
        scale = __scale_new
    else:
        transl_x = __transl_x_old
        transl_y = __transl_y_old
        scale = __scale_old

    newX = x * scale
    newY = y * scale

    return Point(x=newY - transl_x, y=newX + transl_y)
