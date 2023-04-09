import numpy as np

asdf = [[-0.5,  0.5], [0. , 0.5], [0., 0.], [-0.5,  0.5], [-0.5,  0. ], [0., 0.], [ 0.5, -0.5], [ 0. , -0.5], [0., 0.], [ 0.5, -0.5], [0.5, 0. ], [0., 0.], [-1., -1.], [-1. , -0.5], [-0.5, -0.5], [-1., -1.], [-0.5, -1. ], [-0.5, -0.5], [-1. , -0.5], [-0.5, -0.5], [-0.5,  0. ], [-1. , -0.5], [-1.,  0.], [-0.5,  0. ], [-1.,  0.], [-0.5,  0. ], [-0.5,  0.5], [-1.,  0.], [-1. ,  0.5], [-0.5,  0.5], [-1.,  1.], [-0.5,  1. ], [-0.5,  0.5], [-1.,  1.], [-1. ,  0.5], [-0.5,  0.5], [-0.5,  1. ], [-0.5,  0.5], [0. , 0.5], [-0.5,  1. ], [0., 1.], [0. , 0.5], [1., 1.], [1. , 0.5], [0.5, 0.5], [1., 1.], [0.5, 1. ], [0.5, 0.5], [1. , 0.5], [0.5, 0.5], [0.5, 0. ], [1. , 0.5], [1., 0.], [0.5, 0. ], [1., 0.], [ 1. , -0.5], [ 0.5, -0.5], [ 1., -1.], [ 0.5, -1. ], [ 0.5, -0.5], [ 1., -1.], [ 1. , -0.5], [ 0.5, -0.5], [ 0.5, -1. ], [ 0.5, -0.5], [ 0. , -0.5], [ 0.5, -1. ], [ 0., -1.], [ 0. , -0.5]]

last_pair = None
for ix in range(int(len(asdf) / 3)):
  a = asdf[(3 * ix)]
  b = asdf[(3 * ix)]
  c = asdf[(3 * ix)]
  for pair in [(a,b),(b,c),(c,a)]:
    distance = np.linalg.norm(np.array(pair[1]) - np.array(pair[0]))
    if distance > 1:
      print("EXCEEDS", ix, pair[0], pair[1])
