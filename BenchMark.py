import time
import random
import numpy as np
import PPPN1
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import ShowPath

dataset_path = 'datasets/CountrySide1.npy'

t1 = time.time()
PPPN1.map_init(64, dataset_path)
t2 = time.time()
print(f'HCM生成时间: {round((t2 - t1) * 1000, 2)} ms')

graph_data = np.load(dataset_path)
choices = np.argwhere(graph_data == 1)

for i in range(10):
    print(f'--------------- 第{i + 1}次查询 ---------------')
    pst = choices[random.randint(0, len(choices) - 1)]
    pen = choices[random.randint(0, len(choices) - 1)]

    PPPN1.st = PPPN1.get_point(int(pst[0]), int(pst[1]))
    PPPN1.en = PPPN1.get_point(int(pen[0]), int(pen[1]))
    print(f'起始点: {int(pst[0]), int(pst[1])}, 终点: {int(pen[0]), int(pen[1])}')
    # print(graph_data[int(pst[0]), int(pst[1])], graph_data[int(pen[0]), int(pen[1])])

    t1 = time.time_ns()
    route = PPPN1.run_algorithm()
    t2 = time.time_ns()
    print(f'PathPPS 结果，路径长度: {len(route)}, 时间: {t2 - t1} ns')

    grid = Grid(matrix=graph_data)
    start = grid.node(int(pst[1]), int(pst[0]))  # 起点
    end = grid.node(int(pen[1]), int(pen[0]))  # 终点
    finder = AStarFinder()
    nodes, len2 = finder.find_path(start, end, grid)

    route1 = []
    for node in nodes:
        route1.append((node.y, node.x))
    print(f'A* 结果，路径长度: {len(nodes)}, 百分比: {len(nodes)/len(route) * 100:.2f}%')
    # ShowPath.draw_path(graph_data, route, route1, True)

    # 优化准确率的计算方法或地图网格的生成算法

