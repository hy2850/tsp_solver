Representation

Individual - an array of 11849 cities in specific order

Population - a list of M individuals



Operator

order is important

cross-over between two individuals may cause duplicate cities for visit

cross-over -> in one individual, choose a point and swap order of segment

indiv1 = [A, B] -> [B, A]

mutation -> choose a single city, swap it with any random other city in the individual



Fitness 

Distance travelled





Tournament + Total replacement





class로 만드는게 좋겠다.

pop

indiv



공용 global 변수 관리

https://stackoverflow.com/questions/13034496/using-global-variables-between-files/13034908

config.py, settings.py 같은거 만들어두고 거기서 관리





31Oct21 - 대강 코드는 완성했는데, Gen 4 이후로 수렴해버림 (local optima?)





3Nov21 - 버그 수정 + PMX crossover 구현.

딱히 크게 달라진 건 없음





4Nov21 - GA가 계속 수렴해서 이것 저것 바꿔봤지만 성능이 크게 나아지지 않음.

너무 N이 커서, 랜덤한 방식으로는 한계가 있는걸까?

local search - 2opt 구현해봄.

확실히 fitness 팍팍 개선되는데, 그 속도가 너무 느림. 한 6시간 돌려야 반 정도로 줄어드는 수준?





5Nov21 

### NN init 추가

http://tsp-basics.blogspot.com/2017/02/tour-construction-nearest-neighbor-nn.html



### 문제점 - NN 너무 느린데?

O(N^2) 일텐데 너무 느림; 

대안1) 너무 Nearest 찾으려 하지 말고, 적당한 선에서 for문 break

→ 11849개의 도시가 있고, 난 최대 2천만까지는 원함

대안2) dist 문제인가? math.sqrt 하지말고, 제곱 형태로 그냥 ㄱㄱ

→ O(N^2)을 극복하진 못함. 별 차이 없는 듯 (일단 두기)



마찬가지로 2-Opt 돌릴 때, A와 B dist가 너무 멀면 





8Nov21 

### NN 최적화

goal을 인자로 받아서, 적당히 avg_needed 찾으면 for문 break - 1분 걸리던게 1초로 짧아짐 미친 ㅋㅋ (goal 천만)

Optimal sol : 923288 ([출저](http://www.math.uwaterloo.ca/tsp/rl11849/rl11849_sol.html))

니까, goal 2백만~5백만 정도로 잡고 2-Opt로 최적화하기

goal 1000000 - 45초 정도 걸리고, fitness 110만 정도로 시작



### Python flag argument

argparse? sys.argv?
https://stackoverflow.com/questions/8259001/python-argparse-command-line-flags-without-arguments

python namespace
use namespace as dict - https://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary



### 2-Opt 최적화

1. city 1부터 thoroughly 탐색, 

2. dist 멀면 pass로 최적화 해보려 했는데,

```python
for city1 in range(1, config.TOTAL_CITIES + 1):
	for city2 in range(city1+1, config.TOTAL_CITIES+1):
		if dist(city1, city2) > SEARCH_DIST_LIMIT:
			if VERBOSE:
				print(f"{city1} - {city2} too far - pass")
			continue
```

1 문제점 - 대부분 miss (worse fitness)

거의 NN init으로 fitness를 확 줄였고, local search로는 가뭄에 콩나듯 hit → stochastic optimisation 아니라고 점수 존나 깎을수도

2 문제점 - 멀리 떨어져 있어도, 둘 사이에 꼬인 경로를 풀어주면 fitness 개선될 수도 있음 - 부적절?



그리고 아래와 같이 고칠까 말까 고민중인데, city 넘버 받으면 path에서 index을 찾아야하지 않나

city 정보 사용 안할꺼면 바로 i, j 받아서 2-Opt 돌려도 되긴 한데..

 ```python
 def TwoOpt(path, city1, city2):
 	i = path.index(city1)
 	j = path.index(city2)
 ```



simulated annealing 적용? accept some worse solutions



Most local search algorithms apply one of the three strategies: random, best improvement, and prioritization

난 random?

https://www.frontiersin.org/articles/10.3389/frobt.2021.689908/full



fitness (total travel dist) history
Init : 86904764
Gen 10000 : 56074904 (1시간)
Gen 20000 : 38386621
Gen 30000 : 26448120 (3시간)
Gen 40000 : 18436226 (3시간)
