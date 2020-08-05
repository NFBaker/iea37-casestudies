using PyPlot

function PointsInCircum(center_x, center_y, r, n = 100)
    bndry_x = zeros(n+1)
    bndry_y = zeros(n+1)
    for i in 1:n+1
        bndry_x[i] = center_x + cos(2*pi/n*i)*r
        bndry_y[i] = center_y + sin(2*pi/n*i)*r
    end
    return bndry_x, bndry_y
end

num_pts = 200
radius = 100.0
center = [100.0, 100.0]
bndry_x, bndry_y = PointsInCircum(center[1], center[2], radius, num_pts)

# Make a turbine grid inside the circle
circ_corners = 1/sqrt(2)
cc_r = 100 + (circ_corners * 100)  # ~170
cc_l = 100 - (circ_corners * 100)  # ~ 30
cc_d = cc_r - cc_l                 # ~140
cc_d2 = cc_d/2                     # ~ 70

turbine_x = [cc_l, 100.0, cc_r, cc_l, 100.0, cc_r, cc_l, 100.0, cc_r]
turbine_y = [cc_r, cc_r, cc_r, 100.0, 100.0, 100.0, cc_l, cc_l, cc_l]

#vertexList = [0,2,4,6,8]
# vertexList = [0, 5, 10, 15, 20]  # 20 pts
# vertexList = [1, 26, 51, 76, 101]  # 100 pts
vertexList = [1, 51, 101, 151, 201]  # 100 pts
#vertexList = [0,10,16]
plot(bndry_x, bndry_y)
# Print the turbines
for i in 1:length(vertexList)
    plot(turbine_x, turbine_y, "go")
end
# Print the vertices
for i in 1:length(vertexList)
    plot(bndry_x[vertexList[i]],
             bndry_y[vertexList[i]], "ro")
end

axis("square")
axis("off")
show()

# np.savetxt('./discretized-circle-' + str(num_pts) +
#            '-x.csv', pointsArray[:,0], delimiter=',')
# np.savetxt('./discretized-circle-' + str(num_pts) +
#            '-y.csv', pointsArray[:,1], delimiter=',')

