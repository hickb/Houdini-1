# Hou.Session
# Misc. Scripts

def FindAssets():
	'''Returns a list of HDAs in a given OTL file on disk.'''
    import os
    otlFile = "%s/Otls/stage.otl" % "D:/GitHub/Houdini/Study_and_Tests/Talented_Ball"
    for d in hou.hda.definitionsInFile(otlFile):
        print d.nodeTypeCategory().name() + "/" + d.nodeTypeName()

def FindLoadedAssets():
    '''Returns a list of loaded HDAs in Houdini scene.'''
    result = []
    for category in hou.nodeTypeCategories().values():
        for node_type in category.nodeTypes().values():
                d = node_type.definition()
                if d is None:
                        continue
                if d.libraryFilePath() not in result:
                        result.append(d.libraryFilePath())
    
    for r in result:
        if not r.startswith(hou.getenv("HFS")):
            print r

