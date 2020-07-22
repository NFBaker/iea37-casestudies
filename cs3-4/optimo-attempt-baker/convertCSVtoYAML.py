from os import path
import numpy as np
import sys
import csv
import yaml
import baker_cs34_functions as Iea37sb
import iea37_aepcalc as iea37aepC

# Load necessary Files for AEP calculation
#- Load the turbine and windrose atributes -#
fname_turb = "../startup-files/iea37-10mw.yaml"
fname_wr = "../startup-files/iea37-windrose-cs3.yaml"
wind_dir, wind_dir_freq, wind_speeds, wind_speed_probs, num_speed_bins, min_speed, max_speed = iea37aepC.getWindRoseYAML(
    fname_wr)
turb_ci, turb_co, rated_ws, rated_pwr, turb_diam = iea37aepC.getTurbAtrbtYAML(
    fname_turb)
#- Make a dictionary for variable passing -#
dictParams = dict([('wind_dir_freq', wind_dir_freq),
                   ('wind_speeds', wind_speeds),
                   ('wind_speed_probs', wind_speed_probs),
                   ('wind_dir', wind_dir),
                   ('turb_diam', turb_diam),
                   ('fMinTurbDist', fMinTurbDist),
                   ('turb_ci', turb_ci),
                   ('turb_co', turb_co),
                   ('rated_ws', rated_ws),
                   ('rated_pwr', rated_pwr),
                   ('splineMatDict', splineMatDict),
                   ('coordsCornersDict', coordsCornersDict),
                   ('nRegionNumTurbs', nRegionNumTurbs)])

#- Necessary constants -#
nNumRegions = 5
x0l = []                        # Initialize our turbine <coord> list
nRunToRead = 14

# Read in the correct file
for i in range(nNumRegions):    # Loop through our regions
    PreStarts = np.loadtxt('./results/baker-cs3-bpm-snopt.csv', delimiter=',')
    x0l.extend(Iea37sb.makeArrayCoord(PreStarts[nRunToRead]))

x0 = Iea37sb.makeCoordListArray(x0l)
x0s = Iea37sb.makeArrayCoord(x0)
startAEP = Iea37sb.optimoFun(x0, dictParams)
print("Start AEP = " + str(startAEP*scaledAEP))  # *Args['fAEPscale']))
# Convert to correct format
# Write to a .yaml file.
