import pandas as pd #used for data handling/structor
import numpy as np  #used for arrays
import matplotlib.pyplot as plt #vishual presentation
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans 
from sklearn.metrics import silhouette_score 
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier

df=pd.read_csv(r"C:\Users\TEJU\Downloads\IBM_Dataset_Attrition_newfile.csv")
# print(df.dtypes)
missing_values=df.isnull().sum()
# print(missing_values)
df4=df.to_csv(r'C:\Users\TEJU\Downloads\IBM_Dataset_Attrition_newfile_updated_perceptron.csv',index=False)
#print(df.dtypes)
df['Age']=df['Age'].fillna(df['Age'].mean())
# print(df.isnull().sum())
df['MonthlyIncome']=df['MonthlyIncome'].fillna(df['MonthlyIncome'].mean())
# print(df.isnull().sum())

df = df.drop(['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours'],axis=1)
df5=df.to_csv(r'C:\Users\TEJU\Downloads\IBM_Dataset_Attrition_newfile_perceptron.csv',index=False)
# print(df.dtypes)

df['Attrition']=df['Attrition'].map({'Yes':0,
                                       'No':1})                                       
# print(df['Attrition'].value_counts())

df['Department']=df['Department'].map({'Sales':0,
                                       'Research & Development':1,
                                       'Human Resources':2})
# print(df['Department'].value_counts())

df['BusinessTravel']=df['BusinessTravel'].map({'Travel_Frequently':0,
                                                 'Travel_Rarely':1,
                                                 'Non-Travel':2})
# # # print(df.dtypes)
# print(df['BusinessTravel'].value_counts())

df['EducationField']=df['EducationField'].map({'Life Sciences':0,
                                               'Other':1,
                                               'Medical':2,
                                               'Marketing':3,
                                               'Technical Degree':4,
                                               
                                               'Human Resources':5})
# print(df['EducationField'].value_counts())


df['Gender']=df['Gender'].map({'Female':0,'Male':1})
# print(df['Gender'].value_counts())


df['JobRole']=df['JobRole'].map({'Sales Executive':0,
                                 'Research Scientist':1,
                                 'Laboratory Technician':2,
                                 'Manufacturing Director':3,
                                 'Healthcare Representative':4,
                                 'Manager':5,
                                 'Sales Representative':6,
                                 'Research Director':7,
                                 'Human Resources':8})
# print(df['JobRole'].value_counts())


df['MaritalStatus']=df['MaritalStatus'].map({'Single':0,
                                             'Married':1,
                                             'Divorced':2})
# print(df['MaritalStatus'].value_counts())


df['OverTime']=df['OverTime'].map({'Yes':0,'No':1})
# print(df['OverTime'].value_counts())

# df3=df.to_csv(r'C:\Users\TEJU\Downloads\IBM_Dataset_Attrition_newfile_updated.csv',index=False)

X=df.drop('Attrition',axis=1)
Y=df['Attrition']
X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.3,random_state=42)
sclar=StandardScaler()
X_train_scale=sclar.fit_transform(X_train)
X_test_scale=sclar.transform(X_test)

perceptron=Perceptron(max_iter=1000,random_state=42)
perceptron.fit(X_train_scale,y_train)

Y_pred_perceptron=perceptron.predict(X_test_scale)

from sklearn.neural_network import MLPClassifier

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train MLP
mlp = MLPClassifier(hidden_layer_sizes=(100,50),  # two hidden layers
                    activation='relu',
                    solver='adam',
                    max_iter=500,
                    random_state=42)
mlp.fit(X_train_scaled, y_train)

# Predictions
y_pred_mlp = mlp.predict(X_test_scaled)

# Evaluation
print("MLP Accuracy:", accuracy_score(y_test, y_pred_mlp))
print("\nClassification Report:\n", classification_report(y_test, y_pred_mlp))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_mlp))
# model=Perceptron 


