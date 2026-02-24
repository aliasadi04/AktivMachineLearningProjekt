# %%
import numpy as np
import torch
from torch import nn, distributions
from scipy.spatial.distance import cdist
from scipy.stats import norm, multivariate_normal
import matplotlib.pyplot as plt

import GPyOpt

# %%

normal = multivariate_normal(mean=[0.3,-0.5], cov=[[2,.1],[.1,2]])
f= lambda x: -normal.pdf(x)
N = 100
max_iter = 16

x = np.linspace(-3,3,N)
x = np.array(np.meshgrid(x,x,indexing='ij')).reshape(2,-1)
Xinit = np.array([[-3,-3],[-3,3],[3,-3],[3,3]])

bounds2d = [{'name': 'x', 'type': 'continuous', 'domain': (-3,3)},
            {'name': 'y', 'type': 'continuous', 'domain': (-3,3)}]

bo = GPyOpt.methods.BayesianOptimization(f, domain=bounds2d, X=Xinit, acquisition_type='EI')
bo.run_optimization(max_iter = max_iter)

# %%
y=f(x.T).reshape(N,N).T
plt.figure('Optimization progress')
plt.imshow(y,cmap='viridis',origin='lower',extent=[x[0][0],x[0][-1],x[1][0],x[1][-1]])
plt.plot(bo.X[:,0],bo.X[:,1],'ro:')
for i,xx in enumerate(bo.X):
    plt.text(xx[0],xx[1],'%i'%(i+1))
plt.figure('Approximated function')
plt.subplot(1,2,1)
plt.title('mean')
plt.imshow(bo.model.predict(x.T)[0].reshape(N,N).T,cmap='viridis',origin='lower',extent=[x[0][0],x[0][-1],x[1][0],x[1][-1]])
plt.subplot(1,2,2)
plt.title('variance')
plt.imshow(bo.model.predict(x.T)[1].reshape(N,N).T,cmap='viridis',origin='lower',extent=[x[0][0],x[0][-1],x[1][0],x[1][-1]])
#plt.suptitle('Approximated function')
plt.figure('Acquisition function')
plt.imshow(-bo.acquisition.acquisition_function(x.T).reshape(N,N).T,cmap='viridis',origin='lower',extent=[x[0][0],x[0][-1],x[1][0],x[1][-1]])