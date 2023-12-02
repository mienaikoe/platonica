import bpy

location='/Users/alice/Projects/platonica/code/game/models'
filename='octaherdron.py'

thingie = bpy.context.object.data

file = open('{}/{}'.format(location, filename), 'w')

file.write('vertex_palette = [\n')
for v in thingie.vertices:
    file.write('({}, {}, {}),\n'.format(v.co.x, v.co.y, v.co.z))
file.write(']\n\n')

file.write('face_vertices = [\n')
for face in thingie.polygons:
    v = face.vertices
    file.write('({}, {}, {}),\n'.format(v[0], v[1], v[2]))
file.write(']')


file.close()

