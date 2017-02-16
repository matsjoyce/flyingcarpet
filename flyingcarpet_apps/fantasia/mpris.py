import collections
import os.path
from PyQt5 import QtCore, QtDBus, QtMultimedia
import ctypes
import dbus.service
import dbus.mainloop.pyqt5


LOCATION = os.path.dirname(__file__) + os.path.sep


class DBusMediaPlayer2Adaptor(dbus.service.Object):
    properties = {}

    def __init__(self, parent):
        self.parent = lambda: parent
        self.last_position = 0
        super().__init__(dbus.SessionBus(), "/org/mpris/MediaPlayer2")
        self.prop_values = {i: getattr(self, i) for i in self.properties}
        self.parent().position_slider.valueChanged.connect(self.onSeek)
        self.parent().maybeSomethingChanged.connect(self.onChange)

    def onChange(self):
        changes = collections.defaultdict(dict)
        for i in self.properties:
            new = getattr(self, i)
            if new != self.prop_values[i]:
                iface = self.properties[i].__doc__
                changes[iface][i] = self.prop_values[i] = new
        for iface, values in changes.items():
            self.PropertiesChanged(iface,
                                   dbus.Dictionary(values, signature="sv"), [])
        self.onSeek(self.parent().player.position())

    def dbus_property(iface="org.mpris.MediaPlayer2.Player", properties=properties):
        def w(prop):
            prop.__doc__ = iface
            properties[prop.fget.__name__] = prop
            return prop
        return w

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        return self.GetAll(interface_name)[property_name]

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        return dbus.Dictionary({i: j.fget(self) for i, j in DBusMediaPlayer2Adaptor.properties.items()}, signature="sv")

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv')
    def Set(self, interface_name, property_name, new_value):
        self.properties[property_name].fset(new_value)
        self.PropertiesChanged(interface_name, {property_name: new_value}, [])

    @dbus.service.signal(dbus.PROPERTIES_IFACE, signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        pass

    # org.mpris.MediaPlayer2

    @dbus.service.method("org.mpris.MediaPlayer2")
    def Raise(self):
        state = self.parent().windowState() | QtCore.Qt.WindowActive
        self.parent().setWindowState(state)

    @dbus.service.method("org.mpris.MediaPlayer2")
    def Quit(self):
        self.parent().close()

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def CanQuit(self):
        return True

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def Fullscreen(self):
        return bool(self.parent().windowState() & QtCore.Qt.WindowMaximized)

    @Fullscreen.setter
    def Fullscreen(self):
        state = self.parent().windowState() | QtCore.Qt.WindowMaximized
        self.parent().setWindowState(state)

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def CanSetFullscreen(self):
        return True

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def CanRaise(self):
        return True

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def HasTrackList(self):
        return False

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def Identity(self):
        return "fantasia"

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def DesktopEntry(self):
        return "flyingcarpet-fantasia"

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def SupportedUriSchemes(self):
        return dbus.Array([], signature="s")

    @dbus_property("org.mpris.MediaPlayer2")
    @property
    def SupportedMimeTypes(self):
        return dbus.Array([], signature="s")

    # org.mpris.MediaPlayer2.Player

    @dbus.service.method("org.mpris.MediaPlayer2.Player")
    def Next(self):
        self.parent().next()

    @dbus.service.method("org.mpris.MediaPlayer2.Player")
    def Previous(self):
        self.parent().previous()

    @dbus.service.method("org.mpris.MediaPlayer2.Player")
    def Pause(self):
        self.parent().pause()

    @dbus.service.method("org.mpris.MediaPlayer2.Player")
    def PlayPause(self):
        if self.parent().player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.parent().pause()
        else:
            self.parent().play()

    @dbus.service.method("org.mpris.MediaPlayer2.Player")
    def Stop(self):
        self.parent().stop()

    @dbus.service.method("org.mpris.MediaPlayer2.Player")
    def Play(self):
        self.parent().play()

    @dbus.service.method("org.mpris.MediaPlayer2.Player", in_signature="x")
    def Seek(self, position):
        self.parent().player.setPosition(self.parent().player.position() + position / 1000)

    @dbus.service.method("org.mpris.MediaPlayer2.Player", in_signature="ox")
    def SetPosition(self, uri, position):
        if position == self.last_position:
            return
        self.parent().player.setPosition(position / 1000)

    @dbus.service.method("org.mpris.MediaPlayer2.Player", in_signature="o")
    def OpenUri(self, uri):
        raise NotImplementedError()

    @dbus_property()
    @property
    def PlaybackStatus(self):
        state = self.parent().player.state()
        if state == QtMultimedia.QMediaPlayer.StoppedState or self.parent().player.duration() <= 0:
            return "Stopped"
        elif state == QtMultimedia.QMediaPlayer.PlayingState:
            return "Playing"
        elif state == QtMultimedia.QMediaPlayer.PausedState:
            return "Paused"

    @dbus_property()
    @property
    def LoopStatus(self):
        if self.parent().actionLoop.isChecked():
            return "Playlist"
        else:
            return "None"

    @LoopStatus.setter
    def LoopStatus(self, value):
        if value == "None":
            self.parent().actionLoop.setChecked(False)
        else:
            self.parent().actionLoop.setChecked(True)

    @dbus_property()
    @property
    def Rate(self):
        return 1.0

    @dbus_property()
    @property
    def Shuffle(self):
        return self.parent().actionRandomize.isChecked()

    @Shuffle.setter
    def Shuffle(self, value):
        return self.parent().actionRandomize.setChecked(value)

    @dbus_property()
    @property
    def Metadata(self):
        po = self.parent().playing_obj
        if po is not None:
            data = dbus.Dictionary({"mpris:trackid": dbus.ObjectPath("/org/mpris/MediaPlayer2"),
                                    "xesam:title": po.name,
                                    "xesam:album": po.album,
                                    "xesam:url": po.fname}, signature="sv")
            if self.parent().player.duration() > 0:
                data["mpris:length"] = self.parent().player.duration() * 1000
            return data
        return dbus.Dictionary({}, signature="sv")

    @dbus_property()
    @property
    def Volume(self):
        return 0.4

    @dbus_property()
    @property
    def Position(self):
        self.last_position = self.parent().player.position() * 1000
        return dbus.Int64(self.last_position)

    @dbus_property()
    @property
    def GetPosition(self):
        self.last_position = self.parent().player.position() * 1000
        return dbus.Int64(self.last_position)

    @dbus_property()
    @property
    def MinimumRate(self):
        return 1.0

    @dbus_property()
    @property
    def MaximumRate(self):
        return 1.0

    @dbus_property()
    @property
    def CanGoNext(self):
        return True

    @dbus_property()
    @property
    def CanGoPrevious(self):
        return True

    @dbus_property()
    @property
    def CanPlay(self):
        return True

    @dbus_property()
    @property
    def CanPause(self):
        return True

    @dbus_property()
    @property
    def CanSeek(self):
        return True

    @dbus_property()
    @property
    def CanControl(self):
        return True

    def onSeek(self, position):
        self.Seeked(position * 1000)

    @dbus.service.signal(dbus.PROPERTIES_IFACE, signature='x')
    def Seeked(self, position):
        pass


def dbus_mpris(mainwindow):
    ql = dbus.mainloop.pyqt5.DBusQtMainLoop(set_as_default=True)
    name = dbus.service.BusName('org.mpris.MediaPlayer2.fantasia', dbus.SessionBus())
    return DBusMediaPlayer2Adaptor(mainwindow), ql, name
