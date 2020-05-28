import pandas as pd
excel1 = "D:\\www\\SeleniumWWS\\Data\\employee1.xlsx"
excel2 = "D:\\www\\SeleniumWWS\\Data\\employee2.xlsx"
df1 = pd.read_excel(excel1)
df2 = pd.read_excel(excel2)

#print(df1.columns)
#print(df2.columns)
#print(df1['EmployeeID'].isin(df2['EmployeeID']))
#filter df1 data by if existing in df2
filter_df1 = df1.loc[(df1['EmployeeID'].isin(df2['EmployeeID']))]
#filter df1 data by if no existing in df2
filter_df2 = df1.loc[~(df1['EmployeeID'].isin(df2['EmployeeID']))]
#print(filter_df2)

#filter data by multiple conditions & and |
filter_df3 = df1.loc[(df1['EmployeeID'].isin(df2['EmployeeID'])) | (df1['Salary'] > 200)]
print(filter_df3)

all_df = pd.merge(df1, df2, how='outer', on="EmployeeID")
all_df = pd.merge(df1, df2, how='inner', on="EmployeeID")
print(all_df.columns)

filter_df4 = all_df.loc[(all_df['Salary'] > 200) & (all_df['Level'] >= 2)]
print(filter_df4)

#merge = pd.merge(df1, df2, on="EmployeeID")
#print(merge)
#merge.to_excel("D:\\www\\SeleniumWWS\\Data\\employee_merge.xlsx")