import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer as timer
from utils import polynomial, plot_polynomial, polynomial_data, plot_linear, NUM_DIMENSIONS

# Part 1: fit model with training data
#grab data preprocesed time series data and sentiment data


#set of all x and y points 

# inspect plot for SVA's of model
plt.scatter(x, y, color='green')
plt.title('SVA check')
plt.show()

#Part 2: Ordinary least squares

#least_squares approximation
def least_squares(x, y):
    xTx = x.T.dot(x)
    xTx_inv = np.linalg.inv(xTx)
    w = xTx_inv.dot(x.T.dot(y))

    y_hat = x.dot(w)
    error = np.mean((y - y_hat) ** 2)
    return w, error




#How well does it work in other dimensions?
times = []
errs = []
for i in range(0, 10):
    plt.figure()
    plot_regression(x, y, i)

#Maybe we can do better
plot_regression(x, y, 20)

plot_regression(x, y, 100)

features_100 = polynomial_features(x, 100)
features_100.shape
xTx = features_100.T.dot(features_100)
eig, _ = np.linalg.eig(xTx)
eig.min()

#What happens if we sample new data?
np.random.seed(124)
x_new, y_new = polynomial_data(coeffs, 200)

plt.scatter(x, y, color='green')
plt.scatter(x_new, y_new, color='blue')

#4-degree polynomial
plt.figure(figsize=(20, 10))
plt.subplot(121)
plot_regression(x, y, 4)
plt.subplot(122)
plot_regression(x_new, y_new, 4)

#20-degree polynomial
plt.figure(figsize=(20, 10))
plt.subplot(121)
plot_regression(x, y, 20)
plt.subplot(122)
plot_regression(x_new, y_new, 20)

#What happens if we have more data?
x_big, y_big = polynomial_data(coeffs, 100000)
plt.figure()
plot_regression(x_big, y_big, 4)
plt.figure()
plot_regression(x_big, y_big, 20)
plt.figure()
plot_regression(x_big, y_big, 200)

#Part 3: Polynomial features

def polynomial_features(x, order):
    features = np.column_stack([x**i for i in range(0, order+1)])
    return features

def plot_regression(x, y, order):
    start = timer()
    features = polynomial_features(x, order)
    w, mse = least_squares(features, y)
    end = timer()
    plt.scatter(x, y, color='green')
    plot_polynomial(w)
    plt.title(f"Polynomial degree: {order}, error: {mse}, time: {end-start}")

    #least_squares approximation
def least_squares(x, y):
    xTx = x.T.dot(x)
    xTx_inv = np.linalg.inv(xTx)
    w = xTx_inv.dot(x.T.dot(y))

    y_hat = x.dot(w)
    error = np.mean((y - y_hat) ** 2)
    return w, error

