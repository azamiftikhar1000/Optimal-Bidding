
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import preprocessing


# In[5]:


train_folder = "Data_Training_Set/"


# In[6]:


demand_train_pred = pd.read_csv(train_folder + "Demand_Train_pred.csv", header = None)
demand_train = pd.read_csv(train_folder + "Demand_Train.csv", header = None)


# In[7]:


tp = demand_train_pred.values.tolist()
x_val = []
for row in tp:
    for val in row:
        x_val.append([val])
tp = demand_train.values.tolist()
y_val = []
for row in tp:
    for val in row:
        y_val.append(val)
lab_enc = preprocessing.LabelEncoder()
encoded = lab_enc.fit_transform(y_val)
# tp = []
# for i in range(len(y_val)):
#     tp.append((y_val[i] - x_val[i]))
# y_val = tp
print(len(y_val))


# In[41]:


x_train, x_test, y_train, y_test = train_test_split(x_val, y_val, test_size = 0.1)
forest = MLPRegressor(hidden_layer_sizes=(64,64), activation='relu')
# forest = RandomForestRegressor(n_estimators = 500)
# x_train = np.array(x_train)
# x_train = x_train.reshape(-1,1)
print(type(x_train))
print(type(y_train))
# print(type(x_train))
# print(type(y_train))

# y_train = np.array(y_train)
# y_train = y_train.reshape(-1,1)
# xx = []
# for val in x_train:
#     xx.append([val])
# print(xx)
# yy = y_train
# yy = []
# for val in y_train:
#     yy.append([val])
# print(xx)
forest.fit(x_train, y_train)
y_found = forest.predict(x_test)
s1 = 0
s2 = 0

for i in range(len(y_found)):
#     print(x_test[i][0], " ", y_found[i], " ", y_test[i])
    s1 += (y_found[i] - y_test[i])*(y_found[i] - y_test[i])
    s2 += (x_test[i][0] - y_test[i])*(x_test[i][0] - y_test[i])
    
print(s1)
print(s2)


# In[21]:


print(demand_train_pred.describe())


# In[16]:


print(demand_train_pred)

