import pandas


df = pandas.read_csv('dataItviec.csv', delimiter=';')
i = 1
for i in range(1, 7):
    path = 'dataset/' + str(i) + '_'
    df0 = pandas.read_csv(path+'dataItviec.csv', delimiter=';')
    df1 = pandas.read_csv(path+'dataJobsgo.csv', delimiter=';')
    df2 = pandas.read_csv(path+'dataTopcv.csv', delimiter=';')
    df = df.append(pandas.concat([df0, df1, df2], ignore_index = True))
    df = df.drop_duplicates(keep='first')

print(df.shape)

