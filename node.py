from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.showbase.BulletinBoard import BulletinBoard
from direct.showbase.JobManager import JobManager
from panda3d.core import VirtualFileSystem, ConfigVariableManager, ClockObject, NodePath
from direct.showbase.Messenger import Messenger
import math

window: ShowBase = ShowBase()

data: BulletinBoard = BulletinBoard()
data.post("A", 1)
file_system: VirtualFileSystem = VirtualFileSystem.get_global_ptr()
jobs: JobManager = JobManager()
config: ConfigVariableManager = ConfigVariableManager.get_global_ptr()
clock: ClockObject = globalClock
events: Messenger = window.messenger


class Event(DirectObject):
    def __init__(self):
        super().__init__()

    def clean_up(self):
        self.ignore_all()
        self.remove_all_tasks()


def trigger(name: str, *args):
    events.send(name, sentArgs=args)


def model(name: str, parent=window.render, static=True):
    model = window.loader.load_moade(name)
    if static:
        model.clear_model_nodes()
        model.flatten_strong()

    if parent:
        model.reparent_to(parent)

    return model


def sound(name: str):
    return window.loadSfx(name)


def music(name: str):
    return window.loadMusic(name)


class Var:
    def __init__(self, value, on_change=None, range=None, sync=False):
        self._value = value
        self.range: tuple = range
        self.on_change = on_change

        self.synced = sync

        if self.synced:
            # Register the variable in a sync manager and set it up so that everytime it changes
            # It broadcasts the var
            pass

    def _on_sync(self):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value_type = type(value)

        if value_type is str:
            value = value[:self.range[1]]
        elif value_type is int or value_type is float:
            value = min(self.range[0], max(value, self.range[1]))

        if self.on_change:
            value = self.on_change(value)

        self._value = value

        if self.synced:
            pass


class Sound3D:
    def __init__(self):
        ...


class VarientSound:
    def __init__(self, name: str):
        """DOESNT WORK"""
        self.sound = window.loadSfx(name)

    def play(self):
        self.sound.pitch()
        self.sound.play()


inputs = {}


def on_input():
    ...


class SaturnNode:
    def __init__(self, name, parent=window.render):
        self._node = NodePath(name)
        self._node.reparent_to(parent)
        self._object = Event()
        self._parent = None
        self.children = []

    def save(self):
        ...

    def listen(self, name, function):
        self._object.accept(name, function)

    def resume_listening(self):
        ...

    def ignore(self, name):
        self._object.ignore(name)

    def ignore_all(self):
        self._object.ignore_all()

    def disable(self):
        self.ignore_all()
        self.pause_all_tasks()

    def enable(self):
        self.resume_listening()
        self.resume_all_tasks()

    def pause_task(self):
        ...

    def resume_task(self):
        ...

    def pause_all_tasks(self):
        ...

    def resume_all_tasks(self):
        ...

    @property
    def tasks(self):
        ...

    @property
    def billboard(self):
        ...

    @property
    def childeren(self):
        ...

    @property
    def parent(self):
        ...

    @property
    def color(self):
        ...

    def look_at(self):
        ...

    def stash(self):
        self._node.stash()
        self.disable()
        for child in self.children:
            child.stash()

    def unstash(self):
        self._node.unstash()
        self.enable()
        for child in self.children:
            child.unstash()

    def clean_up(self):
        self.unstash()
        self._object.clean_up()
        self._node.remove_node()

    @property
    def x(self):
        return self._node.get_x()

    @property
    def y(self):
        return self._node.get_y()

    @property
    def z(self):
        return self._node.get_z()

    @property
    def pos(self):
        return self._node.get_pos()

    @property
    def heading(self):
        return self._node.get_h()

    @property
    def pitch(self):
        return self._node.get_p()

    @property
    def roll(self):
        return self._node.get_r()

    @property
    def hpr(self):
        return self._node.get_hpr()

    @property
    def scale_x(self):
        return self._node.get_sx()

    @property
    def scale_y(self):
        return self._node.get_sy()

    @property
    def scale_z(self):
        return self._node.get_sz()

    @property
    def scale(self):
        return self._node.get_scale()

    @property
    def shear_x(self):
        return self._node.get_shxy()

    @property
    def shear_y(self):
        return self._node.get_shyz()

    @property
    def shear_z(self):
        return self._node.get_sz()


Node = SaturnNode


class SaturnNode2D(SaturnNode):
    def __init__(self, name):
        super().__init__(name, parent=window.render2d)


Node2D = SaturnNode2D


class Skeleton(SaturnNode):
    def __init__(self):
        super().__init__("")
        self._actor = Actor()
        self._actor.reparent_to(self._node)


class Terrain(SaturnNode):
    def __init__(self):
        super().__init__("")


class Physical(SaturnNode):
    def __init__(self):
        super().__init__("")


class TriggerBox(SaturnNode):
    def __init__(self):
        super().__init__("")
