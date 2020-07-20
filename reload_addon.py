bl_info = {
    "name": "Reload Addon",
    "blender": (2, 83, 0),
    "category": "Development",
}

import bpy
from bpy.props import StringProperty
import time

class ReloadOperator(bpy.types.Operator):
    bl_idname = "wm.reload_addon"
    bl_label = "Reload Addon"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        prefs = context.preferences.addons[__name__].preferences

        if prefs.filepath == "" or prefs.name == "":
            print("Cannot reload addon, filepath or name not set.")
            return {'CANCELLED'}

        now = int(time.time())
        os.utime(bpy.path.abspath(prefs.filepath), (now, now))

        bpy.ops.preferences.addon_disable(module=prefs.name)
        bpy.ops.preferences.addon_enable(module=prefs.name)
        return {'RUNNING_MODAL'}


class ReloadPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    name = StringProperty(name="Addon name")

    filepath = StringProperty(
            name="__init__.py",
            subtype='FILE_PATH',
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name")
        layout.prop(self, "filepath")


def register():
    bpy.utils.register_class(ReloadOperator)
    bpy.utils.register_class(ReloadPreferences)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.active.keymaps["Window"]
    km.keymap_items.new('wm.reload_addon', 'F5', 'PRESS', repeat=False)


def unregister():
    bpy.utils.unregister_class(ReloadOperator)
    bpy.utils.unregister_class(ReloadPreferences)
