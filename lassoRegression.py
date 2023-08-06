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

df_0 = pandas.read_csv('dataset/1_dataItviec.csv', delimiter=';')
df_1 = pandas.read_csv('dataset/1_dataJobsgo.csv', delimiter=';')
df_2 = pandas.read_csv('dataset/1_dataTopcv.csv',  delimiter=';')

df = pandas.concat([df_0,df_1,df_2], ignore_index = True)

test_df = df.loc[df["Salary average"] == -1]

for i in range(df.shape[0]-1):
    if int(df["Salary average"][i]) == -1:
        #test_df.append(df.iloc[i])
        df = df.drop(i)
        i-=1
df = pandas.concat([df], ignore_index = True)

scaler = MinMaxScaler()
df['Salary average'] = scaler.fit_transform(df['Salary average'].values.reshape(-1,1))

# df is the original data frame

X = df[skills + ['Minimum years of exp', 'Bachelor', 'Experience level']]
Y = df['Salary average']
#print(X, Y)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)


lasso_linear = linear_model.Lasso(alpha=1.0)
lasso_linear.fit(x_train, y_train)
# Evaluating the model
result = lasso_linear.predict(x_test.values)
print(y_test.values)
#score_trained = lasso_linear.score(x_test, y_test)

mse = mean_squared_error(y_test, result)
r2 = r2_score(y_test, result)
mae = mean_absolute_error(y_test, result)
rmse = mean_squared_error(y_test, result, squared = False)

print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("Mean Absolute Error (MAE):", mae)
print("R-squared (R2) Score:", r2)