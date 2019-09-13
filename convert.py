
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn import preprocessing
import math
from sklearn.cluster import KMeans
from copy import deepcopy


# In[2]:


train_folder = "Data_Training_Set/"


# In[3]:


demand_train_pred = pd.read_csv(train_folder + "Demand_Train_pred.csv", header = None)
demand_train = pd.read_csv(train_folder + "Demand_Train.csv", header = None)

solar_train_pred = pd.read_csv(train_folder + "Solar_Train_pred.csv", header = None)
solar_train = pd.read_csv(train_folder + "Solar_Train.csv", header = None)


# In[18]:


demand_x_vals_list = demand_train_pred.values.tolist()
solar_x_vals_list = solar_train_pred.values.tolist()

x_val = []
tm = 0
sum_hour = [0 for i in range(24)]
for_kmeans = []
ct = 0
for row in range(len(demand_x_vals_list)):
    summ = 0
    i = 0
    for_kmean = []
    for col in range(24):
        summ += demand_x_vals_list[row][col]
        sum_hour[i] += demand_x_vals_list[row][col]
        for_kmean.append(demand_x_vals_list[row][col])
        if demand_x_vals_list[row][col] - solar_x_vals_list[row][col] <= -5:
            ct += 1
        i += 1
    for_kmeans.append(for_kmean)
print(ct/21600)
tppp = []
for i in range(len(sum_hour)):
    tppp.append([sum_hour[i],i])
tppp.sort()
# print(tppp)
kmeans = KMeans(n_clusters=7, random_state=0).fit(for_kmeans)


# print(kmeans.labels_)
# sums = set(summ)
iterr = 0
for row in range(len(demand_x_vals_list)):
    tm = 0
    if iterr == 7:
        iterr = 0
    for col in range(24):
        x_val.append([demand_x_vals_list[row][col]])
        tm += 1
    iterr += 1
    
demand_y_vals_list = demand_train.values.tolist()
y_val = []
for row in demand_y_vals_list:
    for val in row:
        y_val.append(val)
y_vals = []
for i in range(len(y_val)):
    y_vals.append((y_val[i]))
y_val = y_vals
print(len(y_val))


# In[28]:


x_train, x_test, y_train, y_test = train_test_split(x_val, y_val, test_size = 0.1)
forest = RandomForestRegressor(n_estimators = 256)


xTemp = deepcopy( x_train )
yTemp = deepcopy( y_train )

    
print(len(x_train))
print(len(y_train))


forest.fit(x_train, y_train)
y_found = forest.predict(x_test)
s1 = 0
s2 = 0

for i in range(len(y_found)):
#     print(x_test[i][0], " ", y_found[i], " ", y_test[i])
    s1 += (y_found[i] - (x_test[i][0]))*(y_found[i] - (x_test[i][0]))
    s2 += (y_test[i] - (y_found[i]))*(y_test[i] - (y_found[i]))
    
print(s1)
print(s2)


# In[21]:


print(demand_train_pred.describe())


# In[16]:


print(demand_train_pred)

