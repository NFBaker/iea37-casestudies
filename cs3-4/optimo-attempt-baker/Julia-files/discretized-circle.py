import math
import matplotlib.pyplot as plt
import numpy as np

pi = math.pi

def PointsInCircum(center_x, center_y, r, n=100):
    bndry_x = np.zeros(n+1)
    bndry_y = np.zeros(n+1)
    for i in range(0, n+1):
        bndry_x[i] = center_x + math.cos(2*pi/n*i)*r
        bndry_y[i] = center_y + math.sin(2*pi/n*i)*r
    return bndry_x, bndry_y

num_pts = 100
radius = 100
center = [100, 100]
bndry_x, bndry_y = PointsInCircum(center[0], center[1], radius, n=num_pts)

# Make a turbine grid
turb_grid = [3,3]
num_turbs = turb_grid[0] * turb_grid[1]
circ_corners = 1/np.sqrt(2)
cc_r = 100 + (circ_corners * 100)  # ~170
cc_l = 100 - (circ_corners * 100)  # ~ 30
cc_d = cc_r - cc_l                # ~140
cc_d2 = cc_d/2                    # ~ 70

turbine_x = [cc_l, 100.0, cc_r, cc_l, 100.0, cc_r, cc_l, 100.0, cc_r]
turbine_y = [cc_r, cc_r, cc_r, 100.0, 100.0, 100.0, cc_l, cc_l, cc_l]

# print(100-(math.cos(math.radians(45))*100))

#vertexList = [0,2,4,6,8]
# vertexList = [0, 5, 10, 15, 20]  # 20 pts
vertexList = [0, 25, 50, 75, 100]  # 100 pts
#vertexList = [0,10,16]
plt.plot(bndry_x, bndry_y)
# Print the turbines
for i in range(len(vertexList)):
    plt.plot(turbine_x, turbine_y, 'go')
# Print the vertices
for i in range(len(vertexList)):
    plt.plot(bndry_x[vertexList[i]],
             bndry_y[vertexList[i]], 'ro')

plt.axis("square")
plt.axis("off")
plt.show()

# np.savetxt('./discretized-circle-' + str(num_pts) +
#            '-x.csv', pointsArray[:,0], delimiter=',')
# np.savetxt('./discretized-circle-' + str(num_pts) +
#            '-y.csv', pointsArray[:,1], delimiter=',')

