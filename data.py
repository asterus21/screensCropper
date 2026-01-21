'''Contains data, i.e. color of the target pixels.'''

def get_upper_target() -> dict:
    '''Contains upper targets colors.'''
    targets = {
        'upper_0' : (187, 187, 187),
        'upper_1' : (186, 186, 186),
        'upper_2' : (112, 112, 112),
        'upper_3' : (153, 153, 153),
        'upper_4' : (182, 182, 182),
        'upper_5' : (162, 162, 162),
        'upper_6' : (111, 111, 111),
        'upper_7' : (161, 161, 161)
    }

    return targets

def get_upper_neighbors() -> dict:
    '''Contains upper neighbors colors.'''
    targets = {
        'neighbor_0' : (239, 239, 239),
        'neighbor_1' : (143, 143, 143),
        'neighbor_2' : (238, 238, 238)
    }

    return targets

def get_lower_target() -> dict:
    '''Contains lower targets colors.'''
    targets = {
        'lower_0' : (176, 176, 176),
        'lower_1' : (175, 175, 175),
        'lower_2' : (106, 106, 106),
        'lower_3' : (143, 143, 143),
        'lower_4' : (173, 173, 173),
        'lower_5' : (151, 151, 151),
        'lower_6' : (105, 105, 105),
        'lower_7' : (149, 149, 149)
    }

    return targets

def get_lower_neighbors() -> dict:
    '''Contains lower neighbors colors.'''
    targets = {
        'neighbor_0' : (238, 238, 238),
        'neighbor_1' : (143, 143, 143),
        'neighbor_2' : (237, 237, 237),
        'neighbor_3' : (236, 236, 236),
    }

    return targets
