"""EP02 練習題答案：世界是事實，不是物。
1.21：每一個事態都可以獨立成立或不成立 → n 個事態有 2^n 種「哪些成立」的組合（可能世界）。
本程式用 itertools 實際列舉，不只套公式。執行：python3 calc_u02.py
"""
from itertools import combinations, product

def worlds(n):
    return list(product([0, 1], repeat=n))       # 每個事態：1 成立／0 不成立

# Q1 3 個彼此獨立的事態
q1 = len(worlds(3))
# Q2 5 個事態
q2 = len(worlds(5))
# Q3 4 個對象，「兩兩相連」這種關係（無方向）：可能的事態＝對象兩兩配對
objs = "abcd"
facts = list(combinations(objs, 2))
q3_facts = len(facts)
q3 = len(worlds(q3_facts))
# Q4 3 個事態中「恰好 2 個成立」的世界有幾個（1.12：同時也就決定了哪 1 個不成立）
q4 = sum(1 for w in worlds(3) if sum(w) == 2)
# 參考：1.21 從任一世界只改一個事態、其餘不變，能到達幾個不同的世界（n=5）
w0 = (1, 0, 1, 1, 0)
neighbors = [w for w in worlds(5) if sum(a != b for a, b in zip(w, w0)) == 1]

print("Q1 3 個獨立事態的可能世界數                     =", q1)
print("Q2 5 個獨立事態的可能世界數                     =", q2)
print("Q3 4 個對象兩兩配對的事態數 =", q3_facts, "；可能世界數 =", q3)
print("Q4 3 個事態中恰好 2 個成立的世界數              =", q4)
print("--- 參考：5 個事態時只改一個事態可到達的世界數  =", len(neighbors))
print("--- 參考：4 個對象若關係有方向（a→b 與 b→a 不同），事態數 =", 4 * 3, "；世界數 =", 2 ** 12)
