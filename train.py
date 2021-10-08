import skopt
import numpy as np
import datetime
import csv
from skopt import load

from algo2 import evaluateProfit


# SPACE = {"smallema": np.array([5, 10, 20]),
#          "bigema": [10, 20, 50, 100, 200],
#          "smallemasell": np.array([5, 10, 20]),
#          "bigemasell": [10, 20, 50],
#          "starttime": np.array([datetime.time(9, 30, 0), datetime.time(9, 45, 0), datetime.time(10, 0, 0), datetime.time(10, 15, 0), datetime.time(10, 30, 0), datetime.time(10, 45, 0), datetime.time(11, 0, 0), datetime.time(11, 15, 0), datetime.time(11, 30, 0), datetime.time(11, 45, 0), datetime.time(12, 0, 0), datetime.time(12, 15, 0), datetime.time(12, 30, 0), datetime.time(12, 45, 0), datetime.time(1, 0, 0), datetime.time(1, 15, 0), datetime.time(1, 30, 0), datetime.time(1, 45, 0), datetime.time(2, 0, 0), datetime.time(2, 15, 0), datetime.time(2, 30, 0), datetime.time(2, 45, 0), datetime.time(3, 0, 0), datetime.time(3, 15, 0)]),
#          "endtime": np.array([datetime.time(9, 45, 0), datetime.time(10, 0, 0), datetime.time(10, 15, 0), datetime.time(10, 30, 0), datetime.time(10, 45, 0), datetime.time(11, 0, 0), datetime.time(11, 15, 0), datetime.time(11, 30, 0), datetime.time(11, 45, 0), datetime.time(12, 0, 0), datetime.time(12, 15, 0), datetime.time(12, 30, 0), datetime.time(12, 45, 0), datetime.time(1, 0, 0), datetime.time(1, 15, 0), datetime.time(1, 30, 0), datetime.time(1, 45, 0), datetime.time(2, 0, 0), datetime.time(2, 15, 0), datetime.time(2, 30, 0), datetime.time(2, 45, 0), datetime.time(3, 0, 0), datetime.time(3, 15, 0), datetime.time(3, 30, 0)])}

SPACE = [skopt.space.space.Integer(1, 4, name='smallema'),
         skopt.space.space.Integer(2, 10, name='bigema'),
         skopt.space.space.Integer(1, 4, name='smallemasell'),
         skopt.space.space.Integer(2, 5, name='bigemasell'),
         skopt.space.space.Integer(9, 15, name='starthour'),
         skopt.space.space.Integer(13, 16, name='endhour'),
         skopt.space.Real(0.995, 1.005, name='alpha')]


@skopt.utils.use_named_args(SPACE)
def objective(**params):
    return -1.0 * evaluateProfit(params)


checkpoint_callback = skopt.callbacks.CheckpointSaver("./result.pkl")
prevresultarray = []
res_loaded = load('result.pkl')
for i in range(len(res_loaded.func_vals)):
    prevresultarray.append([res_loaded.func_vals[i], res_loaded.x_iters[i]])
print(f"Prev array: {prevresultarray}")
with open(f"out{datetime.datetime.now().hour}{datetime.datetime.now().minute}{datetime.datetime.now().second}.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(prevresultarray)
results = skopt.forest_minimize(
    objective, SPACE, n_calls=300, n_random_starts=60, callback=[checkpoint_callback])
resultarray = []
best_auc = -1.0 * results.fun
best_params = results.x
skopt.dump(
    results, 'result.pkl')
print(type(results))
print('best result: ', best_auc)
print('best parameters: ', best_params)
for i in range(len(results.func_vals)):
    resultarray.append([results.func_vals[i], results.x_iters[i]])
with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(resultarray)
