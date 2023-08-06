import pandas
import numpy
from sklearn import linear_model
from sklearn.linear_model import Ridge
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

import assistant

skills_file = open("skillsFromItviec.txt", "r", encoding='utf-8', newline='')
read = skills_file.readlines()
skills = []
for row in read:
    skills.append(row.replace('\n', '').replace('\r', ''))

skills_file.close()

df = assistant.mergeDataFrame()
df = df[df['Salary'] < 90]

scaler = MinMaxScaler()

df['Salary'] = scaler.fit_transform(df['Salary'].values.reshape(-1,1))

X = df[['HN', 'HCM', 'else', 'Engineer', 'Manager', 'Dev', 'Administrator', 'Tester', 'Designer', 'Support', 'Analyst', 'Scientist'] + skills + ['Years of experience', 'Bachelor', 'Experience level']]
Y = df['Salary']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)

ridge = Ridge(alpha=0.5)
ridge.fit(x_train, y_train)

result = ridge.predict(x_test)

'''
salary_y_test =  scaler.inverse_transform(y_test.values.reshape(-1,1)).reshape(-1)
predictions = scaler.inverse_transform(result.reshape(-1,1)).reshape(-1)
'''

mse = mean_squared_error(y_test, result)
r2 = r2_score(y_test, result)
mae = mean_absolute_error(y_test, result)
rmse = mean_squared_error(y_test, result, squared = False)

""" 
# chart
plt.figure(figsize=(10,6))
sns.regplot(x=y_test,y=result,ci=None,scatter_kws={'color': 'blue'}, line_kws={'color': 'red'})
plt.xlabel('True')
plt.ylabel('Prediction')
plt.legend(['True value', 'Linear regression'])
plt.show()
"""

print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("Mean Absolute Error (MAE):", mae)
print("R-squared (R2) Score:", r2)
