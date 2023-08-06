import pandas
import numpy
from sklearn import linear_model
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import assistant

skills_file = open("skillsFromItviec.txt", "r", encoding='utf-8', newline='')
read = skills_file.readlines()
skills = []
for row in read:
    skills.append(row.replace('\n', '').replace('\r', ''))

skills_file.close()

df_0 = pandas.read_csv('dataset/2_dataItviec.csv', delimiter=';')
df_1 = pandas.read_csv('dataset/2_dataJobsgo.csv', delimiter=';')
df_2 = pandas.read_csv('dataset/2_dataTopcv.csv',  delimiter=';')

df = pandas.concat([df_0,df_1,df_2], ignore_index = True)

scaler = MinMaxScaler()
df['Salary'] = scaler.fit_transform(df['Salary'].values.reshape(-1,1))

# df is the original data frame

X = df[['HN', 'HCM', 'else', 'Engineer', 'Manager', 'Dev', 'Administrator', 'Tester', 'Designer', 'Support', 'Analyst', 'Scientist'] + skills + ['Years of experience', 'Bachelor', 'Experience level']]
Y = df['Salary']
#print(X, Y)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)

#print(X, Y)

Linear_regression = linear_model.LinearRegression()
Linear_regression.fit(x_train, y_train)

result = Linear_regression.predict(x_test)

mse = mean_squared_error(y_test, result)
r2 = r2_score(y_test, result)
mae = mean_absolute_error(y_test, result)
rmse = mean_squared_error(y_test, result, squared = False)

print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("Mean Absolute Error (MAE):", mae)
print("R-squared (R2) Score:", r2)
