from direct.showbase.ShowBase import ShowBase

window = ShowBase()

from direct.showbase.ShowBaseGlobal import base, render2d, aspect2d, globalClock, cvMgr, hidden

load_model = base.loader.load_model
load_sfx = base.loadSfx
load_music = base.loadMusic
jobs = base.jobMgr
tasks = base.task_mgr
builtin_board = base.bboard
render = base.render
clock = globalClock
configure = cvMgr

from panda3d.core import NodePath

nodes = {}


class Node(NodePath):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        nodes[self.node()] = self

        if "parent" in kwargs:
            if kwargs["parent"]:
                self.reparent_to(kwargs["parent"])
        else:
            self.reparent_to(render)

    @property
    def x(self):
        return self.get_x()

    @x.setter
    def x(self, value):
        self.set_x(value)

    @property
    def y(self):
        return self.get_y()

    @y.setter
    def y(self, value):
        self.set_y(value)

    @property
    def z(self):
        return self.get_z()

    @z.setter
    def z(self, value):
        self.set_z(value)

    @property
    def h(self):
        return self.get_h()

    @h.setter
    def h(self, value):
        self.set_h(value)

    @property
    def p(self):
        return self.p()

    @p.setter
    def p(self, value):
        self.set_p(value)

    @property
    def r(self):
        return self.get_r()

    @r.setter
    def r(self, value):
        self.set_r(value)

    @property
    def sx(self):
        return self.get_sx()

    @sx.setter
    def sx(self, value):
        self.set_sx(value)

    @property
    def sy(self):
        return self.sy()

    @sy.setter
    def sy(self, value):
        self.set_sy(value)

    @property
    def sz(self):
        return self.get_sz()

    @sz.setter
    def sz(self, value):
        self.set_sz(value)

    def clean_up(self):
        del nodes[self.node()]
        self.remove_node()

    def find(self, path: str):
        node = NodePath.find(self, path)

        if node in nodes:
            return nodes[node]
        else:
            return node

    def find_nodepath(self, path: str):
        return NodePath.find(self, path)

    def find_all_matches(self, path: str):
        nodepaths = NodePath.find_all_matches(self, path)

        found_nodes = []
        for node in nodepaths:
            if node.node() in nodes:
                found_nodes.append(nodes[node.node()])
            print(node, node in nodes)

        return found_nodes, nodepaths

    def find_all_nodepath_matches(self, path: str):
        return NodePath.find_all_matches(self, path)

    @property
    def children(self):
        return [nodes[child.node()] for child in NodePath.getChildren(self) if child.node() in nodes]

    @property
    def children_nodepaths(self):
        return self.get_children()

    def parent(self):
        parent_node = NodePath.get_parent(self).node()
        return nodes[NodePath.get_parent(self).node()] if parent_node in nodes else NodePath.get_parent(self)


from direct.showbase.DirectObject import DirectObject


class Mob(Node, DirectObject):
    def __init__(self, name: str, update=NotImplemented, active=True, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self._listening = {}
        self._tasks = {}

        self.update = update

        if self.update != NotImplemented:
            self.add_task(self.update)

        self.active = active

        if not self.active:
            self.disable()

    def add_task(self, funcOrTask, name=None, sort=None, extraArgs=None, priority=None, appendTask=False,
                 uponDeath=None, taskChain=None, delay=None):
        DirectObject.add_task(self, funcOrTask,
                              name=None,
                              sort=None,
                              extraArgs=None,
                              priority=None,
                              appendTask=False,
                              uponDeath=None,
                              taskChain=None,
                              delay=None)
        self._tasks[funcOrTask] = ([name, sort, extraArgs, priority, appendTask, uponDeath, taskChain,
                                    delay])

    def accept(self, event, method, extraArgs=None):
        DirectObject.accept(self, event, method, extraArgs=extraArgs)

        self._listening["event"] = [method, extraArgs]

    def disable(self):
        self.active = False
        self.ignore_all()
        self.remove_all_tasks()

    def enable(self):
        self.active = True
        for event, values in self._listening.items():
            self.accept(event, values[0], values[1])

        for funcOrTask, values in self._tasks.items():
            self.add_task(funcOrTask, *values)

    def toggle(self):
        if self.active:
            self.disable()
        else:
            self.enable()

    def clean_up(self):
        Node.clean_up(self)

        del self._listening
        del self._tasks

        self.ignore_all()
        self.remove_all_tasks()


from direct.actor.Actor import Actor


class Skeleton(Mob):
    def __init__(self, name: str, model: str, update=NotImplemented, active=True, anims=None, *args, **kwargs):
        super().__init__(name=name, update=update, active=active, *args, **kwargs)
        self._actor = Actor(model, anims=anims)
        self._actor.reparent_to(self)

        self.attach = self._actor.attach
        self.loop = self._actor.loop
        self.play = self._actor.play
        self.stop = self._actor.stop
        self.pose = self._actor.pose
        self.get_num_frames = self._actor.get_num_frames
        self.animation_controller = self._actor.getAnimControl
        self.enable_blend = self._actor.enable_blend
        self.disable_blend = self._actor.disable_blend
        self.blend_amount = self._actor.set_control_effect
        self.set_blend = self._actor.set_blend
        self.sub_part = self._actor.make_subpart
        self.joints = self._actor.list_joints

        self.joints_nodes: dict[str, NodePath] = {}
        self.control_nodes: dict[str, NodePath] = {}

    def parent_to_joint(self, node, joint_name: str, model_node: str = "modelRoot"):
        if joint_name not in self.joints_nodes:
            self.joints_nodes[joint_name] = self._actor.expose_joint(None, model_node, joint_name)

        node.reparent_to(self.joints_nodes[joint_name])

    def control_joint(self, node, joint_name: str, model_node: str = "modelRoot"):
        if joint_name not in self.control_nodes:
            self.control_nodes[joint_name] = self._actor.control_joint(None, model_node, joint_name)

        self.control_nodes[joint_name].reparent_to(node)

    def release_joint(self, joint_name: str, model_node: str = "modelRoot"):
        self._actor.release_joint(model_node, joint_name)

    @property
    def play_rate(self, animation_name=None, part_name=None):
        return self._actor.get_play_rate(animation_name, part_name)

    @play_rate.setter
    def play_rate(self, value: tuple):
        self._actor.set_play_rate(value[0], value[1])

    def clean_up(self):
        Skeleton.clear(self)
        self._actor.cleanup()


from panda3d.core import LODNode, FadeLODNode


class Lod(Node):
    def __init__(self, name: str,fades=False, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        if not fades:
            self._lod_node = LODNode()
        else:
            self._lod_node = FadeLODNode()
        self._lod_node_path = NodePath(self._lod_node)
        self._lod_node_path.reparent_to(self)

    def add_level(self, closest: float, furthest: float):
        self._lod_node.add_switch(furthest, closest)

    @property
    def center(self):
        return self._lod_node.get_center()

    @center.setter
    def center(self, value):
        self._lod_node.set_center(value)



if __name__ == "__main__":
    node_1 = Node("A")
    node_2 = Node("B")
    node_3 = Node("C")
    node_3.reparent_to(node_2)
    node_4 = Node("C")
    node_4.reparent_to(node_2)

    print(nodes, "Nodes")

    print(node_2.find("C"), "find")
    print(node_2.find_all_matches("C"), "findall")

    print(node_2.children, node_2.get_children(), "CHILDREN")

    node_2.clean_up()

    print(node_1.x)
    node_1.x += 10
    node_1.x += 20

    print(node_1.x)


    async def move(mob, task):
        print("MOVING")
        await task.pause(1)

        if mob.x > 1000:
            mob.x -= 100
        else:
            mob.x += 100

        mob.h += 10

        return task.cont


    mob_1 = Mob("HI", update=lambda task: move(mob_1, task))
    load_model("teapot").reparent_to(mob_1)

    skeleton = Skeleton("Hi", "panda-model", anims={"walk": "models/panda-walk4"})
    skeleton.ls()
    skeleton.joints()
    skeleton.loop("walk")

    skeleton.parent_to_joint(load_model("teapot"), "Dummy_lr_foot_toe")
    skeleton.control_joint(mob_1, "Bone_neck")


    async def pause(task):
        print("WAITING")
        mob_1.disable()
        await task.pause(1)
        mob_1.enable()
        print("START")
        await task.pause(1)
        return task.cont


    tasks.add(pause)

    window.run()
