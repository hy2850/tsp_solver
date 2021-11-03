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



