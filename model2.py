# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 17:13:59 2018

@author: sijian.xuan
"""


# coding: utf-8

# ### Load Python modules, options, folders

# In[1]:

import os
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,classification_report
# Load user-defined packages
os.chdir('C:/Users/sijian.xuan/Desktop/Python packages')
from ConfusionMatrix import *
from gradientboosting_classifier import *
from Multi_AUC import *
from data_visualization import * 
from Classes import *
from results_analysis import *
get_ipython().magic('matplotlib inline')


# In[2]:

pd.set_option('display.max_rows',None) # do not print max_rows in pandas
np.set_printoptions(threshold = np.nan) # do not print ... in numpy
warnings.filterwarnings("ignore") # do not print warnings


# ### Load data and clean data, divide training set and testing set

# In[3]:

# Load input data for model and prediction
data4model = data4modeling2.copy()
data2pred = data2pred2.copy()


# In[4]:

# do data_visualization
data_visualization_model2(data4model)
######################################################
x_data = data4model.drop(['indication','pat'],axis = 1)
y_data = pd.DataFrame(data4model['indication'])
y_data_series = y_data.squeeze()


# In[5]:

# Check frequency tables
print('Total counts per indication in the dataset: ')
print(y_data_series.value_counts())
print(' ')
print('Market share per indication in the dataset: ')
print(y_data_series.value_counts()/y_data_series.count())


# ### Data Preprocesssing
# **preprocess the whole dataset**
#  1. get dummies for on X_data
#  2. fill nan with 0 on X_data
#  3. normalizer_l2 on X_data
#  4. label encoding on y_data
#  5. use different model to train set
#  6. get accuracy on tst set

# In[6]:

pipeline = Pipeline([('dummies,fillna,normalizer', processing()), ])
x_data_copy = x_data.copy()
x_data_pipeline = pd.DataFrame(pipeline.fit_transform(x_data_copy))

pipeline2 = Pipeline([('labelrecoding', label_encoder())])
y_data_copy = y_data.copy()
# x_data_pipeline,y_data_copy are data for modeling


# In[7]:

# Split training set and testing sst
X = x_data_pipeline#####Select feature columns
y = y_data_copy#####Select label columns
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, stratify=y, random_state = 1)
y_train = y_train.squeeze()
y_test = y_test.squeeze()


# ### Fit the model

# In[8]:

# Fit the best model based on tuned parameters
best_clf = ensemble.GradientBoostingClassifier(learning_rate = 0.05, max_depth = 3, n_estimators = 100)## select model

# Fit the model and check ConfusionMatrix
best_clf.fit(X_train,y_train)

# Check R-Style confusionMatrix

y_pred = best_clf.predict(X_test).tolist()## change type: object to list, cannot create Confusion Matrix if not change


# In[9]:

confusionMatrix(y_pred, y_test).show()## Show the Confusion Matrix


# In[10]:

# Classification Report
print('Classification Report:\n',classification_report(y_test,y_pred, target_names=["Derma","Gastro","Kinder","Ogen","Rheuma"]))


# In[11]:

### prepare input for ROC
n_classes = len(y_train.unique()) # number of indications, if 2 then n_class=1, if >2 then the number of indications
y_score = best_clf.fit(X_train, y_train).decision_function(X_test)
y_test2 = pd.get_dummies(y_test)


# In[12]:

ROC(n_classes, y_score, y_test2)


# In[13]:

PRC(n_classes,y_test2,y_score)


# In[14]:

AUC_model2(best_clf, X_train, y_train, X_test, y_test, n_classes)


# ### Make prediction

# In[15]:

# Data to be predicted
data_predict = data2pred.drop(['pat','indication'], axis=1)
data_predict_pipeline = pd.DataFrame(pipeline.fit_transform(data_predict))
print(data_predict_pipeline.shape)
data_predict_pipeline.head()


# In[16]:

# Final prediction dataset needs to have the same contents as the training and testing set
pred_final_model = best_clf.predict(data_predict_pipeline)## predicted indications
pred_final_prob = best_clf.predict_proba(data_predict_pipeline) ## predicted probabilities


# In[17]:

# Plot top features
feature_importances = pd.concat([pd.DataFrame(x_data_pipeline.columns), pd.DataFrame(best_clf.feature_importances_)], axis = 1)
feature_importances.columns = ['features', 'importance']
feature_importances.sort_values(by = ['importance'], ascending = False, inplace = True)
sns.barplot(x='importance', y='features', data=feature_importances.head(), color="b")
plt.title('Feature importance')


# In[18]:

# Create a patient list with indication and probability of every indication
final_results = pd.concat([data2pred['pat'], pd.DataFrame(pred_final_model), pd.DataFrame(pred_final_prob)], axis = 1)
final_results.columns = ['pat','indication','prob_Derma','prob_Gastro','prob_Kinder','prob_Ogen','prob_Rheuma'] # adpat here
final_results.head()


# In[19]:

# Check frequency tables
print('Total counts per indication in the dataset: ')
print(final_results['indication'].value_counts())
print(' ')
print('Market share per indication in the dataset: ')
print(final_results['indication'].value_counts()/final_results['indication'].count())


# In[20]:

#final_results.to_csv("./Output/prediction_model2.csv", index = False) # adpat here

