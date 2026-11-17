"""EP08 練習題答案：推論與機率（5.1–5.156）。
定義（照原文，方向已核對德文與 Ogden 英譯）：
  5.101 真值根據（Wahrheitsgründe）＝使命題為真的那些真值可能性。
  5.12  若 q 的所有真值根據都是 p 的真值根據，則 p 從 q 推出：TG(q) ⊆ TG(p)。
  5.15  德文：Wr＝命題「r」的真值根據數；Wrs＝命題「s」的真值根據中「同時也是 r 的真值根據」者之數；
        「Wrs : Wr」稱為命題「r」給予（gibt）命題「s」的機率量度。
        → r 給 s 的機率  P(s ← r) = |TG(r) ∩ TG(s)| / |TG(r)|（相當於今天的條件機率 P(s | r)，各真值可能性等權）。
  5.152 兩個基本命題互相給予 1/2；p 從 q 推出時 q 給 p 的機率為 1。
所以「p∨q 給 p 的機率」：r = p∨q、s = p → 2/3。
執行：python3 calc_u08.py
"""
from fractions import Fraction
from itertools import product
import re, pathlib

# 借用 calc_u07.py 的解析器（只取「# ---------- 4.27」之前的定義，不執行它的列印）
src = pathlib.Path(__file__).with_name("calc_u07.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("# ---------- 4.27")[0], ns)
parse, ev = ns["parse"], ns["ev"]

def tg(f, vs):
    """回傳 f 在變項 vs 上的真值根據集合（每個真值可能性以 tuple 表示）。"""
    a = parse(f); out = set()
    for vals in product([True, False], repeat=len(vs)):
        if ev(a, dict(zip(vs, vals))): out.add(vals)
    return out

def vars_of(*fs): return sorted(set(re.findall(r"[pqrs]", "".join(fs))))

def gives(r, s, extra=()):
    """命題 r 給命題 s 的機率 Wrs : Wr（5.15）。"""
    vs = sorted(set(vars_of(r, s)) | set(extra))
    Tr, Ts = tg(r, vs), tg(s, vs)
    if not Tr: return None  # r 為矛盾式：Wr = 0，比值無定義
    return Fraction(len(Tr & Ts), len(Tr))

def follows(p, q):
    """p 是否從 q 推出（5.12）：TG(q) ⊆ TG(p)。"""
    vs = vars_of(p, q)
    return tg(q, vs) <= tg(p, vs)

# ---------- 練習題
q1 = gives("p∨q", "p")                     # p∨q 給 p
q2 = gives("p", "p∨q")                     # p 給 p∨q（p∨q 從 p 推出 → 1）
cols = list(product([True, False], repeat=4))
pq_row = 0  # (p,q)=(W,W) 那一列：p∧q 唯一的真值根據
q3 = sum(1 for c in cols if c[pq_row])     # 16 個二元真值函數中，從 p∧q 推出的個數
q4 = gives("p∨q∨r", "p")

assert q1 == Fraction(2, 3) and q2 == 1 and follows("p∨q", "p") and not follows("p", "p∨q")
assert gives("q", "p") == Fraction(1, 2)                       # 5.152 兩個基本命題互給 1/2
assert gives("p∨~p", "p") == Fraction(1, 2)                    # 重言式給 p：1/2（5.152 應用）
assert gives("p∧~p", "p") is None                              # 矛盾式：Wr=0
assert gives("p∨q", "p", extra=["r", "s"]) == Fraction(2, 3)   # 多加無關變項，比值不變

print("Q1 p∨q 給 p 的機率 Wrs:Wr（r=p∨q, s=p）           =", q1, "≈", round(float(q1), 4))
print("Q2 p 給 p∨q 的機率（p∨q 從 p 推出）               =", q2)
print("Q3 16 個二元真值函數中，從 p∧q 推出的個數          =", q3)
print("Q4 p∨q∨r 給 p 的機率                              =", q4, "≈", round(float(q4), 4))
print("--- 參考：q 給 p（兩個基本命題）                  =", gives("q", "p"))
print("--- 參考：p→q 給 q                                =", gives("p→q", "q"))
print("--- 參考：重言式 p∨~p 給 p                         =", gives("p∨~p", "p"), "；p 給重言式 =", gives("p", "p∨~p"))
print("--- 參考：矛盾式 p∧~p 給 p                         =", gives("p∧~p", "p"), "（Wr=0，無定義）")
print("--- 參考：p∨q 給 p，在 {p,q,r,s} 上計算            =", gives("p∨q", "p", extra=["r", "s"]), "（加入無關變項不變）")
print("--- 參考：p∨q 從 p 推出？", follows("p∨q", "p"), "；p 從 p∨q 推出？", follows("p", "p∨q"),
      "；q 從 p∧q 推出？", follows("q", "p∧q"))
