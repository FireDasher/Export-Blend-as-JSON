bl_info = {
    "name": "Export To JSON",
    "author": "FireDasher22",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > N",
    "description": "Exports the current blend as a JSON file",
    "warning": "",
    "doc_url": "",
    "category": "",
}


import bpy
from bpy_extras.io_utils import ExportHelper
import json

def download(text, filepath):
    f = open(filepath, 'w', encoding='utf-8')
    f.write(text)
    f.close()
    return {'FINISHED'}

def main(filepath):
    cam = bpy.context.scene.camera
    jobj = {"materials": [], "faces": [], "camera": cam.location[:] + cam.rotation_euler[:]}
    
    for mat in bpy.data.materials:
        if hasattr(mat.node_tree, "nodes"):
            jobj["materials"].append(mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value[:])
        else:
            jobj["materials"].append(None)
    
    for obj in bpy.data.objects:
        if (obj.type != "MESH"):
            continue
        
        data = obj.data
        
        
        poly = data.polygons
        vert = data.vertices
        
        for f in poly:
            temp = []
            temp.append(bpy.data.materials[:].index(obj.material_slots[f.material_index].material))
            for idx in f.vertices:
                temp.append((obj.matrix_world @ vert[idx].co)[:])
            jobj["faces"].append(temp)
            
    download(json.dumps(jobj), filepath)

class popupOpp(bpy.types.Operator, ExportHelper):
    # ejp stans for Export JSON Panel
    bl_idname = "ejp.a"
    bl_label = "Export JSON"
    
    filename_ext = ".json"
    
    def execute(self, context):
        main(self.filepath)
        return {'FINISHED'}

class buttonOpp(bpy.types.Operator):
    bl_idname = "export.1"
    bl_label = "Export"

    def execute(self, context):
        bpy.ops.ejp.a("INVOKE_DEFAULT")
        return {'FINISHED'}

class panelClass(bpy.types.Panel):
    bl_label = "JSON Export"
    bl_idname = "OBJECT_PT_exportasjson"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JSON Export"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.operator(buttonOpp.bl_idname, text="Export as JSON", icon='EXPORT')

from bpy.utils import register_class, unregister_class

_classes = [
    buttonOpp,
    panelClass,
    popupOpp
]

def register():
    for cls in _classes:
        register_class(cls)

def unregister():
    for cls in _classes:
        unregister_class(cls)

if __name__ == "__main__":
    register()