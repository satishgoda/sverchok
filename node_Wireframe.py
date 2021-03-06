import bmesh, mathutils
from mathutils import Vector, Matrix
from node_s import *
from util import *


def wireframe(vertices, faces, t,o,replace,boundary ,even_offset,relative_offset):

    if not faces or not vertices:
        return False
   
    if len(faces[0])==2:
        return False
                
    bm=bmesh.new() 
    bm_verts =[ bm.verts.new(v) for v in vertices]
    for face in faces:
        bm.faces.new([bm_verts[i] for i in face])
             
    
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    res=bmesh.ops.wireframe(bm, faces=bm.faces[:], thickness=t,offset=o,use_replace=replace, \
                            use_boundary=boundary,use_even_offset=even_offset, \
                            use_relative_offset=relative_offset)
    #bmesh.ops.wireframe(bm, faces, thickness, offset, use_replace, 
    #    use_boundary, use_even_offset, use_crease, crease_weight, thickness, use_relative_offset, material_offset)
    edges = []
    faces = []
    bm.verts.index_update()
    bm.edges.index_update()
    bm.faces.index_update()
    for edge in bm.edges[:]:
        edges.append([v.index for v in edge.verts[:]])
    verts = [vert.co[:] for vert in bm.verts[:]]
    for face in bm.faces:
        faces.append([v.index for v in face.verts[:]])
    bm.clear()
    bm.free()
    return (verts,edges,faces)


class SvWireframeNode(Node, SverchCustomTreeNode):
    '''Wireframe'''
    bl_idname = 'SvWireframeNode'
    bl_label = 'Wireframe'
    bl_icon = 'OUTLINER_OB_EMPTY'
    
    thickness = bpy.props.FloatProperty(name='thickness', description='thickness', min=0.0,default=0.01, update=updateNode)
    offset = bpy.props.FloatProperty(name='offset', description='offset',min=0.0, default=0.01, update=updateNode)
    
    replace = bpy.props.BoolProperty(name='replace', description='replace', default=True, update=updateNode)
    even_offset = bpy.props.BoolProperty(name='even_offset', description='even_offset', default=True, update=updateNode)
    relative_offset = bpy.props.BoolProperty(name='relative_offset',description='even_offset', default=False, update=updateNode)
    boundary = bpy.props.BoolProperty(name='boundary', description='boundry', default=True, update=updateNode)
    
    def init(self, context):
        self.inputs.new('VerticesSocket', 'vertices', 'vertices')
        self.inputs.new('StringsSocket', 'polygons', 'polygons')
        
        self.outputs.new('VerticesSocket', 'vertices', 'vertices')
        self.outputs.new('StringsSocket', 'edges', 'edges')
        self.outputs.new('StringsSocket', 'polygons', 'polygons')
                
    def draw_buttons(self, context, layout):
        layout.prop(self,'thickness',text="Thickness")
        layout.prop(self,'offset',text="Offset")
        layout.prop(self,'boundary',text="Boundary")
        layout.prop(self,'even_offset',text="Offset even")
        layout.prop(self,'relative_offset',text="Offset relative")
        layout.prop(self,'replace',text="Replace")

    def update(self):
        if not ('vertices' in self.outputs and self.outputs['vertices'].links or \
            'edges' in self.outputs and self.outputs['edges'].links or\
            'polygons' in self.outputs and self.outputs['polygons'].links):
            return
            
        if 'vertices' in self.inputs and self.inputs['vertices'].links and \
            'polygons' in self.inputs and self.inputs['polygons'].links:
                
       
            verts = Vector_generate(SvGetSocketAnyType(self,self.inputs['vertices']))
            polys = SvGetSocketAnyType(self,self.inputs['polygons'])
            

            verts_out = []
            edges_out = []
            polys_out = []
                     
            for obj in zip(verts,polys):
                res = wireframe(obj[0], obj[1], self.thickness,self.offset,
                                self.replace,self.boundary ,self.even_offset,self.relative_offset)
                if not res:
                    return
                verts_out.append(res[0])
                edges_out.append(res[1])
                polys_out.append(res[2])
             
            if 'vertices' in self.outputs and self.outputs['vertices'].links:
                SvSetSocketAnyType(self, 'vertices',verts_out)
            
            if 'edges' in self.outputs and self.outputs['edges'].links:
                SvSetSocketAnyType(self, 'edges',edges_out) 
                
            if 'polygons' in self.outputs and self.outputs['polygons'].links:
                SvSetSocketAnyType(self, 'polygons', polys_out) 
            
     

    def update_socket(self, context):
        self.update()

def register():
    bpy.utils.register_class(SvWireframeNode)   
    
def unregister():
    bpy.utils.unregister_class(SvWireframeNode)

if __name__ == "__main__":
    register()







