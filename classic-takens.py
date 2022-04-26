import numpy as np
import matplotlib.pyplot as plt
from numpy import pi
from numpy import linalg as LA
from math import comb as nCk
from itertools import combinations


##############################
#        Functions           #
##############################


# k-simplices
def kcomplex(k, n):
    comp = np.zeros( (nCk(n,k+1), n) )
    for row, combo in enumerate( np.array( list( combinations( range(n), k+1) ) ) ):
        comp[row][combo] = 1
    return comp


# Simplex diameter
def diameter(simplex, x, y, eps):
    vertx = x[simplex > 0.5] # x coordinate of vertices in simplex
    verty = y[simplex > 0.5] # y coordinate of vertices in simplex
    for a, b in zip(vertx,verty):
        for c, d in zip(vertx, verty):
            if LA.norm( np.array( [a - c, b - d] ) ) > eps: # If diameter is larger than eps return 0
                return 0
    return 1 # Otherwise return 1


# Get coefficient of boundary matrix
def isface(face, simplex):
    if (simplex.sum() - face.sum()) < 0.5:
        return 0 # Not a face if it's of higher dimension
    diff = face + simplex # Difference, i.e. get rid of repeated vertices
    if np.sum( np.absolute( diff - 1.0 ) < 0.5 ) > 1.0:
        return 0 # Not a face if difference is more than one vertex
    power = np.argmin( diff[ diff > 0.5 ] ) # Position of the missing vertex determines the sign
    return (-1)**power


# Boundary
def boundary(k, n):
    comp1 = kcomplex(k-1, n) # simplices dimension k-1
    comp2 = kcomplex(k, n) # simplices dimension k
    faces, _ = comp1.shape # number of simplices dimension k-1
    simp, _ = comp2.shape # number of simplices dimension k
    bound = np.zeros( (faces, simp) )
    for row, face in enumerate(comp1):
        for col, simplex in enumerate(comp2):
            bound[row,col] = isface(face, simplex)
    return bound


# Projection
def projection(k, n, x, y, eps):
    comp = kcomplex(k, n) # k-simplices
    proj = np.zeros( comp.shape[0] )
    for i, simp in enumerate(comp):
        proj[i] = diameter(simp, x, y, eps)
    return proj


# Persistent Dirac Operator
def dirac(k, n, x, y, eps1, eps2, xi):
    bound1 = boundary(k, n) # k dimensional boundary matrix
    bound2 = boundary(k+1, n) # k-1 dimentional boundary matrix
    rows1, cols1 = bound1.shape
    rows2, cols2 = bound2.shape
    proj = np.block([
        [ np.diag(projection(k-1, n, x, y, eps1)) , np.zeros( (rows1, cols1) ) , np.zeros( (rows1, cols2) ) ],
        [ np.zeros( (cols1, rows1) ) , np.diag(projection(k, n, x, y, eps1)) , np.zeros( (rows2, cols2) ) ],
        [ np.zeros( (cols2, rows1) ) , np.zeros( (cols2, rows2) ) , np.diag(projection(k+1, n, x, y, eps2)) ]
        ]) # Projection operator
    di = proj @ np.block([
        [ (-xi)*np.eye( rows1 ) , bound1 , np.zeros( (rows1, cols2) ) ],
        [ bound1.transpose() , (xi)*np.eye( rows2 ) , bound2 ],
        [np.zeros( (cols2, rows1) ) , bound2.transpose() , (-xi)*np.eye( cols2 ) ],
        ]) @ proj # Dirac operator
    return di


##############
# Parameters #
##############
T = 9 # Number of data-times
tau = 1 # Delay
d = 2 # Dimension of point cloud
e1 = 1.0 # First scale
e2 = 1.3 # Second scale
e3 = 2.0 # Third scale
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
dirop = dirac(betk, points, cloudx, cloudy, e1, e2, xi) # Dirac operator
rank1 = LA.matrix_rank(dirop) # Rank of Dirac operator
eigen, _ = LA.eig( dirop ) # Eigenvalues and eigenvectors of dirac operator
print(f"The dimension of the Dirac operator at scales {e1} and {e2} is {rank1}")
betti = np.sum( np.absolute(eigen - 1.0) < 0.001 ) # Multiplicity of eigenvalue 1
print(f"The number of loops that persist from scale {e1} to scale {e2} is:\n {betti}")

dirop2 = dirac(betk, points, cloudx, cloudy, e2, e2, xi) # Dirac operator
rank2 = LA.matrix_rank(dirop2) # Rank of Dirac operator
eigen2, _ = LA.eig( dirop2 ) # Eigenvalues and eigenvectors of dirac operator
print(f"The dimension of the Dirac operator at scales {e2} and {e2} is {rank2}")
betti2 = np.sum( np.absolute(eigen2 - 1.0) < 0.001 ) # Multiplicity of eigenvalue 1
print(f"The number of loops that at scale {e2} is:\n {betti2}")

dirop3 = dirac(betk, points, cloudx, cloudy, e2, e3, xi) # Dirac operator
rank3 = LA.matrix_rank(dirop3) # Rank of Dirac operator
eigen3, _ = LA.eig( dirop3 ) # Eigenvalues and eigenvectors of dirac operator
print(f"The dimension of the Dirac operator at scales {e2} and {e3} is {rank3}")
betti3 = np.sum( np.absolute(eigen3 - 1.0) < 0.001 ) # Multiplicity of eigenvalue 1
print(f"The number of loops that persist from scale {e2} to scale {e3} is:\n {betti3}")


########################
# Plotting Time series #
########################
fig1 = plt.figure()
plt.plot(time, series, 'o')
plt.ylim(-1.2,1.2)
plt.xlim(-0.2, 1.2)
plt.title("Time Series", size = 24, weight = 'bold')
plt.xlabel("time")
plt.ylabel("sine")


########################
# Plotting Point Cloud #
########################
fig2 = plt.figure()
plt.plot(cloudx, cloudy, 'o')
plt.ylim(-1.2, 1.2)
plt.xlim(-1.2, 1.2)
plt.title("Point Cloud", size = 24, weight = 'bold')
plt.xlabel("x(t)")
plt.ylabel("x(t + tau)")


################
# Saving plots #
################
#fig1.savefig("figures/time-series.png")
#fig2.savefig("figures/point-cloud.png")


#################
#     Test      #
#################
#simp1 = np.array([0,1,1,1])
#simp2 = np.array([0,1,1,0])
#simp3 = np.array([1,1,1,1])
#simp4 = np.array([1,1,0,0])
#xcoo = np.array([0,1,1,0])
#ycoo = np.array([0,0,1,1])
#epst = 1.0
#epst2 = 2.0

#test1 = diameter(simp1, xcoo, ycoo, epst)
#print(f"Test 1 is {test1} and should be 0")
#test2 = diameter(simp2, xcoo, ycoo, epst)
#print(f"Test 2 is {test2} and should be 1")

#test3 = isface(simp2, simp1)
#print(f"Test 3 is {test3} and should be 1")
#test4 = isface(simp3, simp1)
#print(f"Test 4 is {test4} and should be 0")
#test5 = isface(simp4, simp1)
#print(f"Test 5 is {test5} and should be 0")

#test6 = kcomplex(1, 4)
#print(f"Test 6 is \n {test6}")

#test7 = boundary(1, 4)
#print(f"Test 7 is \n {test7}")

#test8 = projection(1, 4, xcoo, ycoo, epst)
#print(f"Test 8 is \n {test8}")

#test9 = dirac(1, 4, xcoo, ycoo, epst, epst2, 1)
#print(f"Test 9 is \n {test9}")
#test10, _ = LA.eig( test9 )
#print(f"Test 10 is \n {test10}")
#test11 = np.sum( np.absolute(test10 - 1.0) < 0.001 )
#print(f"The number of loops that persist from scale {epst} to scale {epst2} is:\n {test11}")

#test12 = dirac(1, 4, xcoo, ycoo, epst, epst, 1)
#print(f"Test 12 is \n {test12}")
#test13, _ = LA.eig( test12 )
#print(f"Test 13 is \n {test13}")
#test14 = np.sum( np.absolute(test13 - 1.0) < 0.001 )
#print(f"The number of loops that persist from scale {epst} to scale {epst} is:\n {test14}")


