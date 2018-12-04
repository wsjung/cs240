import matplotlib.pyplot as plt
import numpy as np
from utils import *
np.set_printoptions(precision=3)


np.random.seed(3)
# 1 + 0.5 * x - 0.5 x^2 - 0.2 x^3 - 0.1 x^4
coeffs = [1, 0.5, -0.5, -0.2, -0.1]
x, y = polynomial_data(coeffs, 200)
plt.scatter(x, y, color='green')
x_range = [100, 110]
plot_polynomial(coeffs, x_range=x_range, color='b')



features_4 = polynomial_features(x, 4)



#test fxn
w, err = ridge_regression(features_4, y)
plt.figure(figsize=(8, 4))
plot_polynomial(coeffs, x_range=x_range, color='b')
plot_polynomial(w, x_range=x_range)











#mean squared error term
def mse(x, y, w):
    return np.mean((x.dot(w) - y)**2)

      #used to test model by generating semi randomized data based on coefficients
def polynomial_data(coeffs, n_data=100, x_range=[-1, 1], eps=0.1):
    #generate a set of points distanced up to 1 unit from coeff equation
    x = np.random.uniform(x_range[0], x_range[1], n_data)
    poly = polynomial(x, coeffs)
    #return x and y
    return x.reshape([-1, 1]), np.reshape(poly + eps * np.random.randn(n_data), [-1, 1])





#format features of a given sample x and degree order
def polynomial_features(x, order):
    features = np.column_stack([x**i for i in range(0, order+1)])
    return features

#plots a regression line given the set of points and the degree order
def plot_regression(x, y, order):
    start = timer()
    features = polynomial_features(x, order)
    w, mse = least_squares(features, y)
    end = timer()
    plt.scatter(x, y, color='green')
    plot_polynomial(w)
    plt.title(f"Polynomial degree: {order}, error: {mse}, time: {end-start}")

    #least squares approximation for set of points
    # x_hat = (A^t * A)^-1 A^T * b
def least_squares(x, y):
    #take product with x and its transpose
    dx = np.dot(x, x.T)

    #take the inverse of the product
    dxinv = np.linalg.inv(dx)
    dxy = np.dot(x, y.T)
   
    #calculate sol
    w = np.dot(dxinv,dxy)

    #calculate mean square error
    y_hat = np.dot(x.T,w)
    error = np.mean((y - y_hat) ** 2)
    return w, error

#use ridge regression to soften bias from noisy data
#With linear algebra generalize to 
# ∥β∥^2= βT⋅β = β⋅β = ∑(d i=1) β^2_i = dot product
# l is hyperparameter we can tweak if needed
def ridge_regression(x, y, l=1.0):
    #start by taking dot product of x (β^2)
    dx = np.dot(x, x.T)
    
    #add ID matrix to squared result
    m1 = dx + l * np.eye(dx.shape[0])
   
    #get dot product of x on y
    m2 = np.dot(x, y.T)
   
    #calculate sol
    w = np.dot(np.linalg.inv(m1),m2)
   
    #calculate mean square error
    err = np.mean((np.dot(x.T,w) - y) ** 2)
    return w, err