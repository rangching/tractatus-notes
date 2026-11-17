"""EP04 練習題答案：圖像論——巴黎法庭的玩具車。
與 sims/u04.html 使用同一套路口模型：
  8×8 格的棋盤，第 3、4 列與第 3、4 行是道路（十字路口），共 28 個道路格。
  每台車有「位置（道路格）」與「方向（北東南西）」。
  圖像（模型）斷言的事態：每台車在哪個路段、朝哪個方向；哪兩台車的行進路徑交會；哪台車的正前方會碰到另一台車。
  模型為真 ⇔ 它斷言的事態集合，與現場（實在）成立的事態集合完全相同。
執行：python3 calc_u04.py
"""
from itertools import permutations, product

N = 8
ROAD = [(r, c) for r in range(N) for c in range(N) if r in (3, 4) or c in (3, 4)]
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]          # 0 北 1 東 2 南 3 西
DIR_ZH = "北東南西"

def zone(r, c):
    if r in (3, 4) and c in (3, 4): return "中央"
    if c in (3, 4): return "北段" if r < 3 else "南段"
    return "西段" if c < 3 else "東段"

def path(r, c, d):
    """從車的位置沿方向往前走，經過的道路格（不含自己）。"""
    out = []; dr, dc = DIRS[d]; r += dr; c += dc
    while 0 <= r < N and 0 <= c < N and (r, c) in ROAD_SET:
        out.append((r, c)); r += dr; c += dc
    return out
ROAD_SET = set(ROAD)

def facts(cars):
    """cars: {名稱: (r, c, d)} → 成立的事態集合（frozenset）。"""
    F = set(); P = {}
    for k, (r, c, d) in cars.items():
        F.add(("在", k, zone(r, c))); F.add(("朝", k, DIR_ZH[d])); P[k] = path(r, c, d)
    ks = sorted(cars)
    where = {cars[k][:2]: k for k in ks}
    for a in ks:
        first = next((where[x] for x in P[a] if x in where), None)   # 正前方遇到的第一台車
        if first: F.add(("前方碰到", a, first))
        for b in ks:
            # 兩台車行進方向垂直、而且前方路徑有共同的格子 → 路徑交會
            if a < b and cars[a][2] % 2 != cars[b][2] % 2 and set(P[a]) & set(P[b]):
                F.add(("路徑交會", a, b))
    return frozenset(F)

# 現場一：路口擦撞（與 sim 相同）
REAL1 = {"紅": (5, 4, 0), "藍": (3, 6, 3)}

# ---------- Q1：圖像涉及 5 個彼此獨立的事態，可以呈現幾種不同的事況
Q1 = 2 ** 5

# ---------- Q2：兩台模型車（不可重疊）、每台 4 個方向，一共有幾種擺法
Q2 = len(ROAD) * (len(ROAD) - 1) * 4 * 4
assert Q2 == sum(1 for a, b in permutations(ROAD, 2) for _ in product(range(4), repeat=2))

# ---------- Q3：在「路口擦撞」現場，有幾種擺法會讓模型為真（呈現同一個事況）
target = facts(REAL1)
Q3 = sum(1 for a, b in permutations(ROAD, 2) for da, db in product(range(4), repeat=2)
         if facts({"紅": (*a, da), "藍": (*b, db)}) == target)

# ---------- Q4：三台模型車對應三台真車，元素對應（投影方式）有幾種
Q4 = sum(1 for _ in permutations(["紅", "藍", "黃"]))

print("道路格數 =", len(ROAD))
print("現場一成立的事態：", sorted(target))
print("Q1 5 個獨立事態可呈現的事況數 2^5        =", Q1)
print("Q2 兩台車的模型擺法數 28×27×4×4          =", Q2)
print("Q3 其中與『路口擦撞』現場相符（為真）的擺法 =", Q3, f"（占 {Q3/Q2:.2%}）")
print("Q4 三台車的元素對應方式 3!                =", Q4)
print("--- 參考：比對的結果只有兩種：符合（真）或不符合（假）")
