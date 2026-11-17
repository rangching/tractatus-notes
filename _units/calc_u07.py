"""EP07 練習題答案：真值表——命題是一張可能性地圖（4.2–4.53）。
維根斯坦的記法：W＝wahr（真）、F＝falsch（假）（4.31）。
真值可能性的排列順序沿用 5.101 的圖式：第 i 列（0 起算）中，第 j 個變項在 i 的第 j 個位元為 1 時取 F。
  兩個變項時依序為 (p,q) = (W,W)、(F,W)、(W,F)、(F,F)，與 5.101 一致。
4.27：n 個事態的存在與不存在共有 K_n = Σ_ν C(n,ν) = 2^n 種組合。
4.42：一個命題與這 K_n 種真值可能性的符合與不符合，共有 Σ_κ C(K_n,κ) = 2^(K_n) 種。
執行：python3 calc_u07.py
"""
from itertools import product
from math import comb
import re

# ---------- 小型命題式解析器（與 sims/u07.html 相同的優先序：~ > ∧ > ∨ > → > ↔，→ 右結合）
def tokenize(s):
    s = s.replace("<->", "↔").replace("->", "→").replace("≡", "↔").replace("⊃", "→")
    s = s.replace("¬", "~").replace("&", "∧").replace(".", "∧").replace("|", "∨").replace("v", "∨")
    return [c for c in s if not c.isspace()]

def parse(s):
    t = tokenize(s); i = 0
    def peek(): return t[i] if i < len(t) else None
    def eat(c):
        nonlocal i
        assert peek() == c, f"預期 {c}"; i += 1
    def iff():
        a = imp()
        while peek() == "↔": eat("↔"); b = imp(); a = ("↔", a, b)
        return a
    def imp():
        a = orr()
        if peek() == "→": eat("→"); return ("→", a, imp())
        return a
    def orr():
        a = andd()
        while peek() == "∨": eat("∨"); a = ("∨", a, andd())
        return a
    def andd():
        a = neg()
        while peek() == "∧": eat("∧"); a = ("∧", a, neg())
        return a
    def neg():
        nonlocal i
        if peek() == "~": eat("~"); return ("~", neg())
        if peek() == "(": eat("("); a = iff(); eat(")"); return a
        c = peek(); assert c in "pqrs", f"不認得 {c}"; i += 1; return c
    a = iff(); assert i == len(t); return a

def ev(a, env):
    if isinstance(a, str): return env[a]
    op = a[0]
    if op == "~": return not ev(a[1], env)
    x, y = ev(a[1], env), ev(a[2], env)
    return {"∧": x and y, "∨": x or y, "→": (not x) or y, "↔": x == y}[op]

def table(s, vars_=None):
    a = parse(s)
    vs = vars_ or sorted(set(re.findall(r"[pqrs]", s)))
    n = len(vs); col = []
    for i in range(2 ** n):
        env = {v: not (i >> j & 1) for j, v in enumerate(vs)}
        col.append(ev(a, env))
    return vs, col

def kind(col):
    return "重言式" if all(col) else "矛盾式" if not any(col) else "偶然命題"

def code(col):
    """編號：把真值欄由上往下讀成二進位數（W=1），範圍 0 … 2^(2^n)-1。"""
    return sum(1 << (len(col) - 1 - i) for i, v in enumerate(col) if v)

# 5.101 的十六個真值函數（依原書順序）
W101 = ["WWWW", "FWWW", "WFWW", "WWFW", "WWWF", "FFWW", "FWFW", "FWWF",
        "WFFW", "WFWF", "WWFF", "FFFW", "FFWF", "FWFF", "WFFF", "FFFF"]
def wstr(col): return "".join("W" if v else "F" for v in col)

# ---------- 4.27 / 4.42 的公式檢查
for n in range(1, 5):
    Kn = sum(comb(n, v) for v in range(n + 1))
    assert Kn == 2 ** n
    assert sum(comb(Kn, k) for k in range(Kn + 1)) == 2 ** Kn

# ---------- 二元真值函數的完整列舉
cols2 = [tuple(c) for c in product([True, False], repeat=4)]
assert len(set(cols2)) == 16
assert sorted(W101) == sorted(wstr(c) for c in cols2)
taut2 = sum(all(c) for c in cols2); contra2 = sum(not any(c) for c in cols2)

# ---------- 練習題
q1 = 2 ** 3
q2 = 2 ** (2 ** 3)
_, c3 = table("p→(q∨r)")
q3 = sum(c3)
q4 = 16 - taut2 - contra2

print("Q1 3 個基本命題的真值可能性數 K_3 = 2^3          =", q1)
print("Q2 3 個基本命題可組出的真值函數數 2^(K_3) = 2^8   =", q2)
print("Q3 p→(q∨r) 在 8 列真值可能性中為真的列數          =", q3, " → 真值欄", wstr(c3), kind(c3))
print("Q4 16 個二元真值函數中「偶然」（非重言、非矛盾）的數目 =", q4,
      f"（重言式 {taut2} 個、矛盾式 {contra2} 個）")
print("--- 參考：n=1..4 的真值可能性與真值函數數：",
      [(n, 2 ** n, 2 ** (2 ** n)) for n in range(1, 5)])
print("--- 範例判定（給 sim 與影片核對）")
for f in ["p∨~p", "p∧~p", "p→q", "(p→q)∧p→q", "p↔q", "~(p∧q)↔(~p∨~q)", "(p→q)∧(q→r)→(p→r)", "p.q", "p v q"]:
    vs, c = table(f, ["p", "q"] if set(re.findall(r"[pqrs]", f)) <= {"p", "q"} else None)
    extra = ""
    if len(vs) == 2:
        extra = f"  5.101 第 {W101.index(wstr(c)) + 1} 號"
    print(f"   {f:24s} 變項 {''.join(vs):4s} ({wstr(c)})({','.join(vs)})  編號 {code(c)}/{2 ** (2 ** len(vs))}  {kind(c)}{extra}")
