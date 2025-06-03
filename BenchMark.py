import csv
import time
import random
import numpy as np
from fontTools.misc.cython import returns

import PPPN1
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import ShowPath

dataset_names = ['Beijing', 'Chicago', 'Feicheng', 'Sparse1', 'Sparse2', 'Sparse3']
cell_size = [14, 32, 14, 64, 64, 64]

for p in range(6):
    exp_results = []
    file_name = dataset_names[p]
    cell = cell_size[p]

    dataset_path = f'prodataset/{file_name}.npy'

    t1 = time.time()
    PPPN1.map_init(64, dataset_path)
    t2 = time.time()
    hcm_time = round((t2 - t1) * 1000, 2)
    print(f'HCM生成时间: {hcm_time} ms')
    print(f'地图的大小为：{PPPN1.get_map_size()} B')

    graph_data = np.load(dataset_path)
    choices = np.argwhere(graph_data == 1)

    for i in range(400):
        rst = []

        print(f'--------------- 第{i + 1}次查询 ---------------')
        pst = choices[random.randint(0, len(choices) - 1)]
        pen = choices[random.randint(0, len(choices) - 1)]

        PPPN1.st = PPPN1.get_point(int(pst[0]), int(pst[1]))
        PPPN1.en = PPPN1.get_point(int(pen[0]), int(pen[1]))
        # print(f'起始点: {int(pst[0]), int(pst[1])}, 终点: {int(pen[0]), int(pen[1])}')

        t1 = time.time_ns()
        route = PPPN1.run_algorithm()
        t2 = time.time_ns()
        print(f'PathPPS 结果，路径长度: {route}, 时间: {t2 - t1} ns')
        rst.append(route)
        rst.append((t2 - t1) / 1000000)
        rst.append(route * cell)

        grid = Grid(matrix=graph_data)
        start = grid.node(int(pst[1]), int(pst[0]))  # 起点
        end = grid.node(int(pen[1]), int(pen[0]))  # 终点
        finder = AStarFinder()
        nodes, len2 = finder.find_path(start, end, grid)

        route1 = []
        for node in nodes:
            route1.append((node.y, node.x))
        acc = len(nodes) / route
        print(f'A* 结果，路径长度: {len(nodes)}, 百分比: {acc * 100:.2f}%')
        # ShowPath.draw_path(graph_data, route, route1, True)
        rst.append(acc)

        # 优化准确率的计算方法或地图网格的生成算法

        exp_results.append(rst)

    with open(f'results/{file_name}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['PathPPS_len', 'PathPPS_time', 'Real_len', 'Acc'])  # 写入表头
        writer.writerows(exp_results)  # 写入多行
        # writer.writerow(['HCM(ms):', hcm_time, 'MapSize(K):', PPPN1.get_map_size()/1024])



# PathPPS长度 PathPPS时间 真实长度 准确度
#

