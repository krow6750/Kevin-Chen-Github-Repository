import pandas as pd
import statistics

births = pd.read_csv('births.csv') #1 rename dataframe

births.columns = ['month', 'day', 'births', 'a/b', 'omit'] #2 renamed column names

births = births.loc[:, :'a/b'] #3 splices out the omit column

avg = births["births"].mean() #4 determines overall mean number of births

median = births["births"].median() #5 determines overall median number of births
print(avg)
print(median)


num_births = list(births["births"]) #6 determines mean and median number of births using statistics library
actual_mean = statistics.mean(num_births)
actual_median = statistics.median(num_births)
#print("actual_mean: ", actual_mean)
#print("actual_median: ", actual_median)

sorted = births.sort_values("births") #7 sorts by num of births
#print(sorted)


sanity_median = sorted[185:187] #8 confirms above and below breakpoint
#print(sanity_median)

#print(sorted[sorted["births"] >= median].iloc[0]) #9 prints the first row in the list of all rows above the median
#print(sorted[sorted["births"] <= median].iloc[-1]) #10 prints the last row in the list of all rows above the median

byMonth = births.groupby("month")
print(byMonth.to_string(header = False))
#print(births.to_string())
