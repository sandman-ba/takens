import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from numpy import pi


##############
# Parameters #
##############
tau = 2 # Delay
d = 2 # Dimension of point cloud


#####################
#  Data processing  #
#####################
data = pd.read_csv('data/eeg-data.csv')
data = data.iloc[5857:,:]
data = data.drop(columns = ['IndexId', 'Ref1', 'Ref2', 'Ref3', 'TS1', 'TS2', 'Channel1'])
data = data.reset_index()
data = data.iloc[750:800, :]
data['time'] = data.reset_index().index

#####################
# Values used often #
#####################
points = data.time.size - (tau*(d-1)) # Number of points
cloudx = data.Channel2[:points] # Point Cloud x
cloudy = data.Channel2[tau:] # Point Cloud y


########################
# Plotting Point Cloud #
########################
fig1, ax1 = plt.subplots(1, 1, figsize = (6.5, 5))
ax1.plot(cloudx, cloudy, 'o')
ax1.set_xlabel(r"\(x(t)\)")
ax1.set_ylabel(r"\(x(t + \tau)\)")

fig1.set_tight_layout(True)

################
# Saving plots #
################
fig1.savefig("figures/point-cloud-eeg.png")
