

def getPatternFromJsonFile( jsonFilePath ):
    
    import re, json

    f = open( jsonFilePath, 'r' )
    jsonObj = json.load( f )
    f.close()
    
    pattern = re.compile( '^[A-Z]\\w+(%s)\\d*_[a-z]\\w+(%s)\\d*_(%s)_(%s)$' 
                           %( '|'.join( jsonObj['head'] ), '|'.join( jsonObj['middle'] ), '|'.join( jsonObj['position'] ), '|'.join( jsonObj['type'] ) ) )
    return pattern




def getIncorrectNamesFromPattern( pattern ):
    
    import maya.cmds as cmds
    import re
    
    startupCams = []
    for cam in cmds.ls( ca=1 ):
        if not cmds.camera( cam, q=1, sc=1 ): continue
        startupCams += cmds.ls( cmds.listRelatives( cam, p=1, f=1 ) )
    
    trs = cmds.ls( tr=1 )
    
    incorrectNames = []
    for tr in trs:
        if tr in startupCams: continue
        match = re.search( pattern, tr )
        if match: continue
        incorrectNames.append( tr )
    
    return incorrectNames