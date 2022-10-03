import matplotlib.pyplot as plt
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

    def __call__(self, method='heat_map', **kwargs):
        method = getattr(self, method, None)
        return method(**kwargs)

    def ndvi_plot(self, ax=None, kws=None):

        ndvi = self.vegetation_index.copy()

        ndvi[ndvi <= 0] = 0
        ndvi[ndvi > 0.9] = 10

        for index, step in np.enumerate(np.arange(0.0, 0.9, 0.1)):
            ndvi[(ndvi > step) & (ndvi <= step + 0.1)] = index

        ax.imshow(ndvi, **kws)
        return ax

    def heat_map(self, ax=None, kws=None):
        ax = plt.gca() if ax is None else ax
        kws = {} if kws is None else kws

        ax.imshow(self.vegetation_index, **kws)
        return ax
