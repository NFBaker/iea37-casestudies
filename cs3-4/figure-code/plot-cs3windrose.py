from matplotlib.transforms import BlendedGenericTransform
from matplotlib import pyplot as plt
import numpy as np
# -*- coding: utf-8 -*-
# Create wind speed and direction variables

# For axis arrowheads. 
# Taken from <https://stackoverflow.com/questions/33737736/matplotlib-axis-arrow-tip>
def arrowed_spines(fig, ax):

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # removing the default axis on all sides:
    for side in ['bottom', 'right', 'top', 'left']:
        ax.spines[side].set_visible(False)

    # removing the axis ticks
    plt.xticks([])  # labels
    plt.yticks([])
    ax.xaxis.set_ticks_position('none')  # tick markers
    ax.yaxis.set_ticks_position('none')

    # get width and height of axes object to compute
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    hw = 1./20.*(ymax-ymin)
    hl = 1./20.*(xmax-xmin)
    lw = 1.  # axis line width
    ohg = 0.9  # arrow overhang

    # draw x and y axis
    ax.arrow(xmin, 0, xmax-xmin, 0., fc='k', ec='k', lw=lw,
             head_width=hw, head_length=hl, overhang=ohg,
             length_includes_head=True, clip_on=False)

    ax.arrow(0, ymin, 0., ymax-ymin, fc='k', ec='k', lw=lw+.2,
             head_width=hl, head_length=hw, overhang=ohg,
             length_includes_head=True, clip_on=False)
#--- End arrowhead code ---#

# Main
#if __name__ == "__main__":
color = (74./255., 145./255., 200./255.)  # For nice MATLAB blue
#color = [0, 0.4470, 0.7410]  # Blue
#color = [0.6350, 0.0780, 0.1840] # Red
#color = [0.9290, 0.6940, 0.1250]  # Yellow
cDeg = u"\u00b0"

wf = np.array([0.0312, 0.0260, 0.0255, 0.0253, 0.0297,
               0.0397, 0.0506, 0.0510, 0.0415, 0.0414,
               0.0522, 0.0634, 0.0706, 0.0723, 0.0697,
               0.0668, 0.0676, 0.0677, 0.0613, 0.0464])

# wf = np.array([0.0017, 0.0017, 0.0016, 0.0016, 0.0016, 0.0016, 0.0015, 0.0015,
#           0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0014, 0.0014,
#           0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014,
#           0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014,
#           0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014,
#           0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014,
#           0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014, 0.0014,
#           0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0016, 0.0016, 0.0016,
#           0.0016, 0.0016, 0.0017, 0.0017, 0.0017, 0.0017, 0.0018, 0.0018, 0.0018,
#           0.0019, 0.0019, 0.0019, 0.002, 0.002, 0.002, 0.0021, 0.0021, 0.0021, 0.0022,
#           0.0022, 0.0022, 0.0023, 0.0023, 0.0024, 0.0024, 0.0024, 0.0025, 0.0025,
#           0.0025, 0.0026, 0.0026, 0.0027, 0.0027, 0.0027, 0.0028, 0.0028, 0.0028,
#           0.0028, 0.0029, 0.0029, 0.0029, 0.0029, 0.0029, 0.003, 0.003, 0.003, 0.003,
#           0.003, 0.003, 0.003, 0.003, 0.0029, 0.0029, 0.0029, 0.0029, 0.0029, 0.0028,
#           0.0028, 0.0028, 0.0027, 0.0027, 0.0027, 0.0026, 0.0026, 0.0026, 0.0025,
#           0.0025, 0.0025, 0.0024, 0.0024, 0.0024, 0.0023, 0.0023, 0.0023, 0.0023,
#           0.0022, 0.0022, 0.0022, 0.0022, 0.0022, 0.0022, 0.0022, 0.0022, 0.0022,
#           0.0022, 0.0022, 0.0022, 0.0022, 0.0022, 0.0022, 0.0022, 0.0023, 0.0023,
#           0.0023, 0.0024, 0.0024, 0.0024, 0.0024, 0.0025, 0.0025, 0.0026, 0.0026,
#           0.0026, 0.0027, 0.0027, 0.0027, 0.0028, 0.0028, 0.0029, 0.0029, 0.0029,
#           0.003, 0.003, 0.0031, 0.0031, 0.0031, 0.0032, 0.0032, 0.0032, 0.0033, 0.0033,
#           0.0033, 0.0034, 0.0034, 0.0034, 0.0035, 0.0035, 0.0035, 0.0036, 0.0036,
#           0.0036, 0.0036, 0.0037, 0.0037, 0.0037, 0.0037, 0.0038, 0.0038, 0.0038,
#           0.0038, 0.0039, 0.0039, 0.0039, 0.0039, 0.0039, 0.0039, 0.0039, 0.004, 0.004,
#           0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004,
#           0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004,
#           0.004, 0.004, 0.004, 0.004, 0.0039, 0.0039, 0.0039, 0.0039, 0.0039, 0.0039,
#           0.0039, 0.0039, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038,
#           0.0038, 0.0038, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037,
#           0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037,
#           0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037, 0.0038,
#           0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038,
#           0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038, 0.0038,
#           0.0038, 0.0038, 0.0038, 0.0038, 0.0037, 0.0037, 0.0037, 0.0037, 0.0037,
#           0.0037, 0.0036, 0.0036, 0.0036, 0.0036, 0.0035, 0.0035, 0.0035, 0.0035,
#           0.0034, 0.0034, 0.0034, 0.0033, 0.0033, 0.0032, 0.0032, 0.0032, 0.0031,
#           0.0031, 0.003, 0.003, 0.0029, 0.0029, 0.0028, 0.0027, 0.0027, 0.0026, 0.0026,
#           0.0025, 0.0025, 0.0024, 0.0024, 0.0023, 0.0022, 0.0022, 0.0021, 0.0021,
#           0.002, 0.002, 0.0019, 0.0019, 0.0019, 0.0018, 0.0018, 0.0017]

fCirc = 2*np.pi
wf = wf/sum(wf)          # Normalize so it totals to one
#wf = wf/max(wf)          # Normalize so it's a percentage
nDir = len(wf)           # Get the number of wind directions
ws = np.ones(nDir)   # Make all Wind Speeds the same
wd = np.linspace(0., (fCirc)-(fCirc/nDir), nDir)  # Make the Wind Directions correct

bottom = 0  # Make the bars go to the center
width = (fCirc-1) / nDir

# Windrose Plot
sub1 = plt.subplot(111, polar=True)
sub1 = plt.subplot(121, polar=True)
bars = sub1.bar(wd, wf*ws, width=width, bottom=bottom, color=color)
xlabels = ('0'+cDeg,
            '', '', '', '',
            '90'+cDeg,
            '', '', '', '',
            '180'+cDeg,
            '', '', '', '',
            '270'+cDeg,
            '', '', '', '',
            '180'+cDeg,
            '', '', '', '')      # Make the Wind Directions correct

xticks = np.linspace(0., (fCirc)-(fCirc/nDir), nDir)
plt.gca().set_theta_direction(-1)
plt.gca().set_theta_zero_location("N")
plt.gca().set_xticks(xticks)
plt.gca().set_xticklabels(xlabels, fontsize=10)

#plt.gca().set_axisbelow(True) # Puts the gridlines behind the image
plt.gca().set_rgrids([.01, .0225, .035, .0475, .06], alpha=.02) #, angle=35.) # For bi-off
plt.gca().set_yticklabels(['0.01%','','0.035%','',''],fontsize=10,family='serif', alpha =1)

plt.gca().set_rlabel_position(20)  # get radial labels away from plotted line #132.5
#plt.title('IEA37 WFLO Case Study Wind Rose', y=1.09, fontsize=20, family='serif')

# Plot for X/Y axis
sub2 = plt.subplot(447)
sub2.spines['right'].set_visible(False)         # Take off the right bar
sub2.spines['top'].set_visible(False)           # Take off the top bar
plt.gca().set_aspect('equal', adjustable='box') # Make it an even square

sub2.axhline(linewidth=1.7, color="black")
sub2.axvline(linewidth=1.7, color="black")

# removing the axis ticks
plt.xticks([1])
plt.yticks([])

#plt.subplots_adjust(wspace=-2)


sub2.text(0.1, 0.995, r'$y$', transform=BlendedGenericTransform(sub2.transData, sub2.transAxes), ha='center')
sub2.text(.95, 0.1, r'$x$', transform=BlendedGenericTransform(sub2.transAxes, sub2.transData), va='center')
fig = plt.gcf()
arrowed_spines(fig, sub2)

plt.tight_layout()  # Keeps words in frame
#plt.savefig('iea37-windrose.pdf',transparent=True)
plt.show()
