# -*- coding: utf-8 -*-
"""alexopoulos_angelos_stout_case_study_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xvpSpEIRs2A9szlqP2KIcwbgoUjfn3Nk

##Case Study-Stout##
Alexopoulos Angelos

##Loading and Description##

We were given a data set that represents thousands of loans made through the Lending Club platform, which is a platform that allows individuals to lend to other individuals. On this dataset is required to perform a number of tasks:



1.    Describe the dataset and any issues with it.

2.   Generate a minimum of 5 unique visualizations using the data and write a brief description of your observations. Additionally, all attempts should be made to make the visualizations visually appealing
3.   	Create a feature set and create a model which predicts interest_rate using at least 2 algorithms. Describe any data cleansing that must be performed and analysis when examining the data.
4.   	Visualize the test results and propose enhancements to the model, what would you do if you had more time. Also describe assumptions you made and your approach.
"""

#libraries import
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import plotly.express as px

!pip install missingno

#dataset loading and printing a sample of 10 rows
df = pd.read_csv('loans_full_schema.csv')
df.sample(10)

#Dataset shape -
print("The size of the dataset is", df.shape )

"""Description
Descriptive statistics include those that summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values.
"""

df.describe(percentiles=None, include=None, exclude=None, datetime_is_numeric=False).T

"""*  Check for null values



"""

df.columns[df.isnull().any()].tolist()
print("The columns that have null values are",len(df.columns[df.isnull().any()].tolist()), "and are", df.columns[df.isnull().any()].tolist())

df.isnull().sum()

print( "The total number of null values are", df.isnull().sum().sum()) 
freq=df.isnull().sum().sum()/(df.shape[0]*df.shape[1])
print(f"The total percentage of null values are {freq * 100:.2f} %. " )

# Visualize missing values as a matrix
msno.matrix(df, labels = True,)

plt.title('Null values visual bar plot',fontdict={'fontsize': 20})
msno.bar(df)

#Dataframe that represents the percentage of columns with missing values
prc_missing_values = pd.DataFrame()
prc_missing_values['Percentage of missing values'] = ['over 10% ','over 20% ','over 30% ','over 40% ','over 50%','over 60%','over 70% ','over 80%', 'over 90%'] 


ten_percent    = len(df.columns[((df.isnull().sum())/len(df)) > 0.1])
twenty_percent = len(df.columns[((df.isnull().sum())/len(df)) > 0.2])
thirty_percent = len(df.columns[((df.isnull().sum())/len(df)) > 0.3])
forty_percent  = len(df.columns[((df.isnull().sum())/len(df)) > 0.4])
fifty_percent  = len(df.columns[((df.isnull().sum())/len(df)) > 0.5])
sixty_percent  = len(df.columns[((df.isnull().sum())/len(df)) > 0.6])
seventy_percent= len(df.columns[((df.isnull().sum())/len(df)) > 0.7])
eighty_percent = len(df.columns[((df.isnull().sum())/len(df)) > 0.8])
ninety_percent = len(df.columns[((df.isnull().sum())/len(df)) > 0.9])

prc_missing_values['Number of columns'] = [ten_percent, twenty_percent, thirty_percent, forty_percent, fifty_percent, sixty_percent, seventy_percent, eighty_percent, ninety_percent]

prc_missing_values

#Columns with high percentage of null values may cause trouble so we remove them based on a threshold of our desire
#threshold choice= 0.5
#new dataframe named af for dataset after columns drop
af=df.dropna(axis=1, thresh=int(0.5*len(df)))
af.shape

#Null check again


af.columns[af.isnull().any()].tolist()
print("The number of columns that have null values is", len(af.columns[af.isnull().any()].tolist()),"and are", af.columns[af.isnull().any()].tolist())
print( "The total number of null values are", af.isnull().sum().sum()) 
freq=af.isnull().sum().sum()/(af.shape[0]*af.shape[1])
print(f"The total percentage of null values are {freq * 100:.2f} %. " )

af.isnull().sum()

"""We will get more info about the columns with missing value. The first on reffers to the jobs titles. A little guess is that the missing values refers to unemployed people. #The following 4 columns with missing values will be replaced using the interpolation method
af['emp_length'].
"""

af['emp_title'].value_counts()
print(af['emp_title'])

af['emp_title'] = af['emp_title'].fillna('Unemployed')

af['emp_length'] = af['emp_length'].interpolate(method='linear', limit_direction='forward', axis=0)
af['debt_to_income'] = af['debt_to_income'].interpolate(method='linear', limit_direction='forward', axis=0)
af['months_since_last_credit_inquiry'] = af['months_since_last_credit_inquiry'].interpolate(method='linear', limit_direction='forward', axis=0)
af['num_accounts_120d_past_due'] = af['num_accounts_120d_past_due'].interpolate(method='linear', limit_direction='forward', axis=0)

"""* Now there are no more missing values and we can continue with the visualizataion



"""

af.isnull().sum()

af.info()
af.shape

"""Generally as reffered in the documentation too the dataset represents thousands of loans made through the Lending Club platform, which is a platform that allows individuals to lend to other individuals. After some pre-processing I ended up with 1000 rows and 50 columns. The main data prepocessing actions that I made was: 
*   Handling missing data
*   Handling categorical data (next chapter)

**Here is a description of the dataset:**
  The dataset contains information on loans made through the Lending Club platform. It includes variables such as the loan amount, interest rate, loan term, credit score, employment length, annual income, and more. The goal of this dataset is to predict the interest rate of a loan based on various borrower characteristics.

There are a few potential issues with the dataset:
1.	Missing values: Some of the variables have missing values, which may affect the accuracy of the model.
2.	Outliers: There may be outliers in the data that could impact the model's performance.
3.	Imbalanced classes: The classes (interest rates) may not be balanced, which could lead to a model that is biased towards the majority class.
4.	Correlated variables: Some of the variables may be correlated, which could affect the model's performance.
5.	Data leakage: There may be data leakage, where information that should not be available at the time of loan application is included in the dataset. This could lead to a model that is overly optimistic about its performance.

##Visualization##
"""

af.sample(10)

(af['paid_total'].value_counts())
#af.columns

"""**First Vizualization**:Peaks of the data for Home Ownership."""

sns.violinplot(x="homeownership", y="interest_rate", data=af, hue="term",palette=["#6c6361","#d9d8a8"])
plt.title("Violin Plot")
plt.xlabel("Home Ownership")
plt.ylabel("Interest Rate in %")
plt.grid(False)
plt.show()

"""**Second Vizualization:** Number of loans per loan grade.




"""

redlines_labels = {'grade': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                   'desc':['A - Best', 'B - Still Desirable', 'C - Definitely Declining', 'D - Hazardous', 'Bad', 'Very Bad'],
                   'color': ['g', 'b', 'y', 'r', ]
         }
fig, ax  = plt.subplots(1,1,figsize=(15,5))
sns.countplot(y='grade',data=af, palette=redlines_labels['color'], ax=ax)
ax.set_title('Number of loans per grade');

"""**Third Vizualization:** Number of loans and per loan status.




"""

fig, ax  = plt.subplots(1,1,figsize=(15,5))
sns.countplot(y='loan_status',data=af, palette=redlines_labels['color'], ax=ax)
plt.ylabel("Loan status")
ax.set_title('Number of loans per loan status');

"""**Fourth Vizualization:** Number of loans and per loan status andd per grade."""

plt.figure(figsize=(15, 15))
grade = sorted(af.grade.unique().tolist())
plt.subplot(2, 2, 1)
sns.countplot(x='grade', data=af, hue='loan_status', order=grade,palette=["#6c6361","#d9d8a8",'#c5be54',"#635e21","#847474","#bcbdbf"])
plt.ylabel("Number of loans")
plt.xlabel("Grade")
plt.grid(True)
plt.show()

"""**Fifth Visualization:**
How interest rate is distributed across its different values
"""

sns.displot(af['interest_rate'])
plt.title("Distribution of Interest Rate")
plt.xlabel("Interest Rate in %")
plt.ylabel("Occurance")
plt.grid(False)
plt.show()

"""**Sixth Visualization** 
Number of Loans per State.
"""

#Loans per State
plt.figure(figsize=(30, 30))
loan_status = af.loan_status.unique().tolist()
plt.subplot(2, 2, 1)
sns.countplot(y='state', data=af,palette=["#6c6361","#d9d8a8",'#c5be54',"#635e21","#847474","#bcbdbf"])
plt.grid(False)
plt.ylabel("State")
plt.xlabel("Count")
plt.show()

"""**Seventh Visualization:**
 Correlation between variables
"""

#corr between variables
plt.figure(figsize = (15,15))
sns.heatmap(data = af.corr(), annot = True)
plt.show()

"""For this section the visualizations that I chose to recreate in order to get an insight for the data were:

*   A Violin Plot which shows the peaks of the data for Home Ownership(inputs:  homeownership per interest of rate).
*   Bar Chart whose inputs about number of loans and per grade
*   Bar Chart same as before about number of loans per status.
*   Bar Chart same as before about number of loans per status and grade.
*   Distribution Plot which shows how interest rate is distributed across its different values
*   Bar Chart which shows the distribution of loans per State.
*   Correlation Heatmap: check correlation between all the variables to get some info about them.

"""



"""#**Model Creation**

After the visualizations are over we will start making the data ready in order to be fed into the machine learning model. Initially, all the data must be in the same data type. So using LabelEncoding() the category 'emp_title' which have string value variables will be transformed to floats. LabelEncoding is used to transform non-numerical labels (as long as they are hashable and comparable) to numerical labels.

By default, it will assign integers to labels in the order that is observed in the data. If a specific order is desired, it can be specified via the “categories” argument as a list with the rank order of all expected labels.

* Encoder
"""

#categorical to numerical
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
labelencoder  = LabelEncoder()
oridnalencoder  = OrdinalEncoder()
for i in af.columns:
    if af[i].dtypes == 'object':
        
        af[i] = labelencoder.fit_transform(af[i])

"""* Correlation

I will delete some attributes that are high correlated with the interest rate
"""

af.corr().abs()['interest_rate'].sort_values(ascending = False)

af = af.drop('grade', axis=1)
af = af.drop('term', axis=1)
af = af.drop('sub_grade', axis=1)

#save the target variable in X->train and Y->test
#slpit the dataset to train and test
from sklearn.model_selection import train_test_split

X = af.drop(['interest_rate'],axis=1).values
y = af['interest_rate'].values

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.01)

from sklearn.metrics import mean_squared_error 
from sklearn.metrics import r2_score, accuracy_score,confusion_matrix
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor  
from sklearn.svm import SVR
from sklearn.model_selection import RandomizedSearchCV
from sklearn import linear_model

"""Mean squared error (MSE) measures the amount of error in statistical models. It assesses the average squared difference between the observed and predicted values. When a model has no error, the MSE equals zero. As model error increases, its value increases.

The mean absolute percentage error (MAPE) is the mean or average of the absolute percentage errors of forecasts. Error is defined as actual or observed value minus the forecasted value.

R-Squared (R² or the coefficient of determination) is a statistical measure in a regression model that determines the proportion of variance in the dependent variable that can be explained by the independent variable. In other words, r-squared shows how well the data fit the regression model.

###Random Forest
"""

# Fit the model on the training set
forest_out_of_the_box = RandomForestRegressor()
forest_out_of_the_box.fit(X_train, y_train)

# Predict on the test set
y_pred = forest_out_of_the_box.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error for forest_out_of_the_box: {mse:.7f}')
mbe=mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for forest_out_of_the_box: {mbe:.7f}')
r2=r2_score(y_test, y_pred)
print(f'r2 for forest_out_of_the_box: {r2:.7f}')

#grid search to find the best parameters for RandomForest
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
 
param_grid = [{'n_estimators':[50, 60, 70], 'max_depth':[10, 15 , 20], 'bootstrap':[True, False], 'max_features':[1, 2, 3]}]
forest = RandomForestRegressor()
grid_search = GridSearchCV(forest, param_grid, cv=5, scoring="neg_mean_squared_error")
grid_search.fit(X_train, y_train)
final = grid_search.best_params_
print(final)

#run with optimus
forest = RandomForestRegressor(bootstrap= False, max_depth= 20, max_features= 3, n_estimators= 60)
forest.fit(X_train,y_train)
y_pred = forest.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error for forest_out_of_the_box: {mse:.7f}')
mbe=mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for forest_out_of_the_box: {mbe:.7f}')
r2=r2_score(y_test, y_pred)
print(f'r2 for forest_out_of_the_box: {r2:.7f}')

"""###K-Nearest Neighbors Algorithm for Regression


KNN algorithm can be used for both classification and regression problems. The KNN algorithm uses ‘feature similarity’ to predict the values of any new data points. This means that the new point is assigned a value based on how closely it resembles the points in the training set.
"""

# Fit the model on the training set
knn_out_of_the_box = KNeighborsRegressor()
knn_out_of_the_box.fit(X_train, y_train)

# Predict on the test set
y_pred = knn_out_of_the_box.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error for knn_out_of_the_box: {mse:.7f}')
mbe=mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for knn_out_of_the_box: {mbe:.7f}')
r2=r2_score(y_test, y_pred)
print(f'r2 for knn_out_of_the_box: {r2:.7f}')

model = KNeighborsRegressor()
param_grid = {'n_neighbors':[45,50,55], 'weights':['uniform', 'distance']}
grid_search = GridSearchCV(model, param_grid, scoring="neg_mean_squared_error", cv=5)
grid_search.fit(X_train, y_train)
final=grid_search.best_params_
print(final)

#run with optimus

model = KNeighborsRegressor(n_neighbors= 45, weights= 'distance')
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

#
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error for knn after tuning: {mse:.7f}')
mbe=mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for knn after tuning: {mbe:.7f}')
r2=r2_score(y_test, y_pred)
print(f'r2 for knn after tuning: {r2:.7f}')

"""So we conlcude that the optimum parameters for both r2_score and neg_mean_squared_error are {'n_neighbors': 45, 'weights': 'distance'}.

###Lasso Regression

Support Vector Machines (SVMs) are well known in classification problems. These types of models are known as Support Vector Regression (SVR).
"""

# Fit the model on the training set
lasso_out_of_the_box = linear_model.Lasso()
lasso_out_of_the_box.fit(X_train, y_train)

# Predict on the test set
y_pred = lasso_out_of_the_box.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error for lasso_out_of_the_box: {mse:.7f}')
mbe=mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for lasso_out_of_the_box: {mbe:.7f}')
r2=r2_score(y_test, y_pred)
print(f'r2 for lasso_out_of_the_box: {r2:.7f}')

#grid search
lasso=linear_model.Lasso()
lasso_params = {'alpha':[ 0.005, 0.01 , 0.015 , 0.02 , 0.025]}
lass = GridSearchCV(lasso, lasso_params, cv=10 )
lass.fit(X_train, y_train)
final = lass.best_params_
print(final)

#run with optimus

model = linear_model.Lasso( 0.005, normalize=True)
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

#
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error for Lasso after tuning: {mse:.7f}')
mbe=mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for Lasso after tuning: {mbe:.7f}')
r2=r2_score(y_test, y_pred)
print(f'r2 for Lasso after tuning: {r2:.7f}')

"""###Results and Conclusion

If I had more time, I would try to improve the model by adding more features, trying different algorithms, Outlier check: (box plot, z-score ... ) , pipelines and/or using more advanced techniques such as hyperparameter tuning or ensembling.

  We observe that in most cases the GridSearch fails to produce better results and the default version of a model is better. There are many reasons for that. Either we failed to explore all the parameters that could help achieve a better result or we did not choose our metrics quite well. Also, it is really important to note that initianally we removed the attributes with the highest correlation in order to get a most realistic result, thus we deprived the models from the best variables.

  Bellow there are the results for the baseline model and with green/red colours the scores with the hyper parameters included. Also the are the plots of the baseline metrics (mse,mbe,r2_score).

  I made the assumption that the dataset is representative of the population of loans made through the Lending Club platform, and that the features in the dataset are relevant for predicting interest rate. My approach was to first identify any issues with the dataset and perform necessary data cleansing, then split the data into a training set and a test set and fit the model using the training set. Finally, I evaluated the model on the test set and made observations about its performance.

|  |  |   Random Forest   | kNN  | Lasso | 
| :-: | :-: | :-: | :-: | :-: | 
| **MSE** || 1.1172692 <br> <font color='red'>8.0238644</font> | 21.1991537<br> <font color='green'>17.9577164</font> | 9.5420270 <br> <font color='red'> 12.0710217 </font> | 66.79 <br> <font color='green'>+88.36</font> | 69.01 <br> <font color='green'>pending</font> |
|**MBE** |  | <br>  0.5733450<br><font color='green'>2.2761866 | 3.6925200 <br> <font color='red'> 3.5141383 </font> | 2.3998805 <br> <font color='green'>2.7883716</font> | 67.86 <br> <font color='green'>+66.94%<
**R2_score** | | 0.9472971 <br> <font color='red'> 0.6215050 </font> | 0.0000113<br> <font color='green'> 0.1529137 </font> | 0.5498915 <br> <font color='red'>0.4305959
"""

from typing import MutableSet

data = {'Random Forest':1.1172692, 'K-NN':21.1991537
, 'Lasso':9.5420270}
Models = list(data.keys())
MSE = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(Models, MSE, color ='maroon',
        width = 0.4)
 
plt.xlabel("Models use for prediction of Interest Rate")
plt.ylabel("Mean Squared Error")
plt.title("Baseline Results")
plt.grid(True)
plt.show()

data = {'Random Forest':0.5733450, 'K-NN':3.6925200
, 'Lasso': 2.3998805}
Models = list(data.keys())
MSE = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(Models, MSE, color ='maroon',
        width = 0.4)
 
plt.xlabel("Models use for prediction of Interest Rate")
plt.ylabel("Mean Absolute Error")
plt.title("Baseline Results")
plt.grid(True)
plt.show()

data = {'Random Forest': 0.9472971, 'K-NN':0.1602618
, 'Lasso': 0.5498915}
Models = list(data.keys())
MSE = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(Models, MSE, color ='maroon',
        width = 0.4)
 
plt.xlabel("Models use for prediction of Interest Rate")
plt.ylabel("R2")
plt.title("Baseline Results")
plt.grid(True)
plt.show()