import math

import numpy as np


def rotate_2d(self, angle, unit='rad'):
    if unit not in ['deg', 'rad']:
        raise ValueError('Only units of rad or deg are supported')
    if unit == 'deg':
        angle = math.radians(angle)

    rotation_matrix = [[np.cos(angle), np.sin(angle)],
                       [np.sin(angle), np.cos(angle)]]
    return np.matmul(rotation_matrix, [[self.x], [self.y]]).T[0]
