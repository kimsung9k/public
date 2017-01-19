import checkMesh_info
import checkMesh_core



def getCrossedUVIds( meshName, select=True ):
    
    infoMesh = checkMesh_info.Info_mesh( meshName )
    infoMesh.getUVs_Info()
    
    crossUVIds = []
    for uvInfo in infoMesh.uvInfos:
        
        if uvInfo.uvSetName != infoMesh.fnMesh.currentUVSetName(): continue
        
        inst = checkMesh_core.Core_UVs( uvInfo.uArrays, uvInfo.vArrays, uvInfo.polygon_to_uvs_map )
        crossUVIds += inst.getCrossedUVsAll( infoMesh.numPolygons )
    
    if select:
        import maya.cmds as cmds
        selTargets = []
        for i in crossUVIds:
            selTargets.append( meshName + '.map[%d]' % i )
        cmds.select( selTargets )
    
    return crossUVIds




def getTwistedFaceIds( meshName, select=True ):
    
    infoMesh = checkMesh_info.Info_mesh( meshName )
    infoMesh.getMeshComponentRelationInfo()
    
    inst = checkMesh_core.Core_Mesh( infoMesh.points, 
                           infoMesh.polygon_to_vertices_map )
    
    twistedPolygonIds = []
    for polygonId in range( infoMesh.numPolygons ):
        if not inst.isTwistedFace( polygonId ): continue
        twistedPolygonIds.append( polygonId )
    
    if select:
        import maya.cmds as cmds
        selTargets = []
        for i in twistedPolygonIds:
            selTargets.append( meshName + '.f[%d]' % i )
        cmds.select( selTargets )
    
    return twistedPolygonIds




def getWeldVertexIds( meshName, select=True ):
    
    infoMesh = checkMesh_info.Info_mesh( meshName )
    infoMesh.getMeshComponentRelationInfo()
    
    inst = checkMesh_core.Core_Mesh( infoMesh.points, 
                           infoMesh.polygon_to_vertices_map,
                           infoMesh.polygon_to_edges_map,
                           infoMesh.edge_to_polygons_map,
                           infoMesh.vertex_to_edges_map )
    weldVertexIds = []
    for vertexId in range( infoMesh.numVertices ):
        if not inst.isWeldVertex( vertexId ): continue
        weldVertexIds.append( vertexId )
    
    if select:
        import maya.cmds as cmds
        targetVertexNames = []
        for weldVertex in weldVertexIds:
            targetVertexNames.append( meshName + '.vtx[%d]' % weldVertex )
        cmds.select( targetVertexNames )
    
    return weldVertexIds



def getCloseVerticeIds( meshName, select=True, tol=0.001 ):
    
    infoMesh = checkMesh_info.Info_mesh( meshName )
    inst = checkMesh_core.Core_Mesh( infoMesh.points )
    
    ids = inst.getClosestVerticesIds( infoMesh.boundingBox, tol )
    
    if select:
        import maya.cmds as cmds
        vtxNames = []
        for i in ids:
            vtxNames.append( meshName + '.vtx[%d]' % i )
        cmds.select( vtxNames )
    
    return ids