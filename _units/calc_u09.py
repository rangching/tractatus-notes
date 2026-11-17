"""EP09 練習題答案：N 運算與命題的一般形式（5.5–5.52、6–6.03）。
N(ξ̄)：把括號內所有命題都否定再合取＝「全部為假時才為真」（5.502、5.51：一個值 N=~p；兩個值 N=~p.~q）。
真值函數以 4 位元遮罩表示，位元 i 對應 5.101 的第 i 個真值可能性：(p,q) = (W,W)、(F,W)、(W,F)、(F,F)。
  N(S) = ~(s1 ∨ s2 ∨ …) = FULL & ~OR(S)。

本程式算三種「最少」：
  (A) 層數（深度）：G0={p,q}；G_{k+1} = G_k ∪ { N(S) : S 為 G_k 的任意非空子集 }。f 第一次出現的 k。
  (B) 最少 N 次數（可重複使用已生成的命題，＝ sims/u09.html 遊樂場的步數）：
      狀態＝已生成命題的集合，從 {p,q} 出發；一步＝對目前集合的任意非空子集按一次 N，把結果加入集合。
      以 BFS 求得到 f 所需的最少步數，以及集齊全部 16 個所需的最少步數。
  (C) 寫成一條式子（樹狀、不共用子式）時 N 符號的最少個數，例如 p∧q = N(N(p),N(q)) 要 3 個。
執行：python3 calc_u09.py
"""
from collections import deque
from itertools import combinations

FULL = 0b1111
P, Q = 0b0101, 0b0011           # p 在第 0、2 列為真；q 在第 0、1 列為真
def col(m): return "".join("W" if m >> i & 1 else "F" for i in range(4))
def N(*fs):
    o = 0
    for f in fs: o |= f
    return FULL & ~o

NAMES = {0b1111: "重言式", 0b1110: "~(p∧q)", 0b1101: "q→p", 0b1011: "p→q", 0b0111: "p∨q",
         0b1100: "~q", 0b1010: "~p", 0b0110: "p⊻q（互斥或）", 0b1001: "p↔q", 0b0101: "p",
         0b0011: "q", 0b1000: "~p∧~q", 0b0100: "p∧~q", 0b0010: "q∧~p", 0b0001: "p∧q", 0b0000: "矛盾式"}
# 依 5.101 順序列出（真值欄字串）
ORDER = ["WWWW", "FWWW", "WFWW", "WWFW", "WWWF", "FFWW", "FWFW", "FWWF",
         "WFFW", "WFWF", "WWFF", "FFFW", "FFWF", "FWFF", "WFFF", "FFFF"]
mask_of = {col(m): m for m in range(16)}
assert {col(m) for m in NAMES} == set(ORDER)
assert NAMES[mask_of["WWFW"]] == "p→q" and NAMES[mask_of["WFWF"]] == "p" and NAMES[mask_of["WWFF"]] == "q"

def unions(G):
    """G 的所有非空子集的「或」值（只需值，不需子集本身）。"""
    U = set()
    for g in G:
        U |= {u | g for u in U}; U.add(g)
    return U

# ---------- (A) 層數
layer = {P: 0, Q: 0}; G = {P, Q}; k = 0; per_layer = [sorted(G)]
while len(G) < 16:
    k += 1
    new = {FULL & ~u for u in unions(G)} - G
    for f in new: layer[f] = k
    G |= new; per_layer.append(sorted(new))
LAYERS = k

# ---------- (B) 最少 N 次數（狀態 BFS）
start = frozenset({P, Q})
dist = {start: 0}; dq = deque([start]); first = {P: 0, Q: 0}; all16 = None
while dq:
    s = dq.popleft(); d = dist[s]
    if len(s) == 16 and all16 is None: all16 = d
    if len(first) == 16 and all16 is not None: break
    for u in unions(s):
        f = FULL & ~u
        if f in s: continue
        t = s | {f}
        if t not in dist:
            dist[t] = d + 1; dq.append(t)
            first.setdefault(f, d + 1)

# ---------- (C) 樹狀式子的 N 個數：cost[f] = 1 + min{ Σ cost(s) : OR(S) = ~f }
INF = 10 ** 9
cost = {m: INF for m in range(16)}; cost[P] = cost[Q] = 0
changed = True
while changed:
    changed = False
    # best[u]：一組命題（可多個）其「或」恰為 u 時的最小總成本
    # （只算非空集合：矛盾式的「或」也是 0，不能和空集合混在一起）
    best = {m: cost[m] for m in range(16) if cost[m] < INF}
    grew = True
    while grew:
        grew = False
        for u, c in list(best.items()):
            for m in range(16):
                if cost[m] < INF:
                    v, cc = u | m, c + cost[m]
                    if cc < best.get(v, INF): best[v] = cc; grew = True
    for u, c in best.items():
        f = FULL & ~u
        if c + 1 < cost[f]: cost[f] = c + 1; changed = True

# ---------- 驗算幾條手寫構造
assert N(P) == mask_of["FWFW"]                    # ~p
assert N(N(P), N(Q)) == mask_of["WFFF"]           # p∧q
assert N(N(P, Q)) == mask_of["WWWF"]              # p∨q
assert N(N(N(P), Q)) == mask_of["WWFW"]           # p→q ＝ ~p∨q
assert N(N(P, N(P))) == FULL and N(P, N(P)) == 0  # 重言式、矛盾式
assert N(N(P)) == P                               # 5.254：運算可以消失
assert all(cost[m] < INF for m in range(16)) and len(first) == 16

# ---------- 數的定義（6.02）：Ω^0'x = x、Ω^(ν+1)'x = Ω'Ω^ν'x；數就是運算的指數（6.021）
def omega_power(n, op, x):
    for _ in range(n): x = op(x)
    return x
assert omega_power(2, lambda f: N(f), P) == P and omega_power(3, lambda f: N(f), P) == N(P)

m_neg, m_and, m_or, m_imp = mask_of["FWFW"], mask_of["WFFF"], mask_of["WWWF"], mask_of["WWFW"]
print("Q1 ~p   最少 N 次數（可重用）=", first[m_neg], "；式子中 N 個數 =", cost[m_neg], "  N(p)")
print("Q2 p∧q  最少 N 次數（可重用）=", first[m_and], "；式子中 N 個數 =", cost[m_and], "  N(N(p),N(q))")
print("Q3 p∨q  最少 N 次數（可重用）=", first[m_or], "；式子中 N 個數 =", cost[m_or], "  N(N(p,q))")
print("Q4 從 {p,q} 逐層生成全部 16 個真值函數所需層數 =", LAYERS)
print("--- 每層新增：", [len(x) for x in per_layer], "（第 0 層為 p、q）")
for i, x in enumerate(per_layer):
    print(f"    第 {i} 層：", "、".join(NAMES[m] for m in x))
print("--- 集齊全部 16 個所需最少 N 次數（可重用、一次加一個）=", all16)
print("--- 5.101 順序逐一：真值欄 名稱 層 最少N次數(可重用) 式子N個數")
for i, c in enumerate(ORDER, 1):
    m = mask_of[c]
    print(f"    {i:2d} ({c})(p,q) {NAMES[m]:12s} 層 {layer[m]}  最少 {first[m]}  式子 {cost[m]}")
print("--- p→q 最少 N 次數 =", first[m_imp], "；式子 N 個數 =", cost[m_imp], "  N(N(N(p),q))")
print("--- 6.02：Ω'Ω'Ω'x 寫成 Ω^(0+1+1+1)'x，指數 = 3；N 作用兩次回到原命題：N(N(p)) = p")
