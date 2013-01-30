from PyQt4 import QtCore, QtGui

from dat import MIMETYPE_DAT_PLOT
from dat.gui.generic import DraggableListWidget
from dat.global_data import GlobalManager

from vistrails.core.application import get_vistrails_application


class PlotList(DraggableListWidget):
    def buildData(self, element):
        data = QtCore.QMimeData()
        data.setData(self._mime_type, '')
        data.plot = element.plot
        return data


class PlotItem(QtGui.QListWidgetItem):
    def __init__(self, plot):
        QtGui.QListWidgetItem.__init__(self, plot.name)
        self.plot = plot


class PlotPanel(QtGui.QWidget):
    def __init__(self):
        super(PlotPanel, self).__init__()

        layout = QtGui.QVBoxLayout()

        self._list_widget = PlotList(self, MIMETYPE_DAT_PLOT)
        layout.addWidget(self._list_widget)

        self.setLayout(layout)

        app = get_vistrails_application()
        app.register_notification('dat_new_plot', self.plot_added)
        app.register_notification('dat_removed_plot', self.plot_removed)

        for plot in GlobalManager.plots:
            self.plot_added(plot)

    def plot_added(self, plot):
        self._list_widget.addItem(PlotItem(plot))

    def plot_removed(self, plot):
        item = 0
        while item < self._list_widget.count():
            if self._list_widget.item(item).plot is plot:
                self._list_widget.takeItem(item)
            else:
                item += 1
