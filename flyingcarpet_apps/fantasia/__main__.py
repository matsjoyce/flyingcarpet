import random
import os.path
import pathlib

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import potash
from potash.qt3 import object_view, object_model, object_edit_widget, displays
from misty.qt import queryedit
import flyingcarpet

from . import mpris, ui


class PositionLabel(QtWidgets.QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.position = self.duration = 0
        self.updateText()

    @staticmethod
    def formatTime(milli):
        mins, secs = divmod(milli / 1000, 60)
        hours, mins = divmod(mins, 60)
        return f"{int(hours)}:{int(mins):02}:{round(secs):02}"

    def updateText(self):
        p = self.formatTime(self.position)
        d = self.formatTime(self.duration)
        self.setText(f"{p} / {d}")

    def setPosition(self, position):
        self.position = position
        self.updateText()

    def setDuration(self, duration):
        self.duration = duration
        self.updateText()


class SliderStyle(QtWidgets.QProxyStyle):
    def styleHint(self, hint, option, widget, returnData):
        if hint == QtWidgets.QStyle.SH_Slider_AbsoluteSetButtons:
            return QtCore.Qt.LeftButton
        return super().styleHint(hint, option, widget, returnData)


class PlayedDisplay(displays.Display):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.playing = QtGui.QIcon.fromTheme("media-playback-start")
        self.played = QtGui.QIcon.fromTheme("dialog-ok-apply")

    def sizeHint(self, option, index):
        return QtCore.QSize(26, 26)

    def paint(self, qp, option, index):
        obj = index.data(object_model.OBJECT_ROLE)
        x, y = option.rect.x() + 2, option.rect.y() + 2
        width, height = option.rect.width() - 4, option.rect.height() - 4
        qp.save()
        if option.state & QtWidgets.QStyle.State_Selected:
            qp.fillRect(option.rect, option.palette.highlight())
        if obj == self.main_window.playing_obj:
            self.playing.paint(qp, x, y, width, height)
        elif obj.oid in self.main_window.played_yet:
            self.played.paint(qp, option.rect)
        qp.restore()


class FantasiaApp(flyingcarpet.App, ui.Ui_MainWindow):
    NAME = "fantasia"
    LAUNCHER_NAME = "fantasia"
    GENERIC_NAME = "Music Player"
    DESCRIPTION = "Music player using the potash system"
    VERSION = (0, 1)
    ICON = "player-volume"
    CATEGORIES = {flyingcarpet.Category.Audio}
    SUBCATEGORIES = {flyingcarpet.SubCategory.Player}
    ADD_PREFIX = False

    maybeSomethingChanged = QtCore.pyqtSignal(name="maybeSomethingChanged")

    def __init__(self):
        super().__init__(maximized=True)
        self.setupUi(self)

        self.source = potash.user_source()
        self.columns = [object_model.ObjectModelHeader("album"),
                        object_model.ObjectModelHeader("name"),
                        object_model.ObjectModelHeader("tags"),
                        object_model.ObjectModelHeader("rating")]
        self.playing_obj = None
        self.played_yet = set()

        self.player = QtMultimedia.QMediaPlayer(self)

        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.position_slider.setTracking(False)
        self.position_slider.setStyle(SliderStyle(self.position_slider.style()))
        self.control_toolbar.insertWidget(self.actionSeek_Forward,
                                          self.position_slider)

        self.enter_shortcut = QtWidgets.QShortcut(QtCore.Qt.Key_Return, self)
        self.enter_shortcut.activated.connect(self.enter_pressed)

        self.setup_playlist_tab()
        self.setup_media_tab()
        self.setup_statusbar()
        self.set_player_actions()

        self.tabWidget.currentChanged.connect(self.set_player_actions)
        self.actionAdd.triggered.connect(self.add_to_playlist)
        self.actionRemove.triggered.connect(self.remove_from_playlist)
        self.actionClear.triggered.connect(self.clear_playlist)

        self.actionMove_Up.triggered.connect(self.move_up)
        self.actionMove_Down.triggered.connect(self.move_down)

        self.actionPlay.triggered.connect(self.play)
        self.actionPause.triggered.connect(self.pause)
        self.actionStop.triggered.connect(self.stop)

        self.actionNext.triggered.connect(self.next)
        self.actionPrevious.triggered.connect(self.previous)

        self.actionSeek_Backward.triggered.connect(self.seek_backward)
        self.actionSeek_Forward.triggered.connect(self.seek_forward)

        self.actionAdd_Music_File.triggered.connect(self.add_music_file)
        self.actionAdd_Music_Folder.triggered.connect(self.add_music_folder)

        self.actionRandomize.triggered.connect(self.randomize_playlist)

        self.player.durationChanged.connect(self.position_message_label.setDuration)
        self.player.positionChanged.connect(self.position_message_label.setPosition)
        self.player.durationChanged.connect(self.position_slider.setMaximum)
        self.player.positionChanged.connect(self.set_position_slider_value)
        self.player.stateChanged.connect(self.set_player_actions)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.player.mediaStatusChanged.connect(self.set_player_actions)
        self.player.durationChanged.connect(self.set_player_actions)

        self.position_slider.valueChanged.connect(self.player.setPosition)

        self.playlist_object_view.model().modelReset.connect(self.set_player_actions)
        self.playlist_object_view.selectionModel().selectionChanged.connect(self.set_player_actions)
        self.media_object_view.selectionModel().selectionChanged.connect(self.set_player_actions)
        self.actionLoop.toggled.connect(self.set_player_actions)

        self.mpris = mpris.dbus_mpris(self)

    def setup_playlist_tab(self):
        self.playlist_object_view = object_view.ObjectView(self)
        self.playlist_object_view.setRootIsDecorated(False)
        self.playlist_tab.layout().addWidget(self.playlist_object_view)
        model = object_model.ObjectModel(self.source, self.playlist_object_view)
        model.setHeaders([object_model.ObjectModelHeader(attr="name", title="", display=PlayedDisplay(self)),
                          *self.columns])
        self.playlist_object_view.setModel(model)

    def setup_media_tab(self):
        self.media_object_view = object_view.ObjectView(self)
        self.media_object_view.setRootIsDecorated(False)
        self.media_tab.layout().addWidget(self.media_object_view)
        model = object_model.ObjectModel(self.source, self.media_object_view)
        model.setHeaders(self.columns)
        model.setFilter(type=potash.builtin_objects.Music)
        self.media_object_view.setModel(model)
        self.media_object_view.setSortingEnabled(True)

        self.media_query_frame = QtWidgets.QFrame(self.media_tab)
        self.media_query_layout = QtWidgets.QHBoxLayout(self.media_query_frame)
        self.media_query_layout.setContentsMargins(0, 0, 0, 0)
        self.media_tab.layout().addWidget(self.media_query_frame)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.control_toolbar.sizePolicy().hasHeightForWidth())
        self.media_query_frame.setSizePolicy(sizePolicy)

        self.media_query_label = QtWidgets.QLabel(self.media_query_frame)
        self.media_query_label.setText("Search:")
        self.media_query_frame.layout().addWidget(self.media_query_label)

        self.media_query_edit = queryedit.QueryEdit(self.media_query_frame)
        self.media_query_frame.layout().addWidget(self.media_query_edit)
        self.media_query_edit.queryChanged.connect(self.set_query)

    def setup_statusbar(self):
        self.position_message_label = PositionLabel(self.statusBar)
        self.position_message_label.setStyleSheet("QLabel {color: white;}")
        self.statusBar.addPermanentWidget(self.position_message_label)

    def set_query(self, q):
        try:
            self.media_object_view.model().setFilter(q.matches,
                                                     type=potash.builtin_objects.Music)
        except Exception as e:
            pass

    def add_to_playlist(self):
        total_items = self.playlist_object_view.model().objs()
        total_items.extend(i for i in self.media_object_view.selectedObjects() if i not in total_items)
        self.playlist_object_view.model().setObjs(total_items)

    def randomize_playlist(self):
        total_items = self.playlist_object_view.model().objs()
        random.shuffle(total_items)
        self.playlist_object_view.model().setObjs(total_items)

    def remove_from_playlist(self):
        items = self.playlist_object_view.selectedObjects()
        total_items = self.playlist_object_view.model().objs()
        if self.playing_obj in items:
            self.next()
        for item in items:
            total_items.remove(item)
            self.played_yet.discard(item.oid)
        self.playlist_object_view.model().setObjs(total_items)

    def move_up(self):
        for index in self.playlist_object_view.selectedRows():
            self.playlist_object_view.model().setIndexRow(index, index.row() - 1)

    def move_down(self):
        for index in reversed(self.playlist_object_view.selectedRows()):
            self.playlist_object_view.model().setIndexRow(index, index.row() + 1)

    def clear_playlist(self):
        self.stop()
        self.played_yet.clear()
        self.playlist_object_view.model().setObjs([])

    def clear_played_yet(self):
        self.played_yet.clear()
        for i in range(self.playlist_object_view.model().rowCount()):
            self.playlist_object_view.update(self.playlist_object_view.model().index(i, 0))

    def next_playlist_item(self):
        objs = self.playlist_object_view.model().objs()
        if not objs:
            return
        if self.playing_obj:
            index = objs.index(self.playing_obj)
        elif objs[0] not in self.played_yet or self.actionLoop.isChecked():
            index = -1
        if index + 1 >= len(objs):
            if not self.actionLoop.isChecked():
                return
            index = -1
        return objs[index + 1]

    def prev_playlist_item(self):
        objs = self.playlist_object_view.model().objs()
        if not objs:
            return
        index = objs.index(self.playing_obj) if self.playing_obj else -1
        if index <= 0:
            if not self.actionLoop.isChecked():
                return
            index = len(objs)
        return objs[index - 1]

    def next(self):
        self.play_file(self.next_playlist_item())

    def previous(self):
        self.play_file(self.prev_playlist_item())

    def set_player_actions(self):
        content = bool(self.playlist_object_view.model().rowCount())
        pselection = self.playlist_object_view.selectionModel().hasSelection()
        mselection = self.media_object_view.selectionModel().hasSelection()
        previous = self.prev_playlist_item() is not None
        next = self.next_playlist_item() is not None
        index = self.tabWidget.currentIndex()
        playlist_tab = index == 0
        media_tab = index == 1

        state = self.player.state()
        playing = state == QtMultimedia.QMediaPlayer.PlayingState
        paused = state == QtMultimedia.QMediaPlayer.PausedState
        stopped = state == QtMultimedia.QMediaPlayer.StoppedState

        self.actionPlay.setVisible(paused or stopped)
        self.actionPlay.setEnabled(content)
        self.actionPause.setVisible(playing)
        self.actionStop.setEnabled(playing or paused)

        self.actionSeek_Backward.setEnabled(playing or paused)
        self.actionSeek_Forward.setEnabled(playing or paused)

        self.actionPrevious.setEnabled(previous)
        self.actionNext.setEnabled(next)

        self.actionAdd.setEnabled(mselection and media_tab)
        self.actionRemove.setEnabled(pselection and playlist_tab)
        self.actionClear.setEnabled(content)

        self.actionMove_Up.setEnabled(pselection and playlist_tab)
        self.actionMove_Down.setEnabled(pselection and playlist_tab)

        self.position_slider.setEnabled(playing or paused)

        self.maybeSomethingChanged.emit()

    def play_file(self, obj):
        if self.playing_obj:
            old_index, = self.playlist_object_view.model().indexes_of_obj(self.playing_obj)
        else:
            old_index = None
        if obj is None:
            self.stop()
        else:
            self.playing_obj = obj
            self.played_yet.add(obj.oid)
            fname = self.playing_obj.fname
            self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fname)))
            self.player.play()
            self.statusBar.showMessage(f"Playing {obj.album} :: {obj.name}")
            self.setWindowTitle(f"fantasia - {obj.album} :: {obj.name}")
            index, = self.playlist_object_view.selectObject(obj, clear=True)
            self.playlist_object_view.update(index)
        if old_index:
            self.playlist_object_view.update(old_index)

    def play(self):
        if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.player.play()
        elif self.player.state() == QtMultimedia.QMediaPlayer.StoppedState:
            self.next()

    def pause(self):
        self.player.pause()

    def media_status_changed(self, status):
        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.next()
        else:
            print(status)

    def stop(self):
        if self.playing_obj:
            index, = self.playlist_object_view.model().indexes_of_obj(self.playing_obj)
            self.playlist_object_view.update(index)
        self.player.stop()
        self.playing_obj = None
        self.player.setMedia(QtMultimedia.QMediaContent())
        self.statusBar.showMessage("")
        self.position_message_label.setDuration(0)
        self.position_message_label.setPosition(0)
        self.setWindowTitle("fantasia")

    def seek_forward(self):
        self.player.setPosition(self.player.position() + 10000)

    def seek_backward(self):
        self.player.setPosition(self.player.position() - 10000)

    def play_index(self, index):
        obj = index.data(object_model.OBJECT_ROLE)
        if obj != self.playing_obj:
            self.play_file(obj)

    def set_position_slider_value(self, value):
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(value)
        self.position_slider.blockSignals(False)

    def enter_pressed(self):
        if not self.tabWidget.currentIndex():
            idxs = self.playlist_object_view.selectionModel().selectedRows()
            if idxs:
                self.play_index(idxs[0])
        else:
            self.add_to_playlist()

    def add_music_file(self):
        fs = QtWidgets.QFileDialog.getOpenFileNames(
             self, "Open File",
             os.path.expanduser("~/Music"),
             "Music files (*.mp3 *.m4a *.wav)")[0]
        for f in fs:
            path = pathlib.Path(f)
            album = " - ".join(path.parent.relative_to(os.path.expanduser("~/Music")).parts)
            obj = potash.builtin_objects.Music(self.source, fname=f, name=path.stem, album=album)
            if not object_edit_widget.ObjectEditDialog.edit([obj], self.columns):
                obj.destroy()

    def add_music_folder(self):
        f = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder",
                                                       os.path.expanduser("~/Music"))
        if not f:
            return
        path = pathlib.Path(f)
        album = " - ".join(path.relative_to(os.path.expanduser("~/Music")).parts)
        objs = [potash.builtin_objects.Music(self.source, fname=str(i), name=i.stem, album=album)
                for i in path.iterdir() if i.suffix in (".mp3", ".m4a", ".wav")]
        if not object_edit_widget.ObjectEditDialog.edit(objs, self.columns[:1] + self.columns[2:]):
            for obj in objs:
                obj.destroy()

