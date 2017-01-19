class ApiType:
    
    transform = ["kTransform", "kJoint"]
    shape = ["kMesh", "kNurbsCurve", "kNurbsSurface"]
    dag = []
    dag += transform
    shape += shape



class NodeType:
    
    transform = ['transform', 'joint']
    shape = ['mesh', 'nurbsCurve', 'nurbsSurface']
    dag = []
    dag += transform
    shape += shape