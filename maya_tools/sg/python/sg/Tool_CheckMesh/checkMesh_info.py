import maya.OpenMaya as om


class Info_fnc:
    
    @staticmethod
    def sepPerFaceCounts( counts, ids ):
        returnValue = []
        startIndex = 0
        for i in range( len( counts ) ):
            count = counts[i]
            returnValue.append( ids[startIndex:startIndex+count] )
            startIndex += count
        return returnValue



class Info_UV:
    
    def __init__(self, fnMesh, uvSetName ):
        
        #------------------Get UV Info------------------
        self.uvSetName = uvSetName
        self.uArrays = om.MFloatArray()
        self.vArrays = om.MFloatArray()
        uvCounts = om.MIntArray()
        uvIds = om.MIntArray()
        
        fnMesh.getUVs( self.uArrays, self.vArrays, uvSetName )
        fnMesh.getAssignedUVs( uvCounts, uvIds, uvSetName )
        
        self.polygon_to_uvs_map = Info_fnc.sepPerFaceCounts( uvCounts, uvIds )



class Info_mesh:

    def __init__(self, meshName ):
        
        #---------Get MFnMesh------------
        selList = om.MSelectionList()
        selList.add( meshName )
        
        self.dagPath = om.MDagPath()
        selList.getDagPath( 0, self.dagPath )
        
        self.fnMesh = om.MFnMesh( self.dagPath )
        
        self.numVertices = self.fnMesh.numVertices()
        self.numEdges    = self.fnMesh.numEdges()
        self.numPolygons = self.fnMesh.numPolygons()
        
        self.points = om.MPointArray()
        self.fnMesh.getPoints( self.points )
        
        self.boundingBox = self.fnMesh.boundingBox()


    def getMeshComponentRelationInfo(self):
        
        self.itMeshVertex  = om.MItMeshVertex( self.dagPath )
        self.itMeshPolygon = om.MItMeshPolygon( self.dagPath )
        
        self.polygon_to_vertices_map = [ [] for i in range( self.numPolygons ) ]
        self.polygon_to_edges_map    = [ [] for i in range( self.numPolygons ) ]
        self.edge_to_vertices_map   = [ [] for i in range( self.numEdges ) ]
        self.edge_to_polygons_map   = [ [] for i in range( self.numEdges ) ]
        self.vertex_to_polygons_map  = [ [] for i in range( self.numVertices ) ]
        self.vertex_to_edges_map     = [ [] for i in range( self.numVertices ) ]
        
        vtxCounts = om.MIntArray()
        vtxIds  = om.MIntArray()
        self.fnMesh.getVertices( vtxCounts, vtxIds )        
        self.polygon_to_vertices_map = Info_fnc.sepPerFaceCounts( vtxCounts, vtxIds )
        
        edgeIds = om.MIntArray()
        polygonIds = om.MIntArray()
        
        while not self.itMeshPolygon.isDone():
            polygonId = self.itMeshPolygon.index()
            self.itMeshPolygon.getEdges( edgeIds )
            listEdgeIds   = [ edgeIds[i] for i in range( edgeIds.length() ) ]
            
            self.polygon_to_edges_map[polygonId] = listEdgeIds
            
            for edgeId in listEdgeIds:
                if not polygonId in self.edge_to_polygons_map[ edgeId ]:
                    self.edge_to_polygons_map[ edgeId ].append( polygonId )
            
            self.itMeshPolygon.next()
        
        while not self.itMeshVertex.isDone():
            vertexId = self.itMeshVertex.index()
            self.itMeshVertex.getConnectedEdges( edgeIds )
            self.itMeshVertex.getConnectedFaces( polygonIds )
            
            listEdgeIds = [ edgeIds[i] for i in range( edgeIds.length() ) ]
            listPolygonIds   = [ polygonIds[i] for i in range( polygonIds.length() ) ]
            
            self.vertex_to_edges_map[vertexId] = listEdgeIds
            self.vertex_to_polygons_map[vertexId] = listPolygonIds
            
            for edgeId in listEdgeIds:
                if not vertexId in self.edge_to_vertices_map[ edgeId ]:
                    self.edge_to_vertices_map[ edgeId ].append( vertexId )
            
            self.itMeshVertex.next()
        
    def getUVs_Info(self):
        
        self.uvInfos = []
        
        namesUVSets = []
        self.fnMesh.getUVSetNames( namesUVSets )
        
        for nameUVSet in namesUVSets:
            info_uv_inst = Info_UV( self.fnMesh, nameUVSet )
            self.uvInfos.append( info_uv_inst )