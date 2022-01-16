<h1 style="text-align: center;">Travelling Salesman Problem</h1>
<br>
<br>

## Program specification

### Basic execution

Execute `tsp_solve.py` with TSP problem file, for example `rl11849.tsp`

→ `python tsp_solver.py rl11849.tsp`

<br>

### Flags

| flag | details                                                         | need additional number argument? | Default |
| :--: | :-------------------------------------------------------------- | :------------------------------: | :-----: |
|  -v  | verbose; print out progress                                     |                No                |  False  |
|  -m  | 3-Opt mode; add this flag to use 3-Opt instead of 2-Opt         |                No                |  False  |
|  -g  | goal for Nearest Neighbor initialization; set custom goal value |               Yes                |    0    |
|  -f  | limit the total number of fitness evaluations                   |               Yes                |  1000   |
|  -p  | population size (NOT USED)                                      |               Yes                |   -1    |

<br>

### Usage

Usage example : `python tsp_solver.py rl11849.tsp -m -v -g 1234567 -f 1234 -p 99999`

Flags can be skipped. Default value will be used for skipped flags.
`python tsp_solver.py rl11849.tsp`
`python tsp_solver.py rl11849.tsp -v -f 2500`

Order does not matter.
`python tsp_solver.py rl11849.tsp -v -f 2500`
`python tsp_solver.py rl11849.tsp -f 2500 -v`

Some flags require additional number argument.
Fail) `python tsp_solver.py rl11849.tsp -f`
Success) `python tsp_solver.py rl11849.tsp -f 2500`

<br>
<br>

## Path representation

A path is represented with a list of unique numbers ranging from 1 to `TOTAL_CITIES`, where `TOTAL_CITIES` is 11849 for `rl11849.tsp`.

`path = [n for n in range(1, config.TOTAL_CITIES + 1)]`

<br>

## Fitness

Fitness is the total distance travelled in current TSP problem. Lower the better.

```python
def getFitness(path, distFunc):
	fitness = 0
	for idx in range(1, config.TOTAL_CITIES):
		fitness += distFunc(path[idx], path[idx - 1])
	return fitness
```

<br>
<br>

## Initialization

### Random

Random initialization is the simplest way to start search.

```python
# random path
path = [n for n in range(1, config.TOTAL_CITIES + 1)]
random.shuffle(path)
```

Despite its simplicity, the initial fitness is terribly high - `Fitness 87,153,074`.
Because our problem size is huge, search starting from random path often fell into local optima.
Another method is needed to initialize the path in more optimal way.

<br>

### Nearest Neighbor (NN)

Nearest Neighbor initialization is a **greedy** algorithm that finds and selects nearest city from current position. Available cities are kept in hash set and closest city from current position is selected as next city to explore.

```python
def nearestNeighbors(goal=10000000):
    avg_needed = goal/config.TOTAL_CITIES # desired avg distance between two cities to achieve goal fitness

    ...
    available = {n for n in range(1, config.TOTAL_CITIES+1)} # set
    path = []
    now = getRandomCity()

    # until path is complete
    while len(available) > 0:
        closest = -1 # next closest city to visit
        minDist = INF
        for nxtCity in available:
            d = distSquared(now, nxtCity) # squared distance - save time on sqrt
            if d < minDist:
                closest = nxtCity
                minDist = d

                if minDist < avg_needed ** 2: # distance is close enough - end search
                    break

        available.remove(closest)
        path.append(closest)
        now = closest
        ...
```

Time complexity for naive implementation of `nearestNeighbors` (tries to search all available city) is `O(N^2)`. This is too slow, so I made modification so that search for best next city ends if distance between two cities is close enough.

By 'close enough', distance should be lower than `avg_needed` value. This is desired average distance between two cities to achieve goal fitness.
`avg_needed = goal/config.TOTAL_CITIES`

<br>

Performance of `nearestNeighbors` is remarkable.
Although it takes more time when goal is more strictly set, the initial fitness is hugely improved compared to random initialization. Initial fitness can be reduced as close to 1,000,000.

|    goal     | 10,000,000 | 5,000,000 | 3,000,000 | 1,000,000 |
| :---------: | :--------: | :-------: | :-------: | :-------: |
| **fitness** | 6,768,118  | 3,501,804 | 2,259,937 | 1,237,746 |
| **time(s)** |    3.11    |   11.68   |   24.95   |   43.40   |

_Table 1. Nearest neighbor initialization with goal and corresponding result fitness and time taken_

<div style="page-break-after: always;"></div>
<br>

## Local Search

2-Opt and 3-Opt are tested and compared with each other.
2-Opt or 3-Opt is repeated until stopping condition `FITNESS_CNT`, which is set with flag `-f`, is met.

```python
def run_localSearch(path, use_ThreeOpt=False):
    ...

    while True:
        city1 = getRandomCity()
        city2 = getRandomCity(city1+1)

        new_path = TwoOpt(path, city1, city2)
        if config.FITNESS_CNT:
            newFitness = getFitness(new_path, dist)
            config.FITNESS_CNT -= 1
        else: # stopping condition
            return path
```

<br>

### 2-Opt

Select single segment and re-order the crossing.

```Python
# Choose single segment (i,j) and re-order
def TwoOpt(path, i, j):
	new_path = path[:i]
	new_path += list(reversed(path[i:j+1]))
	new_path += path[j+1:]
	return new_path
```

<br>

### 3-Opt

Given three distinct segments, there are 8 ways to re-order the segments.
One is the original path itself, three 2-opt cases, and 4 3-opt cases.

![3opt_cases](C:\Users\Park\Desktop\CS454 SBSE\Assignment 3 - TSP\report\3opt*cases.png)
\_Fig 1. 8 cases of 3-opt reconnection*

```python
# Choose 3 distinct segments A(i1, j1), B(i2, j2), C(i3, j3)
def ThreeOpt(path, i1, j1 ,i2, j2, i3, j3):
	new_paths = [] # an array of paths

	# 1. identity - 1 case
	# new_paths.append(path)

	# 2. Two opt - 3 cases
    # A'BC, AB'C, ABC' (' means reversed)
	TwoOpt_paths = [TwoOpt(path, i1, j1), TwoOpt(path, i2, j2), TwoOpt(path, i3, j3)]
	new_paths += TwoOpt_paths

	# 3. Three opt - 4 cases
	ThreeOpt_paths = []
    # A'BC'
	ThreeOpt_paths.append(path[i2:j2+1] + path[j2+1:i3]
                          + list(reversed(path[i3:j3+1])) + path[j3+1:] + path[:i1]
                          + list(reversed(path[i1:j1+1])) + path[j1+1:i2])
    # A'B'C
	ThreeOpt_paths.append(path[i3:j3+1] + path[j3+1:] + path[:i1]
                          + list(reversed(path[i1:j1+1])) + path[j1+1:i2]
                          + list(reversed(path[i2:j2+1])) + path[j2+1:i3])
    # AB'C'
	ThreeOpt_paths.append(path[i1:j1+1] + path[j1+1:i2]
                          + list(reversed(path[i2:j2+1])) + path[j2+1:i3]
                          + list(reversed(path[i3:j3+1])) + path[j3+1:] + path[:i1])
    # A'B'C'
	ThreeOpt_paths.append(path[:i1] + list(reversed(path[i1:j1+1])) + path[j1+1:i2]
                          + list(reversed(path[i2:j2+1])) + path[j2+1:i3]
                          + list(reversed(path[i3:j3+1])) + path[j3+1:])
	new_paths += ThreeOpt_paths

	return new_paths # an array of paths
```

When a better path is found using 2-Opt or 3-Opt, replace current path with better path and run local search on updated path again.

<br>
<br>

## Result

command line used to execute solver
2-opt : `python tsp_solver.py rl11849.tsp -f 3000 -g {goal}`
3-opt : `python tsp_solver.py rl11849.tsp -f 3000 -g {goal} -m`

3 goals investigated : 10,000,000 / 3,000,000 / 1,000,000
3000 fitness evaluations set as stopping condition

| goal  | 10,000,000 | 3,000,000 | 1,000,000 |
| ----- | ---------- | --------- | --------- |
| 2-opt | 6,751,113  | 2,248,263 | 1,243,501 |
| 3-opt | 6,746,829  | 2,254,984 | 1,247,258 |

_Table 2. Fitness after 3000 evaluations for 2-opt and 3-opt. Different goal produces different starting path._

<br>

### Overall

First of all, Nearest Neighbor(NN) initialization is very strong. NN with goal 1,000,000 produced initial path with fitness around 1,300,000. After that, 2-opt and 3-opt barely found any better paths within 3000 trials of fitness evaluations. Likewise, overall improvements by 2-Opt and 3-Opt were minimal. Most fitness improvements came from NN initialization, and local search only contributed to small fitness optimization.

One reason for this may be largely due to randomness in choosing segment and the size of the problem. Segments for 2-Opt and 3-Opt are selected randomly. Because the problem size is big, majority of the new paths found from 2-Opt and 3-Opt were worse (miss).

To compensate for this, a lot more trial than 3000 is needed. This actually helps, as I've ran 2-opt local search for 6 hours from random initialized path and could reduce the fitness 86,904,764 to 18,436,226.

### 2-Opt vs 3-Opt

Empirically, it seemed like 3-Opt isn't any better than 2-Opt. This was counter-intuitive as 3-Opt is expected to have wider search area in the landscape as it swaps 3 segments around. Also, 3-Opt took significantly more time than 2-Opt. So with NN initialization, 2-Opt is preferable over 3-Opt as 2-Opt produces similar result and takes less time.

<br>

Below is the rough visualization of TSP path according to the path fitness.
The lower the fitness is, the clearer the path becomes. Some of the black lines that connects two dots far away are signs of non-optimal path.

![tsp_visualize](C:\Users\Park\Desktop\CS454 SBSE\Assignment 3 - TSP\report\tsp*visualize.jpg)
\_Fig 2. Rough visualization (X, Y coordinate) of path found for rl11849.tsp : path with fitness 8 million (left), 3.5 million (middle), 1.5million (right)*

In conclusion, Nearest Neighbor initialization and 2-opt local search is both simple and effective in optimizing TSP problem, but still far away from optimal solution.

### Possible improvements

Initial path produced by NN with goal 1,000,000 can hardly be improved with 2-opt/3-opt local search anymore. To escape local optima, simulated annealing is worth trying. If local search method itself is the problem, genetic algorithm can also be considered.

<br>

<br>

## References

- Hansen, P., & Mladenović, N. (2006). First vs. best improvement: An empirical study. _Discrete Applied Mathematics_, _154_(5), 802–817. https://doi.org/10.1016/j.dam.2005.05.020
- Sang-Un, L. (2015). Optimal Solution of a Large-scale Travelling Salesman Problem applying DNN and k-opt. _The Journal of the Institute of Internet, Broadcasting and Communication_, 15(4), 249-257. http://dx.doi.org/10.7236/JIIBC.2015.15.4.249
