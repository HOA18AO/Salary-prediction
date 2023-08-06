import assistant
import pandas

df = assistant.mergeDataFrame()
df = df[df['Salary'] < 90]
df.drop('Company', axis=1, inplace=True)
df.drop('URL', axis=1, inplace=True)
df.drop('QUALIFICATIONS', axis=1, inplace=True)

print(df.shape)
print(df.head)
df.to_csv("data.csv", sep=';', encoding='utf-8', index=False)
