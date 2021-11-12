import matplotlib.pyplot as plt
import config

# Draw cities as dots
def drawCities():
	info = config.CITIES
	plt.figure(figsize=(13, 10))
	for N, (x, y) in info.items():
		plt.plot(x, y, '.k', ms=0.7)
	# plt.show()

# Draw paths as lines between cities in the given path
def drawPaths(path):
	for idx in range(1, config.TOTAL_CITIES):
		x1, y1 = config.CITIES[path[idx]]
		x2, y2 = config.CITIES[path[idx - 1]]
		lineX = [x1, x2]
		lineY = [y1, y2]
		plt.plot(lineX, lineY, 'k-', alpha=0.3)

	x1, y1 = config.CITIES[path[config.TOTAL_CITIES-1]]
	x2, y2 = config.CITIES[path[0]]
	lineX = [x1, x2]
	lineY = [y1, y2]
	plt.plot(lineX, lineY, 'k-', alpha=0.3)

	plt.show()