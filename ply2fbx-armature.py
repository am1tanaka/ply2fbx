import bpy
import os

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Operator
from io_mesh_ply import import_ply

class ImportPLY(bpy.types.Operator):
    """
    PLYをインポートして、 重複頂点を結合して、左下の倍率でスケーリングします。
    """
    bl_idname = "import.ply"
    bl_label = "Import PLY"

    # ImportHelper mixin class uses this
    filename_ext = ".ply"

    filter_glob = StringProperty(
            default="*.ply",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting = FloatProperty(
            name="Scale",
            description="Import Scaling",
            default=0.22,
            )

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        import_ply.load_ply(self.filepath)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        bpy.ops.mesh.remove_doubles()

        # 3D Cursor to zero
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.context.space_data.pivot_point = 'CURSOR'

        # scaling
        bpy.ops.transform.resize(value=(self.use_setting, self.use_setting, self.use_setting), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

####

class AutoWeight(bpy.types.Operator):
    """
    アーマチュア(BaseArmature.blend)と メッシュを自動的にウェイト設定します。
     事前にアーマチュアとメッシュを読み込んで重ねてから実行してください。
    """
    bl_idname = "armature.autoweight"
    bl_label = "Auto Weight"

    @classmethod
    def poll(cls, context):
        # armature and mesh neet to proc
        arm = [True for x in bpy.data.objects if x.type=='ARMATURE']
        mesh = [True for x in bpy.data.objects if x.type=='MESH']
        return (len(arm) > 0) and (len(mesh) > 0)

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=Fals)
        bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.select_by_type(type='MESH', extend=False)
        bpy.ops.object.select_by_type(type='ARMATURE', extend=True)

        SetActiveObject('ARMATURE')

        bpy.ops.object.parent_set(type='ARMATURE_AUTO')

        return {'FINISHED'}

####

def SetActiveObject(type):
    for obj in bpy.data.objects:
        if (obj.type == type):
            bpy.context.scene.objects.active = obj

def GetFileName(fpath):
    return os.path.splitext(bpy.path.basename(fpath))[0]


class ExportFBX(bpy.types.Operator):
    """
    PLYメッシュへのマテリアル設定と、 頂点カラーのテクスチャーを生成して、
    指定の場所とファイル名でFBXとPNGを出力します。
    """
    bl_idname = "export.fbxtexture"
    bl_label = "Export FBX and Texture"

    filename_ext = ".fbx"

    filter_glob = StringProperty(
            default="*.fbx",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    width = IntProperty(
            name="Texture Width",
            description="Texture Width",
            min=1, max=4096,
            default=512,
            )
    height = IntProperty(
            name="Texture Height",
            description="Texture Height",
            min=1, max=4096,
            default=512,
            )

    def execute(self, context):
        print(self.filepath)
        print(bpy.path.ensure_ext(filepath=self.filepath, ext='.png'))

        # テクスチャ生成
        self.makeTexture(context)

        # マテリアルの作成
        #self.makeMaterial(context)

        # テクスチャをマテリアルに割り当て

        # FBXエクスポート

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def makeTexture(self, context):
        # make image for texture
        fname = GetFileName(self.filepath)
        image = bpy.data.images.new(name=fname, width=self.width, height=self.height)
        bpy.data.screens['UV Editing'].areas[1].spaces[0].image = image

        # unwrap
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_by_type(type='MESH')
        SetActiveObject('MESH')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.uv.smart_project(island_margin=0.06)

        # bake bake_type='VERTEX_COLORS', bake_margin = 4
        bpy.context.scene.render.bake_type = 'VERTEX_COLORS'
        bpy.context.scene.render.bake_margin = 4
        bpy.ops.object.bake_image()

        # save PNG
        

# Save the baked image
#image.filepath_raw = "output.png"
#image.file_format = "PNG"
#image.save()

# Save the new model with the new UV channel
#ops.object.mode_set(mode='OBJECT')
#bpy.ops.export.three(filepath="output.json")


        # save
        # bpy.ops.image.save_as()

    def makeMaterial(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_by_type(type='MESH', extend=False)
        #bpy.ops.material.new()
        #bpy.ops.texture.new()
        #fname = bpy.path.basename(self.filepath)
        #bpy.data.textures[fname] = fname

class PanelPlyTool(View3DPanel, bpy.types.Panel):
    """Ply Convert Tool"""
    bl_idname = "VIEW3D_PT_ply_tool"
    bl_label = "Ply Tool"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator(ImportPLY.bl_idname, text="Import PLY")

        layout.operator(AutoWeight.bl_idname, text="Auto Weight")

        layout.operator(ExportFBX.bl_idname, text="Export FBX and Texture")

####


def register():
    bpy.utils.register_class(PanelPlyTool)
    bpy.utils.register_class(ImportPLY)
    bpy.utils.register_class(AutoWeight)
    bpy.utils.register_class(ExportFBX)

def unregister():
    bpy.utils.unregister_class(PanelPlyTool)
    bpy.utils.unregister_class(ImportPLY)
    bpy.utils.unregister_class(AutoWeight)
    bpy.utils.unregister_class(ExportFBX)


if __name__ == "__main__":
    register()
