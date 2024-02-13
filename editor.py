from direct.showbase.ShowBase import ShowBase
import dearpygui.dearpygui as dpg
from panda3d.core import *

load_prc_file_data("", """aspect-ratio 1.7777
win-size 960 540
red-blue-stereo 0
side-by-side-stereo 0
undecorated 0""")




def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


dpg.create_context()
dpg.create_viewport(title='Saturn Editor', )

render = dpg.tree_node(label="render")
render2d = dpg.tree_node(label="render2d")


def set_up_input(child, name):
    with dpg.tree_node(label=name):
        dpg.add_input_text(label="name", default_value=child.get_name())
        dpg.add_input_text(label="x", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_x(float(app_data)))
        dpg.add_input_text(label="y", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_y(float(app_data)))
        dpg.add_input_text(label="z", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_z(float(app_data)))
        dpg.add_input_text(label="h", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_h(float(app_data)))
        dpg.add_input_text(label="p", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_p(float(app_data)))
        dpg.add_input_text(label="r", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_r(float(app_data)))
        dpg.add_input_text(label="sx", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_sx(float(app_data)))
        dpg.add_input_text(label="sy", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_sy(float(app_data)))
        dpg.add_input_text(label="sz", default_value=0,
                           callback=lambda sender, app_data, user_data: child.set_sz(float(app_data)))
        dpg.add_input_text(label="shear x", default_value=0, callback=
        lambda sender, app_data, user_data: child.set_shear(
            (float(app_data), child.get_shear()[1], child.get_shear()[2])))
        dpg.add_input_text(label="shear y", default_value=0, callback=
        lambda sender, app_data, user_data: child.set_shear(
            (child.get_shear()[0], float(app_data), child.get_shear()[2])))
        dpg.add_input_text(label="shear z", default_value=0, callback=
        lambda sender, app_data, user_data: child.set_shear(
            (child.get_shear()[0], child.get_shear()[1], float(app_data))))

        node_type = type(child.node())
        if node_type is DirectionalLight:
            print("light")
        elif node_type is PointLight:
            ...
        elif node_type is Spotlight:
            ...
        elif node_type is AmbientLight:
            ...
        else:
            print(type(child.node()))


def scene_graph(parent):
    set_up_input(parent, parent.get_name())
    for child in parent.get_children():
        set_up_input(child, child.get_name())

        if len(child.get_children()) > 0:
            with dpg.tree_node(label="children"):
                for grandchild in child.get_children():
                    dpg.add_tree_node(label=grandchild.get_name())
                    scene_graph(grandchild)




levels = ["start"]
current_level = 0

database_data = {}


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()

window = ShowBase()
winprops = WindowProperties()
winprops.setZOrder(WindowProperties.Z_top)
window.win.requestProperties(winprops)

window.loader.load_model("panda").reparent_to(window.render)
a = DirectionalLight("HI")
an = window.render.attach_new_node(a)

with dpg.window(label="Example Window", autosize=True, no_close=True):
    with dpg.tab_bar():
        with dpg.tab(label='Game'):
            pass
        with dpg.tab(label="Level"):
            dpg.add_button(label="New Level", callback=lambda: (levels.append("new_level"), dpg.configure_item(combo, items=levels)))
            dpg.add_button(label="Duplicate Level", callback=lambda: (levels.append("new_level"), ))
            dpg.add_button(label="Delete Level", callback=lambda: (levels.append("new_level"), ))


            def callback(sender, app_data, user_data):
                print("Called on the main thread!")

            combo = dpg.add_combo(items=levels, default_value=levels[0])
            with render:
                scene_graph(base.render)
            with render2d:
                scene_graph(base.render2d)
        with dpg.tab(label='Shaders'):
            pass
        with dpg.tab(label='Particles'):
            pass
        with dpg.tab(label='Audio'):
            pass
        with dpg.tab(label='Sequence'):
            pass
        with dpg.tab(label='Database'):
            dpg.add_button(label="New Entity")
            with dpg.collapsing_header():
                dpg.add_button(label="Delete Entity")
                with dpg.table(header_row=False) as table:

                    # use add_table_column to add columns to the table,
                    # table columns use child slot 0
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        dpg.add_input_text(label="Appearance", default_value="panda")
                    # add_table_next_column will jump to the next row
                    # once it reaches the end of the columns
                    # table next column use slot 1
                    for i in range(0, 4):
                        with dpg.table_row():
                             dpg.add_input_text(label=f"Row{i} Column")

                dpg.add_button(label="New Data")
                dpg.add_input_text()


        with dpg.tab(label='Settings'):
            pass
with dpg.window(label="Properties", autosize=True,pos=(750,0), no_close=True):
    dpg.add_text("Properities")


# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    window.task_mgr.step()

    dpg.render_dearpygui_frame()

dpg.destroy_context()
