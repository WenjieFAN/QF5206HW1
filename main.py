import math
import statsmodels.api as sm
import pandas as pd
import numpy

tickers = pd.read_csv(r'C:\Users\alien\Desktop\tickers.csv', header=None)
adjusted = pd.read_csv(r'C:\Users\alien\Desktop\adjusted.csv', header=None)
in_univ = pd.read_csv(r'C:\Users\alien\Desktop\in_univ.csv', header=None)
dateline = pd.read_csv(r'C:\Users\alien\Desktop\dateline.csv', header=None)

# part 1
# list of 2019 and 2020
list_2019 = in_univ.iloc[17, :]
list_2020 = in_univ.iloc[18, :]
# print(list_2019)

# list of GICS code
GICS = tickers.iloc[:, 1]

for i in range(len(GICS)):
    if math.isnan(GICS[i]):
        GICS[i] = 0.0
    GICS[i] = int(GICS[i] / 100)

GICS_2019 = GICS.copy()
GICS_2020 = GICS.copy()

for i in range(len(list_2019)):
    if list_2019[i] == 0:
        GICS_2019[i] = 0
print(GICS_2019.value_counts(ascending = False))

for i in range(len(list_2020)):
    if list_2020[i] == 0:
        GICS_2020[i] = 0
print(GICS_2020.value_counts(ascending = False))

# part 2
index_JPM = list(tickers.iloc[:, 0]).index('JPM')
print(int(GICS[index_JPM]))

list_JPM_industry = []
list_JPM_industry_index = []
for i in range(len(GICS_2020)):
    if GICS_2020[i] == GICS[index_JPM]:
        list_JPM_industry_index.append(i)
        list_JPM_industry.append(tickers.iloc[:, 0][i])

print(list_JPM_industry)

# part 3
start_date_index = list(dateline.iloc[:, 0]).index(list(dateline.iloc[:, 0])[-1] - 50000) + 1
end_date_index = list(dateline.iloc[:, 0]).index(list(dateline.iloc[:, 0])[-1])

# calculating the return rate
return_in_stock = [0]*(end_date_index - start_date_index)
for i in range(end_date_index - start_date_index):
    for j in list_JPM_industry_index:
        return_in_stock[i] += (adjusted.iloc[i+start_date_index+1, j] - adjusted.iloc[i+start_date_index, j]) / \
                              adjusted.iloc[i+start_date_index, j]
    return_in_stock[i] = return_in_stock[i] / len(list_JPM_industry_index)
print(return_in_stock)

return_JPM = [0]*(end_date_index - start_date_index)
for i in range(end_date_index - start_date_index):
    return_JPM[i] += (adjusted.iloc[i+start_date_index+1, index_JPM] - adjusted.iloc[i+start_date_index, index_JPM]) / \
                     adjusted.iloc[i+start_date_index, index_JPM]
print(return_JPM)

X = numpy.array(return_in_stock)
Y = numpy.array(return_JPM)

X = sm.add_constant(X)
results = sm.OLS(Y, X).fit()
print(results.summary())