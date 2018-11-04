import matplotlib.pyplot as plt
import numpy as np
import utils
from timeit import default_timer as timer

#grab data preprocesed time series data and sentiment data
#format into column vectors


#set of all x and y points 

# inspect plot for pattern
plt.scatter(x, y, color='green')
plt.title('SVA check')
plt.show()


#see how model fitts on different dimensions
times = []
errs = []
for i in range(0, 10):
    plt.figure()
    plot_regression(x, y, i)

features_100 = polynomial_features(x, 100)
features_100.shape

#find smallest eigen value
xTx = features_100.T.dot(features_100)
eig, _ = np.linalg.eig(xTx)
eig.min()



#Check for overfitting/underfitting on graph






#tweak hyperparams so no outlier predictions




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
