using FlowFarm; const ff = FlowFarm
using PyPlot
#include("../src/optimization_functions.jl")

#-- Multi-turbine circular boundary as a square --#
function DiscreteCircum(center_x, center_y, r, n = 100)
    bndry_x = zeros(n+1)
    bndry_y = zeros(n+1)
    for i in 1:n+1
        bndry_x[i] = center_x + cos(2*pi/n*i)*r
        bndry_y[i] = center_y + sin(2*pi/n*i)*r
    end
    # Roll it to the right so it starts with first element on x-axis
    println(bndry_x)
    bndry_x = circshift(bndry_x, 1)#floor(Int, n*0.25))
    println(bndry_x)
    bndry_y = circshift(bndry_y, 1)#floor(Int, n*0.25))
    return bndry_x, bndry_y
end

# A discretized 20-point circle
num_pts = 4
circ_radius = 100.0
circ_center = [100.0, 100.0]
# # Irregular Boundary
# bndry_x_clsd = [200, 100, 50, 100, 50, 100, 200]
# bndry_y_clsd = [100, 200, 150, 100, 50, 0, 100]

# Simple 10-pt boundary
# A discretized 20-point circle
# bndry_x_clsd = [200.00, 195.11, 180.90, 158.78, 130.90, 100.00, 69.10, 41.22, 19.10, 4.89, 0.00, 4.89, 19.10, 41.22, 69.10, 100.00, 130.90, 158.78, 180.90, 195.11, 200.00]
# bndry_y_clsd = [100.00, 130.90, 158.78, 180.90, 195.11, 200.00, 195.11, 180.90, 158.78, 130.90, 100.00, 69.10, 41.22, 19.10, 4.89, 0.00, 4.89, 19.10, 41.22, 69.10, 100.00]
num_pts = 200
circ_radius = 100.0
circ_center = [100.0, 100.0]
bndry_x_clsd, bndry_y_clsd = DiscreteCircum(circ_center[1], circ_center[2], circ_radius, num_pts)

# Vertices that keep splines injective
# bndry_corner_indcies =[1,2,3,4,5] # 4pts
# bndry_corner_indcies =[1,3,5,7,9] # 8pts
# bndry_corner_indcies =[1,6,11,16, 21]     # 20 pts
# bndry_corner_indcies = [1, 3, 4, 5, 7]  # 100 pts
bndry_corner_indcies = [1, 51, 101, 151, 201]  # 200 pt circle, 4 corners

# Make a turbine grid inside the circle
# testing_x = [ 50, 100, 150,  50, 100, 150,  50, 100, 150]
# testing_y = [150, 150, 150, 100, 100, 100,  50,  50,  50]
# testing_x = [100.0]
# testing_y = [100.0]
# Vertices that keep splines injective
circ_corners = 1/sqrt(2)
cc_r = circ_center[2] + (circ_corners * circ_radius) # ~170
cc_l = circ_center[1] - (circ_corners * circ_radius) # ~ 30
cc_d = cc_r - cc_l                # ~140
cc_d2 = cc_d/2                    # ~ 70

testing_x = [cc_l, 100.0, cc_r, cc_l, 100.0, cc_r, cc_l, 100.0, cc_r]
testing_y = [cc_r, cc_r, cc_r, 100.0, 100.0, 100.0, cc_l, cc_l, cc_l]

test_values = [ cc_r  cc_l   0.0  cc_d
                100.0 100.0  cc_l  cc_r
                cc_l  cc_r   0.0  cc_d
                cc_r  cc_l cc_d2 cc_d2
                100.0 100.0 100.0 100.0
                cc_l  cc_r cc_d2 cc_d2
                cc_r  cc_l  cc_d   0.0
                100.0 100.0  cc_r  cc_l
                cc_l  cc_r cc_d    0.0]
test_values = [100.0 100.0 100.0 100.0]

#test_values = [ ]
# ans = ff.splined_boundary(testing_x, testing_y, bndry_x, bndry_y, bndry_corner_indcies)
# for i in 1:length(testing_x)
#     println(testing_x[i], " ", testing_y[i])
# end
# println()
# for i in 1:length(testing_x)
#     println(test_values[i,:])
# end
# println()
# for i in 1:length(testing_x)
#     println(ans[i,:])
# end
# ans = ff.splined_boundary(testing_x, testing_y, bndry_x_clsd, bndry_y_clsd, bndry_corner_indcies) #atol=1E-3
# print(size(ans))

# Plot the boundary
plot(bndry_x_clsd, bndry_y_clsd)

# Plot the turbines
for i in 1:length(testing_x)
    plot(testing_x, testing_y, "go")
end

#plot(bndry_x_clsd[1], bndry_y_clsd[1], "ro")
# Print the vertices
for i in 1:length(bndry_corner_indcies)
    plot(bndry_x_clsd[bndry_corner_indcies[i]],
             bndry_y_clsd[bndry_corner_indcies[i]], "ro")
end

axis("square")
axis("off")
show()