from skopt import load
import pickle
import train
results = load('./result.pkl')
resultarray = []
for i in range(len(results.func_vals)):
    resultarray.append([results.func_vals[i], results.x_iters[i]])
print(resultarray)
