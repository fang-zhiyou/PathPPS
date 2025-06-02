import time

import numpy as np
from matplotlib import pyplot as plt


def draw_path(graph, path1, path2, save: bool):
    rows, cols = graph.shape
    plt.figure(figsize=(cols * 0.3, rows * 0.3))

    for i in range(rows):
        for j in range(cols):
            if graph[i, j] == 1:
                plt.fill_between([j, j+ 1], i, i + 1, facecolor='gray', alpha=0.5)

    for node in path1:
        i, j = node
        plt.fill_between([j, j + 1], i, i + 1, facecolor='green', alpha=0.5)
    for node in path2:
        i, j = node
        plt.fill_between([j, j + 1], i, i + 1, facecolor='red', alpha=0.5)

    plt.xlim((0, cols))
    plt.ylim((rows, 0))

    plt.xticks(np.arange(0, cols, 1))
    plt.yticks(np.arange(0, rows, 1))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, linestyle='-', color='gray', alpha=0.7, zorder=0)
    plt.tight_layout()
    if save:
        plt.savefig(f'pics/{str(int(time.time()))}.png')
