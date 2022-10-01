import numpy as np

from attrs import define, field
from matplotlib import colors

from .models import Bands


def inter_from_256(x):
    return np.interp(x=x, xp=[0, 255], fp=[0, 1])


cdict = {
    'red': ((0.0, inter_from_256(169), inter_from_256(169)),
            (0.1, inter_from_256(244), inter_from_256(244)),
            (0.2, inter_from_256(253), inter_from_256(253)),
            (0.3, inter_from_256(230), inter_from_256(230)),
            (1, inter_from_256(112), inter_from_256(112))),
    'green': ((0.0, inter_from_256(23), inter_from_256(23)),
              (0.1, inter_from_256(109), inter_from_256(109)),
              (0.2, inter_from_256(219), inter_from_256(219)),
              (0.3, inter_from_256(241), inter_from_256(241)),
              (1, inter_from_256(198), inter_from_256(198))),
    'blue': ((0.0, inter_from_256(69), inter_from_256(69)),
             (0.1, inter_from_256(69), inter_from_256(69)),
             (0.2, inter_from_256(127), inter_from_256(127)),
             (0.3, inter_from_256(146), inter_from_256(146)),
             (1, inter_from_256(162), inter_from_256(162))),
}

ndvi_cmap = colors.LinearSegmentedColormap('ndvi_cmap', segmentdata=cdict)


@define
class IndexPlotter:
    vegetation_index: field(converter=np.asarray)

    def plot(self, ax=None, kws=None):
        pass
