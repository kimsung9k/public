

def createBlendTargetGroupByController():
    
    import maya.cmds as cmds

    targetMeshGrp = 'RIG_g'
    targetBlendShape = 'bl_FaceAll'
    
    bbmin = cmds.getAttr( targetMeshGrp + '.boundingBoxMin' )[0]
    bbmax = cmds.getAttr( targetMeshGrp + '.boundingBoxMax' )[0]
    
    addTx = -(bbmax[0] - bbmin[0] + 0.2 )
    addTy = -(bbmax[1] - bbmin[0] + 0.2 )
    
    ctls = cmds.ls( 'Ctl_*', type='transform' )
    
    setValueList = [["Ctl_Jaw.forceLipsTogether",1],
                    ["Ctl_MouthMove.shrink_L_",1],
                    ["Ctl_MouthMove.shrink_R_",1],
                    ["Ctl_MouthMove.puff",1],
                    ["Ctl_MouthMove.chinUpperRaise",1],
                    ["Ctl_MouthMove.chinLowerRaise",1],
                    ["Ctl_MouthMove.lipsPucker",1],
                    ["Ctl_MouthMove.lipsFunnel",1]]
    for ctl in ctls:
        etys = cmds.transformLimits( ctl, q=1, ety=1 )
        etxs = cmds.transformLimits( ctl, q=1, etx=1 )
        tys = cmds.transformLimits( ctl, q=1, ty=1 )
        txs = cmds.transformLimits( ctl, q=1, tx=1 )
        
        for i in range( len( etys ) ):
            if not etys[i]: continue
            if not tys[i]: continue
            setValueList.append( [ctl + '.ty', tys[i]] )
        
        for i in range( len( etys ) ):
            if not etxs[i]: continue
            if not txs[i]: continue
            setValueList.append( [ctl + '.tx', txs[i]] )
    
    for attr, value in setValueList:
        cmds.setAttr( attr, value )
        weights = cmds.getAttr( targetBlendShape + '.weight' )[0]
        for i in range( len( weights ) ):
            if not weights[i]: continue
            attrName = cmds.ls( targetBlendShape + '.weight[%d]' % i )[0].split( '.' )[-1]
            tyMult, txMult = divmod( i, 6 )
            txValue = (txMult + 1) * addTx
            tyValue = (tyMult + 1) * addTy
            
            duObj = cmds.duplicate( targetMeshGrp )[0]
            cmds.move( txValue, tyValue, 0, duObj )
            
            children = cmds.listRelatives( duObj, c=1, f=1 )
            for child in children:
                cmds.rename( child, child.split( '|' )[-1].replace( targetMeshGrp, attrName ) )
            cmds.rename( duObj, attrName )
            
        cmds.setAttr( attr, 0 )