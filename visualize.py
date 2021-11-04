import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import config

def drawCities():
	info = config.CITIES
	plt.figure(figsize=(13, 10))
	for N, (x, y) in info.items():
		plt.plot(x, y, '.k', ms=0.7)
	# plt.show()

# @args indiv : Individual instance with path info
def drawPaths(indiv):
	path = indiv.path
	for idx in range(1, config.TOTAL_CITIES):
		x1, y1 = config.CITIES[path[idx]]
		x2, y2 = config.CITIES[path[idx - 1]]
		lineX = [min(x1, x2), max(x1, x2)]
		lineY = [min(y1, y2), max(y1, y2)]
		plt.plot(lineX, lineY, 'k-', alpha=0.3)
	# plt.show()

# Q. some points are not connected at all?