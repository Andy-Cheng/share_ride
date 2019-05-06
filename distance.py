# Author: Andy Cheng
# Email: andytony56791@gmail.com

import googlemaps
import numpy as np
import pandas as pd
from util import Car, write_to_excel
import random

if __name__ == '__main__':
    # Parse input
    data = pd.read_excel('data.xlsx')
    ori = data.values.tolist()[0][1:]
    des = data.values.tolist()[1][1:]
    ori_des_pair = []
    car_num = 8
    results = []
    for key, origin in enumerate(ori):
        ori_des_pair.append((origin, des[key]))
    random.shuffle(ori_des_pair)
    ori = []
    des = []
    for key, pair in enumerate(ori_des_pair[:(car_num * 5)]):
        ori.append(pair[0])
        des.append(pair[1])
    # 8 cars appear on the map at a moment.
    for i in range(car_num):
        car = Car(ori[(i * 5): (i * 5 + 5)], des[(i * 5): (i * 5 + 5)])
        result = car.run()
        results.append(result)
    write_to_excel(results)