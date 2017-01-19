

class BoundingBox2d:
    
    def __init__(self):
        
        self.minX = 10000000000.0
        self.maxX = -10000000000.0
        self.minY = 10000000000.0
        self.maxY = -10000000000.0


    def expand( self, xValue, yValue ):
        
        if xValue < self.minX: self.minX = xValue
        if xValue > self.maxX: self.maxX = xValue
        if yValue < self.minY: self.minY = yValue
        if yValue > self.maxY: self.maxY = yValue
    
    
    def isInBoundingBox(self, xValue, yValue ):
        
        if xValue <= self.minX: return False
        if xValue >= self.maxX: return False
        if yValue <= self.minY: return False
        if yValue >= self.maxY: return False
        return True




class Sector2d:
    
    def __init__(self, width, height ):
        
        self.__width  = width
        self.__sector = [ [] for i in range( width*height ) ]


    def append(self, x, y, value ):
        self.__sector[ self.__width * y + x ].append( value )
    
    
    def get(self, x, y ):
        return self.__sector[ self.__width * y + x ]
    
    
    def printLenSector(self):
        print len( self.__sector )
    
    
    

class Sector3d:
    
    def __init__(self, width, height, depth ):
        
        self.__width = width
        self.__height = height
        self.__sector = [ [] for i in range( width * height * depth )]
    
    
    def append(self, x, y, z, value ):
        self.__sector[ self.__width*self.__height*z + self.__width*y + x ].append( value )
        
    def get(self, x, y, z ):
        return self.__sector[ self.__width*self.__height*z + self.__width*y + x ]
    
    def printLenSector(self):
        print len( self.__sector )





class Core_UVs:
    
    def __init__(self, uArray, vArray, polygon_to_uvs_map ):
        
        self.uArray = uArray
        self.vArray = vArray
        self.polygon_to_uvs_map  = polygon_to_uvs_map


    def getCrossedUVs( self, polygonId, boundriIds ):
        
        import maya.OpenMaya as om
        
        uvIds = self.polygon_to_uvs_map[polygonId]
        points = []
        
        crossUVIds = []
        
        for uvId in uvIds:
            xValue = self.uArray[ uvId ]
            yValue = self.vArray[ uvId ]
            
            point = om.MVector( xValue, yValue, 0 )
            points.append( point )
        
        for i in boundriIds:
            
            if i in uvIds: continue
            
            xValue = self.uArray[i]
            yValue = self.vArray[i]
            
            cuPoint = om.MVector( xValue, yValue, 0.0 )
            
            isCross = True
            for j in range( len( points ) ):
                point1 = points[j-1]
                point2 = points[j]
                
                vector1 = cuPoint  - point1
                
                if vector1.length() == 0:
                    isCross = True
                    break
                
                vector2 = point2 - point1
                '''
                if vector1.normal() * vector2.normal() == 1:
                    isCross = True
                    break
                '''
                crossVector = vector1 ^ vector2
                
                if crossVector.z > 0:
                    isCross = False
                    break
            
            if isCross:
                crossUVIds.append( i )
        
        return crossUVIds
    
    
    def getCrossedUVsAll( self, numPolygon ):
        
        bb = BoundingBox2d()
        
        for i in range( len( self.vArray ) ):
            uValue = self.uArray[i]
            vValue = self.vArray[i]
            bb.expand( uValue, vValue )
        
        numUVs = len( self.vArray )
        
        xSize = bb.maxX - bb.minX
        ySize = bb.maxY - bb.minY
        
        allSize = xSize + ySize
        
        sectorNum = int( numUVs**0.65 )
        
        xWidth = int( sectorNum*xSize/allSize ) + 1
        yWidth = int( sectorNum*ySize/allSize ) + 1
        
        sector = Sector2d( xWidth, yWidth )
        sector.printLenSector()
        
        sectorInfo_per_uvs = [ [0,0] for i in range( numUVs ) ]
        
        for i in range( numUVs ):
            xValue = ( self.uArray[i]-bb.minX )/ xSize * ( xWidth-1 )
            yValue = ( self.vArray[i]-bb.minY )/ ySize * ( yWidth-1 )
            indexX = int( xValue )
            indexY = int( yValue )
            
            sector.append( indexX, indexY, i )
            
            if xValue < indexX + 0.001:
                sector.append( indexX-1, indexY, i )
            elif xValue > indexX + 0.999:
                sector.append( indexX+1, indexY, i )
            if yValue < indexY + 0.001:
                sector.append( indexX, indexY-1, i )
            elif yValue > indexY + 0.999:
                sector.append( indexX, indexY+1, i )
            
            sectorInfo_per_uvs[i][0] = indexX
            sectorInfo_per_uvs[i][1] = indexY
        
        returnUVIds = []
        for polygonId in range( numPolygon ):
            uvIds = self.polygon_to_uvs_map[polygonId]
            
            minIndexU = -1
            maxIndexU = -1
            minIndexV = -1
            maxIndexV = -1
            
            for uvId in uvIds:
                indexU, indexV = sectorInfo_per_uvs[ uvId ]
                if minIndexU == -1 or minIndexU > indexU:
                    minIndexU = indexU
                if maxIndexU == -1 or maxIndexU < indexU:
                    maxIndexU = indexU
                if minIndexV == -1 or minIndexV > indexV:
                    minIndexV = indexV
                if maxIndexV == -1 or maxIndexV < indexV:
                    maxIndexV = indexV
            
            boundriIds = []
            for indexU in range( minIndexU, maxIndexU + 1 ):
                for indexV in range( minIndexV, maxIndexV + 1 ):
                    boundriIds += sector.get( indexU, indexV )
            
            boundriIds = list( set( boundriIds ) )
            returnUVIds += self.getCrossedUVs( polygonId, boundriIds )
        
        return returnUVIds




class Core_Mesh:
    
    def __init__(self, points,
                 polygon_to_vertices_map = None,
                 polygon_to_edges_map = None,
                 edge_to_polygons_map = None,
                 vertex_to_edges_map = None ):
        
        self.points = points
        self.polygon_to_vertices_map     = polygon_to_vertices_map
        self.polygon_to_edges_map     = polygon_to_edges_map
        self.edge_to_polygons_map = edge_to_polygons_map
        self.vertex_to_edges_map = vertex_to_edges_map
        

    def isTwistedFace(self, polygonId ):
        
        import copy
        
        vtxIds = self.polygon_to_vertices_map[ polygonId ]
        
        point1 = self.points[ vtxIds[-2] ]
        point2 = self.points[ vtxIds[-1] ]
        point3 = self.points[ vtxIds[0] ]
        
        vector1 = point2 - point1
        vector2 = point3 - point2
        
        vectorCrossBase = vector2 ^ vector1 
        vectorCrossBase.normalize()
        
        vectorBefore = vector2
        for i in range( 1, len( vtxIds )-1 ):
            pointStart = self.points[ vtxIds[i-1] ]
            pointEnd   = self.points[ vtxIds[i] ] 
            
            vectorCurrent = pointEnd - pointStart;
            
            vectorCrossCurrent = vectorCurrent^vectorBefore
            vectorCrossCurrent.normalize()
            
            if vectorCrossBase*vectorCrossCurrent < -0.9:
                return True
            
            vectorBefore    = copy.copy( vectorCurrent )
            vectorCrossBase = copy.copy( vectorCrossCurrent )
        
        return False


    def isWeldVertex(self, vertexId ):
        
        connectedEdges = self.vertex_to_edges_map[ vertexId ]
        
        for edgeId in connectedEdges:
            if len( self.edge_to_polygons_map[edgeId] ) > 2:
                return True
        
        def getConnectedCircleEdges( targetEdge, boundriEdges, checkedEdges = [] ):
            checkedEdges.append( targetEdge )
            
            polygonIds = self.edge_to_polygons_map[ targetEdge ]
            
            for polygonId in polygonIds:
                edgeIds = self.polygon_to_edges_map[ polygonId ]
                for edgeId in edgeIds:
                    if not edgeId in boundriEdges: continue
                    if edgeId in checkedEdges: continue
                    getConnectedCircleEdges( edgeId, boundriEdges, checkedEdges )
            return checkedEdges
        
        connectedCircleEdges = getConnectedCircleEdges( connectedEdges[0], connectedEdges )
        
        if len( connectedCircleEdges ) != len( connectedEdges ): return True
        return False


    def getClosestVerticesIds(self, boundingBox, tol = 0.001 ):
        
        numVertices = self.points.length()
        points = self.points
        
        bb = boundingBox
        
        bbmin = bb.min()
        bbmax = bb.max()
        
        sectorNum = int( numVertices**0.5 )
        xSize = bbmax.x - bbmin.x
        ySize = bbmax.y - bbmin.y
        zSize = bbmax.z - bbmin.z
        
        allSize = xSize + ySize + zSize
        
        xWidth = int( sectorNum*xSize/allSize ) + 1
        yWidth = int( sectorNum*ySize/allSize ) + 1
        zWidth = int( sectorNum*zSize/allSize ) + 1
        
        sector = Sector3d( xWidth, yWidth, zWidth )
        sector.printLenSector()
        
        sectorInfo_per_points = [ [0,0,0] for i in range( numVertices ) ]
        
        for i in range( numVertices ):
            xValue = (points[i].x-bbmin.x )/ xSize * ( xWidth-1 )
            yValue = (points[i].y-bbmin.y )/ ySize * ( yWidth-1 )
            zValue = (points[i].z-bbmin.z )/ zSize * ( zWidth-1 )
            
            indexX = int( xValue )
            indexY = int( yValue )
            indexZ = int( zValue )
            
            sector.append( indexX, indexY, indexZ, i )
            
            sectorInfo_per_points[i][0] = indexX
            sectorInfo_per_points[i][1] = indexY
            sectorInfo_per_points[i][2] = indexZ
            
            if xValue < indexX + 0.001:
                sector.append( indexX-1, indexY, indexZ, i )
            elif xValue > indexX + 0.999:
                sector.append( indexX+1, indexY, indexZ, i )
            if yValue < indexY + 0.001:
                sector.append( indexX, indexY-1, indexZ, i )
            elif yValue > indexY + 0.999:
                sector.append( indexX, indexY+1, indexZ, i )
            if zValue < indexZ + 0.001:
                sector.append( indexX, indexY, indexZ-1, i )
            elif zValue > indexZ + 0.999:
                sector.append( indexX, indexY, indexZ+1, i )
        
        targetIds = []
        for i in range( numVertices ):
            indexX, indexY, indexZ,= sectorInfo_per_points[i]
            
            compairIds = list( set( sector.get( indexX, indexY, indexZ ) ) )
            
            for compairId in compairIds:
                if i == compairId: continue
                if points[i].distanceTo( points[compairId] ) < tol:
                    targetIds.append( compairId )
                    if not i in targetIds: targetIds.append( i )
        
        return targetIds