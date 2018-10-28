# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:30:58 2018

@author: Mitali
"""
import matplotlib.pyplot as plt
import airplane
from sklearn import svm
import numpy as np

df = airplane.load('0001')
columns = ["Alt", "Spd", "WTC", "EngType"]
df = df.reindex(columns=columns)
x = df[['Alt', 'Spd']]
x = x.values
y = df.WTC
y = y.values
clf = svm.SVC(kernel='rbf', C=1000, gamma=3)
print "Begin training..."
clf.fit(x,y)
print "Begin prediction..."
"""
y = clf.predict(X)
print "Begin graphing..."
#s = "y = " + str(clf.coef_[0]) + "x + " + str(clf.intercept_)
#plt.title(s)
plt.scatter(X.WTC,X.Spd,c=y)

plt.contourf(X, y, alpha = 0.4)
plt.contour(X, y, colors='k')
#plt.scatter(X[:, 0], X[:, 1], c = y)
"""
print "Setting values..."
x_min, x_max = 0, 3
y_min, y_max = 0, 666
h = .02
X, Y = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
Z = clf.predict(np.c_[X.ravel(), Y.ravel()])
Z = Z.reshape(X.shape)
print "Plotting..."
plt.contourf(X, Y, Z, alpha = 0.4)
plt.contour(X, Y, Z, colors='k')
plt.scatter(x[:, 0], x[:, 1], c = y)