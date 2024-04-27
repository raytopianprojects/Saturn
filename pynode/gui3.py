from nicegui import ui, app
from nicegui.events import KeyEventArguments
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, WindowProperties


class switch:
    switch = False


a: ShowBase = None


class Action:
    def __init__(self):
        actions.append(self)

    def undo(self):
        pass


actions: list[Action] = []


class AddModel(Action):
    def __init__(self, model_name):
        super().__init__()
        self.model_name: str = model_name
        self.model: NodePath = a.loader.load_model(self.model_name)
        self.model.reparent_to(a.render)

    def undo(self):
        self.model.remove_node()


def handle_keys(event: KeyEventArguments):
    if event.modifiers.ctrl and event.action.keydown:
        if event.key == "z":
            actions.pop().undo()


@ui.page('/')
def index_page():
    keyboard = ui.keyboard(on_key=handle_keys)

    with ui.tabs().classes('w-full') as tabs:
        game_settings = ui.tab('Game')
        level = ui.tab('Level')
        code = ui.tab('Code')
        shaders = ui.tab('Shaders')
        particles = ui.tab('Particles')
        audio = ui.tab('Audio')
        sequence = ui.tab('Sequence')
        database = ui.tab('Database')
        settings = ui.tab('Settings')

    with ui.tab_panels(tabs).classes('w-full'):
        with ui.tab_panel(level):
            ui.label('First tab')
            ui.button("Add Model", on_click=lambda: AddModel("panda"))
        with ui.tab_panel(code):
            ui.label('Second tab')
        with ui.tab_panel(shaders):
            select = ui.select([1, 2, 3], value=1)
            with ui.row():
                print(select.options)
                ui.button('4, 5, 6', on_click=lambda: select.set_options([4, 5, 6], value=4))
                ui.button('1, 2, 3', on_click=lambda: select.set_options([1, 2, 3], value=1))
        with ui.tab_panel(particles):
            pass
        with ui.tab_panel(audio):
            pass
        with ui.tab_panel(sequence):
            pass
        with ui.tab_panel(database):
            pass
        with ui.tab_panel(game_settings):
            pass
        with ui.tab_panel(settings):
            pass


def run():
    a.task_mgr.step()


def start_showbase():
    global a
    a = ShowBase()

    # make sure window is always ontop
    winprops = WindowProperties()
    winprops.setZOrder(WindowProperties.Z_top)
    a.win.requestProperties(winprops)


app.on_startup(start_showbase)
ui.timer(1 / 60, run)
ui.run(reload=False, native=True)
