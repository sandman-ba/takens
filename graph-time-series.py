import numpy as np
import matplotlib.pyplot as plt
from numpy import pi
from numpy import linalg as LA
from math import comb as nCk
from itertools import combinations
from classicTakens import *


##############
# Parameters #
##############
T = 5
tau = 1 # Delay
d = 2 # Dimension of point cloud
e1 = 1.5 # Second scale
e2 = 2.0 # Third scale
betk = 1 # Dimension for Betti number
xi = 1.0 # Parameter for Dirac operator
def f(x): return np.sin((2.0*pi)*x) # Time series function


#####################
# Values used often #
#####################
points = T - (tau*(d-1)) # Number of points
time = np.linspace(0.0, 1.0, num=T, endpoint=True) # Time series times
series = f(time) # Time series
cloudx = series[:points] # Point Cloud x
cloudy = series[tau:] # Point Cloud y


#################
# Betti numbers #
#################

dirop1 = dirac(betk, points, cloudx, cloudy, e1, e1, xi) # Dirac operator
print(f"{dirop1}")
rank1 = LA.matrix_rank(dirop1) # Rank of Dirac operator
eigen1, _ = LA.eig( dirop1 ) # Eigenvalues and eigenvectors of dirac operator
print(f"Eigenvalues:\n {eigen1}")
print(f"The dimension of the Dirac operator at scale {e1} is {rank1}")
betti1 = np.sum( np.absolute(eigen1 - 1.0) < 0.001 ) # Multiplicity of eigenvalue 1
print(f"The number of loops that at scale {e1} is:\n {betti1}")

dirop2 = dirac(betk, points, cloudx, cloudy, e1, e2, xi) # Dirac operator
print(f"{dirop2}")
rank2 = LA.matrix_rank(dirop2) # Rank of Dirac operator
eigen2, _ = LA.eig( dirop2 ) # Eigenvalues and eigenvectors of dirac operator
print(f"Eigenvalues:\n {eigen2}")
print(f"The dimension of the Dirac operator at scales {e1} and {e2} is {rank2}")
betti2 = np.sum( np.absolute(eigen2 - 1.0) < 0.001 ) # Multiplicity of eigenvalue 1
print(f"The number of loops that persist from scale {e1} to scale {e2} is:\n {betti2}")


########################
# Plotting Time series #
########################
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(time, series, 'o-')
#plt.ylim(-1.2,1.2)
#plt.xlim(-0.2, 1.2)
ax1.set_title("Time Series")
ax1.set_xlabel("t")
ax1.set_ylabel("sin(2*pi*t)")


########################
# Plotting Point Cloud #
########################
ax2.plot(cloudx, cloudy, 'o')
#plt.ylim(-1.2, 1.2)
#plt.xlim(-1.2, 1.2)
ax2.set_title("Point Cloud")
ax2.set_xlabel("x(t)")
ax2.set_ylabel("x(t + tau)")


################
# Saving plots #
################
fig.savefig("figures/time-series.png")

