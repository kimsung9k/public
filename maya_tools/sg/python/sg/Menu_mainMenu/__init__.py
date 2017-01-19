import sg.ui


def create():
    
    import os
    toolPath =  __file__.split( 'python')[0]
    targetPath =  toolPath + "datas/menus"
    
    for root, dirs, names in os.walk( targetPath ):
        for directory in dirs:
            sg.ui.showMayaWindow( directory, root+'/'+directory )
        break