from __future__ import print_function   # For Python 3 compatibility
import numpy as np
import sys
import yaml
from math import radians as DegToRad    # For converting degrees to radians
import matplotlib.pyplot as plt # For Debug
from disk_grid_regular_count import disk_grid_regular_count # For validation
from disk_grid_regular import disk_grid_regular # for validation
from matplotlib import cm                   # For plotting colormap
from collections import OrderedDict         # For plotting colormap
"""IEA Task 37 Combined Case Study AEP Calculation Code

Written by Nicholas F. Baker, PJ Stanley, and Jared Thomas (BYU FLOW lab)
Created 10 June 2018
Updated 11 Jul 2018 to include read-in of .yaml turb locs and wind freq dist.
Completed 26 Jul 2018 for commenting and release
Modified 22 Aug 2018 implementing multiple suggestions from Erik Quaeghebeur:
    - PEP 8 adherence for blank lines, length(<80 char), var names, docstring.
    - Altered multiple comments for clarity.
    - Used print_function for compatibility with Python 3.
    - Used structured datatype (coordinate) and recarray to couple x,y coords.
    - Removed unused variable 'sWindRose' (getTurbLocYAML).
    - Removed unecessary "if ... < 0" case (WindFrame).
    - Simplified calculations for sin/cos_wind_dir (WindFrame).
    - Eliminated unecessary calculation of 0 values (GaussianWake, DirPower).
    - Turbine diameter now drawn from <.yaml> (GaussianWake)
    - Used yaml.safe_load.
    - Modified .yaml reading syntax for brevity.
    - Removed some (now) unused array initializations.
"""
# Structured datatype for holding coordinate pair
coordinate = np.dtype([('x', 'f8'), ('y', 'f8')])


def WindFrame(turb_coords, wind_dir_deg):
    """Convert map coordinates to downwind/crosswind coordinates."""

    # Convert from meteorological polar system (CW, 0 deg.=N)
    # to standard polar system (CCW, 0 deg.=W)
    # Shift so North comes "along" x-axis, from left to right.
    wind_dir_deg = 270. - wind_dir_deg
    # Convert inflow wind direction from degrees to radians
    wind_dir_rad = DegToRad(wind_dir_deg)

    # Constants to use below
    cos_dir = np.cos(-wind_dir_rad)
    sin_dir = np.sin(-wind_dir_rad)
    # Convert to downwind(x) & crosswind(y) coordinates
    frame_coords = np.recarray(turb_coords.shape, coordinate)
    frame_coords.x = (turb_coords.x * cos_dir) - (turb_coords.y * sin_dir)
    frame_coords.y = (turb_coords.x * sin_dir) + (turb_coords.y * cos_dir)

    return frame_coords


def GaussianWake(frame_coords, turb_diam):
    """Return each turbine's total loss due to wake from upstream turbines"""
    # Equations and values explained in <iea37-wakemodel.pdf>
    num_turb = len(frame_coords)

    # Constant thrust coefficient
    CT = 4.0*1./3.*(1.0-1./3.)
    # Constant, relating to a turbulence intensity of 0.075
    k = 0.0324555
    # Array holding the wake deficit seen at each turbine
    loss = np.zeros(num_turb)

    for i in range(num_turb):            # Looking at each turb (Primary)
        loss_array = np.zeros(num_turb)  # Calculate the loss from all others
        for j in range(num_turb):        # Looking at all other turbs (Target)
            x = frame_coords.x[i] - frame_coords.x[j]   # Calculate the x-dist
            y = frame_coords.y[i] - frame_coords.y[j]   # And the y-offset
            if x > 0.:                   # If Primary is downwind of the Target
                sigma = k*x + turb_diam/np.sqrt(8.)  # Calculate the wake loss
                # Simplified Bastankhah Gaussian wake model
                exponent = -0.5 * (y/sigma)**2
                radical = 1. - CT/(8.*sigma**2 / turb_diam**2)
                loss_array[j] = (1.-np.sqrt(radical)) * np.exp(exponent)
            # Note that if the Target is upstream, loss is defaulted to zero
        # Total wake losses from all upstream turbs, using sqrt of sum of sqrs
        loss[i] = np.sqrt(np.sum(loss_array**2))

    return loss


def DirPower(turb_coords, wind_dir_deg, wind_speed,
             turb_diam, turb_ci, turb_co, rated_ws, rated_pwr):
    """Return the power produced by each turbine."""
    num_turb = len(turb_coords)

    # Shift coordinate frame of reference to downwind/crosswind
    frame_coords = WindFrame(turb_coords, wind_dir_deg)
    
    # Use the Simplified Bastankhah Gaussian wake model for wake deficits
    loss = GaussianWake(frame_coords, turb_diam)
    # Effective windspeed is freestream multiplied by wake deficits
    wind_speed_eff = wind_speed*(1.-loss)
    # By default, the turbine's power output is zero
    turb_pwr = np.zeros(num_turb)

    # Check to see if turbine produces power for experienced wind speed
    for n in range(num_turb):
        # If we're between the cut-in and rated wind speeds
        if ((turb_ci <= wind_speed_eff[n])
                and (wind_speed_eff[n] < rated_ws)):
            # Calculate the curve's power
            turb_pwr[n] = rated_pwr * ((wind_speed_eff[n]-turb_ci)
                                       / (rated_ws-turb_ci))**3
        # If we're between the rated and cut-out wind speeds
        elif ((rated_ws <= wind_speed_eff[n])
                and (wind_speed_eff[n] < turb_co)):
            # Produce the rated power
            turb_pwr[n] = rated_pwr

    # Sum the power from all turbines for this direction
    pwrDir = np.sum(turb_pwr)

    return pwrDir


def calcAEP(turb_coords, wind_freq, wind_speed, wind_dir,
            turb_diam, turb_ci, turb_co, rated_ws, rated_pwr):
    """Calculate the wind farm AEP."""
    num_bins = len(wind_freq)  # Number of bins used for our windrose

    #  Power produced by the wind farm from each wind direction
    pwr_produced = np.zeros(num_bins)
    # For each wind bin
    for i in range(num_bins):
        # Find the farm's power for the current direction
        pwr_produced[i] = DirPower(turb_coords, wind_dir[i], wind_speed,
                                   turb_diam, turb_ci, turb_co,
                                   rated_ws, rated_pwr)

    #  Convert power to AEP
    hrs_per_year = 365.*24.
    AEP = hrs_per_year * (wind_freq * pwr_produced)
    AEP /= 1.E6  # Convert to MWh

    return AEP


def getTurbLocYAML(file_name):
    """ Retrieve turbine locations and auxiliary file names from <.yaml> file.

    Auxiliary (reference) files supply wind rose and turbine attributes.
    """
    # Read in the .yaml file
    with open(file_name, 'r') as f:
        defs = yaml.safe_load(f)['definitions']

    # Rip the x- and y-coordinates (Convert from <list> to <ndarray>)
    turb_xc = np.asarray(defs['position']['items']['xc'])
    turb_yc = np.asarray(defs['position']['items']['yc'])
    turb_coords = np.recarray(turb_xc.shape, coordinate)
    turb_coords.x, turb_coords.y = turb_xc, turb_yc

    # Rip the expected AEP, used for comparison
    # AEP = defs['plant_energy']['properties']
    #           ['annual_energy_production']['default']

    # Read the auxiliary filenames for the windrose and the turbine attributes
    ref_list_turbs = defs['wind_plant']['properties']['layout']['items']
    ref_list_wr = (defs['plant_energy']['properties']
                       ['wind_resource_selection']['properties']['items'])

    # Iterate through all listed references until we find the one we want
    # The one we want is the first reference not internal to the document
    # Note: internal references use '#' as the first character
    fname_turb = next(ref['$ref']
                      for ref in ref_list_turbs if ref['$ref'][0] != '#')
    fname_wr = next(ref['$ref']
                    for ref in ref_list_wr if ref['$ref'][0] != '#')

    # Return turbine (x,y) locations, and the filenames for the others .yamls
    return turb_coords, fname_turb, fname_wr


def getWindRoseYAML(file_name):
    """Retrieve wind rose data (bins, freqs, speeds) from <.yaml> file."""
    # Read in the .yaml file
    with open(file_name, 'r') as f:
        props = yaml.safe_load(f)['definitions']['wind_inflow']['properties']

    # Rip wind directional bins, their frequency, and the farm windspeed
    # (Convert from <list> to <ndarray>)
    wind_dir = np.asarray(props['direction']['bins'])
    wind_freq = np.asarray(props['probability']['default'])
    # (Convert from <list> to <float>)
    wind_speed = float(props['speed']['default'])

    return wind_dir, wind_freq, wind_speed


def getTurbAtrbtYAML(file_name):
    '''Retreive turbine attributes from the <.yaml> file'''
    # Read in the .yaml file
    with open(file_name, 'r') as f:
        defs = yaml.safe_load(f)['definitions']
        op_props = defs['operating_mode']['properties']
        turb_props = defs['wind_turbine_lookup']['properties']
        rotor_props = defs['rotor']['properties']

    # Rip the turbine attributes
    # (Convert from <list> to <float>)
    turb_ci = float(op_props['cut_in_wind_speed']['default'])
    turb_co = float(op_props['cut_out_wind_speed']['default'])
    rated_ws = float(op_props['rated_wind_speed']['default'])
    rated_pwr = float(turb_props['power']['maximum'])
    turb_diam = float(rotor_props['radius']['default']) * 2.

    return turb_ci, turb_co, rated_ws, rated_pwr, turb_diam

# --- BELOW FOR DEBUGGING --- #


def GWakeGrid(frame_coords, grid_frame_coords):
    """ Returns total loss from wakes at each grid point"""
    # Equations and values explained in <iea37-wakemodel.pdf>
    nTurbines = len(frame_coords.x)      # Get the number of turbines
    nPoints = len(grid_frame_coords.x)     # For the number for points we have

    CT = 4.0*1./3.*(1.0-1./3.)  # constant thrust coefficient
    k = 0.0324555   # constant turbulence

    D = 130.  # IEA37 3.35MW onshore reference turbine rotor diameter

    loss = np.zeros(nPoints) # store a loss for each grid point
    
    for i in range(nPoints):                # For every point we wish to evaluate at
        loss_array = np.zeros(nTurbines)    # Calculate the loss contribution from each turbine at that point
        for j in range(nTurbines):          # Loop through each turbine
            x = grid_frame_coords.x[i]-frame_coords.x[j]
            y = grid_frame_coords.y[i]-frame_coords.y[j]
            if x > 0.:  # Simplified Bastankhah Gaussian wake model, applied to downstream turbines
                sigma = k*(x)+D/np.sqrt(8.)
                loss_array[j] = (1.-np.sqrt(1.-CT/(8.*sigma**2/D**2)))*np.exp(-0.5*(y/sigma)**2)
            else:
                loss_array[j] = 0.
        # total wake loss, sqrt of sum of sqrs
        loss[i] = np.sqrt(np.sum(loss_array**2))

    return loss


def calcWindSpeeds(turb_coords, windFreq, windSpeed, windDir, testDirNum, gridPoints):
    """ Get the wind speeds at each point in the farm, for a single direction on windrose """
    testWindDir = np.array([1], dtype=float)
    testWindFreq = np.array([1], dtype=float)
    grid_coords = np.recarray(gridPoints[:,0].shape, coordinate)
    grid_coords.x = gridPoints[:, 0]
    grid_coords.y = gridPoints[:, 1]
    
    testWindDir[0] = windDir[testDirNum]
    testWindFreq[0] = windFreq[testDirNum]

    # turbines and evaluation points in wind frame coordinates
    frame_coords = WindFrame(turb_coords, testWindDir)
    grid_frame_coords = WindFrame(grid_coords, testWindDir)
    
    # Evaluate loss due to wakes at all points
    loss = GWakeGrid(frame_coords, grid_frame_coords)  # wake losses
    effWindSpeed = windSpeed*(1.-loss)
    effWindSpeed = effWindSpeed.reshape((-1, 1))
    # Store in 3rd column of speedMatrix
    speedMatrix = np.append(gridPoints, effWindSpeed, axis=1)

    return speedMatrix


def printWindSpeeds(turb_coords, windFreq, windSpeed, windDir, testDirNum, numTestDivs):
    # Make an array of all the points to test
    fieldRad = 1300.
    center = np.array([0.0, 0.0])
    ng = disk_grid_regular_count(numTestDivs, fieldRad, center) # Figures out the total number of points given the subdivisions (n)
    numGridPoints = disk_grid_regular(numTestDivs, fieldRad, center, ng) # returns the points for the given number of subdivisions (n)
    numGridPoints = np.transpose(numGridPoints)

    # Calculate windspeeds at all points in array (speedMatrix), with third column = windspeeds.
    speedMatrix = calcWindSpeeds(
        turb_coords, windFreq, windSpeed, windDir, testDirNum, numGridPoints)
    
    # Print Turbine Lcoations
    nNumTurb = 16  # 16 Turbine Farm
    rtrDiam = 130  # Diameter of NREL 3.35 MW turbine rotor
    colorNum = 0 # Should be 0-5 for different colors
    plotFarmSpeeds(turb_coords, rtrDiam, nNumTurb, fieldRad, colorNum, speedMatrix)

    return


def plotFarmSpeeds(turb_coords, rtrDiam, nNumTurb, fieldRad, cNum, speedMat):
    #color = (74./255., 145./255., 200./255.)  # For nice MATLAB blue
    color = np.empty(6, dtype='string')
    color[0] = 'blue'
    color[1] = 'red'
    color[2] = 'green'
    color[3] = 'yellow'
    color[4] = 'magenta'
    color[5] = 'cyan'

    plt.figure(1)
    # Print the windspeeds
    plt.scatter(speedMat[:, 0], speedMat[:, 1], c=speedMat[:, 2], marker='.', cmap='winter')

    # Print the Turbines
    for i in range(nNumTurb):
        circ_opt = plt.Circle((turb_coords.x[i]*1., turb_coords.y[i]*1.), rtrDiam/2.,
                              facecolor=color[cNum], edgecolor=color[cNum], alpha=0.5)
        plt.gca().add_patch(circ_opt)
    circ_outer = plt.Circle((0, 0), fieldRad, linestyle='dashed', edgecolor='black', facecolor='None', label='Boundaries')
    plt.gca().add_patch(circ_outer)

    plt.axis('equal')
    plt.axis('off')
    plt.title("16 Farm")
    plt.savefig("GaussianWakeField.pdf", transparent=True)
    plt.show()
    plt.gcf().clear()
# --- Above for debugging --- #

if __name__ == "__main__":
    """Used for demonstration.

    An example command line syntax to run this file is:

        python iea37-aepcalc.py iea37-ex16.yaml

    For Python .yaml capability, in the terminal type "pip install pyyaml".
    """
    # Read necessary values from .yaml files
    # Get turbine locations and auxiliary <.yaml> filenames
    turb_coords, fname_turb, fname_wr = getTurbLocYAML(sys.argv[1])
    # Get the array wind sampling bins, frequency at each bin, and wind speed
    wind_dir, wind_freq, wind_speed = getWindRoseYAML(fname_wr)
    # Pull the needed turbine attributes from file
    turb_ci, turb_co, rated_ws, rated_pwr, turb_diam = getTurbAtrbtYAML(fname_turb)

    # Calculate the AEP from ripped values
    AEP = calcAEP(turb_coords, wind_freq, wind_speed, wind_dir,
                  turb_diam, turb_ci, turb_co, rated_ws, rated_pwr)
    # Print AEP for each binned direction, with 5 digits behind the decimal.
    print(np.array2string(AEP, precision=5, floatmode='fixed',
                          separator=', ', max_line_width=62))
    # Print AEP summed for all directions
    print(np.around(np.sum(AEP), decimals=5))

    # --- Debug to print the different windspeeds on the farm --- #
    numTestPoints = 70  # How many points to sample across the farm
    testDirNum = 3 # 0-15, which wind direction bucket to test
    printWindSpeeds(turb_coords, wind_freq, wind_speed,
                    wind_dir, testDirNum,  numTestPoints)
    # --- End of Tests --- #
