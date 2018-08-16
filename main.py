import toolutils

head_height = 0.2

# create camera from current viewport
current_viewport = toolutils.sceneViewer().curViewport()
camera = hou.node('obj/').createNode('cam', 'cam')
camera.moveToGoodPosition()
current_viewport.saveViewToCamera(camera)
camera.setColor(hou.Color(.9, 0, 0))
current_viewport.setCamera(camera)

# set camera params
camera.parmTuple('res').set((2048, 858))
camera.parm('aperture').set(24.89);

# create head null
head_null = camera.createInputNode(0, 'null', 'head')

# head null params
head_null.parm('controltype').set('circles')
head_null.parm('geoscale').set('0.5')

# copy roration from camera to head null
head_null.parm('ty').set(camera.parm('ty').eval()-head_height)
head_null.parmTuple('r').set((camera.parm('rx').eval(), camera.parm('ry').eval(), camera.parm('rz').eval()))

# zeroing camera r params
camera.parmTuple('r').set((0, 0, 0))

# create tripod null
tripod_null = head_null.createInputNode(0, 'null', 'tripod')
tripod_null.parm('controltype').set('custom')

# create line geometry for tripod null
line_height = head_null.parm('ty').eval()
control_tripod = hou.node(tripod_null.path() + '/control1')
wrangle = control_tripod.createInputNode(0, 'attribwrangle', 'line')
wrangle.parm('snippet').set('int pt1 = addpoint(0, set(0, 0, 0)); \nint pt2 = addpoint(0, set(0, {}, 0)); \naddprim(0, \'polyline\', pt1, pt2);'.format('chf("../../{}/ty")'.format(head_null)))
wrangle.parm('class').set('detail')

# copy translation from camera to tripod null
tripod_null.parm('tx').set(camera.parm('tx').eval())
tripod_null.parm('tz').set(camera.parm('tz').eval())

# set head height to camera
camera.parmTuple('t').set((0, head_height, 0))

# lock unused parametrs
camera.parmTuple('t').lock((True, False, True))
camera.parmTuple('r').lock((True, True, True))
camera.parmTuple('p').lock((True, True, True))
camera.parmTuple('pr').lock((True, True, True))
head_null.parmTuple('t').lock((True, False, True))
head_null.parmTuple('s').lock((True, True, True))
head_null.parmTuple('p').lock((True, True, True))
head_null.parmTuple('pr').lock((True, True, True))
tripod_null.parmTuple('t').lock((False, True, False))
tripod_null.parmTuple('r').lock((True, True, True))
tripod_null.parmTuple('s').lock((True, True, True))
tripod_null.parmTuple('p').lock((True, True, True))
tripod_null.parmTuple('pr').lock((True, True, True))
