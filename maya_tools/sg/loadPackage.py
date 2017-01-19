import maya.cmds as cmds

try:
	cmds.evalDeferred( 'import sg.Menu_mainMenu' )
	cmds.evalDeferred( 'sg.Menu_mainMenu.create()')
	cmds.evalDeferred( 'import sg.Menu_popup' )
	cmds.evalDeferred( 'sg.Menu_popup.create()')
	cmds.evalDeferred( 'import sg.Function_autoRig' )
	cmds.evalDeferred( 'sg.Function_autoRig.popupCreate()')
except:pass