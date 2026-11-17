"""EP03 練習題答案：對象、事態與邏輯空間。
2.061 事態彼此獨立 → n 個事態構成 n 維「邏輯空間」：每個可能世界是 n 維超立方體 {0,1}^n 的一個頂點，
只差一個事態的兩個世界之間連一條邊。本程式實際建圖、數頂點與邊，並用 BFS 驗證距離。
執行：python3 calc_u03.py
"""
from itertools import product
from collections import deque

def cube(n):
    V = list(product([0, 1], repeat=n))
    E = [(u, v) for i, u in enumerate(V) for v in V[i + 1:] if sum(a != b for a, b in zip(u, v)) == 1]
    return V, E

def bfs_dist(n, start):
    V, E = cube(n)
    adj = {v: [] for v in V}
    for u, v in E:
        adj[u].append(v); adj[v].append(u)
    dist = {start: 0}; q = deque([start])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1; q.append(w)
    return dist, adj

V4, E4 = cube(4)
start = (1, 0, 1, 0)
dist, adj = bfs_dist(4, start)
gray = [i ^ (i >> 1) for i in range(16)]
gray_ok = all(bin(gray[i] ^ gray[i + 1]).count("1") == 1 for i in range(15))

print("Q1 4 個事態的可能世界數（超立方體頂點）       =", len(V4))
print("Q2 4 維超立方體的邊數（只差一個事態的世界對） =", len(E4), "；公式 n·2^(n-1) =", 4 * 2 ** 3)
print("Q3 任一世界的相鄰世界數（n=4）                 =", len(adj[start]))
print("Q4 與某世界恰好差 2 個事態的世界數（n=4）      =", sum(1 for d in dist.values() if d == 2))
print("--- 參考：從 1010 出發，各距離的世界數         =", {d: sum(1 for x in dist.values() if x == d) for d in range(5)})
print("--- 參考：n=1..4 頂點／邊                      =", [(n, len(cube(n)[0]), len(cube(n)[1])) for n in range(1, 5)])
print("--- 參考：4 位元 Gray code 每步只改一個事態    =", gray_ok, [format(g, "04b") for g in gray])
