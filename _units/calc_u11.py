"""EP11 練習題答案：邏輯、數學與科學——牛頓力學是一張網（6.1–6.372）。
6.341 的思想實驗：白色平面上有不規則黑斑，用一張網覆蓋，逐格說「黑」或「白」。
本檔與 sims/u11.html「描述之網」使用同一個演算法（CORE 區塊逐行對應）：
  斑點圖：240×240 像素，mulberry32(6341) 產生 7 團黑斑，每團由 3–5 個旋轉橢圓聯集而成（只用加減乘除與開根號，兩邊結果逐位元相同）。
  網格：方格、正三角形、正六角形三種，以「每格面積 A（像素²）」對齊，公平比較。
    滑桿的「等效邊長」s 取整數 2–40，A = s²（方格邊長就是 s；三角與六角取同面積）。
  每個像素中心歸入一格；一格裡黑像素過半（含剛好一半）就整格報「黑」，否則報「白」。
  描述長度＝網格覆蓋圖面所用的格數（每格 1 位元：黑或白）。
  覆蓋所需格數＝含有任何黑像素的格數（要把黑斑完全蓋住，最少要塗黑的格數）。
  誤差＝被整格判定弄錯顏色的像素數 ÷ 全部像素數。
Q4 用真值表檢查 5 個式子是否為重言式（6.1、6.1201）。
執行：python3 calc_u11.py
"""
import math
from itertools import product

W = H = 240
SQ3 = math.sqrt(3)


def mulberry32(seed):
    st = [seed & 0xFFFFFFFF]

    def imul(x, y):
        return (x * y) & 0xFFFFFFFF

    def rnd():
        st[0] = (st[0] + 0x6D2B79F5) & 0xFFFFFFFF
        a = st[0]
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296

    return rnd


def make_image(seed=6341):
    rnd = mulberry32(seed)
    ells = []
    for _ in range(7):
        cx, cy = 30 + 180 * rnd(), 30 + 180 * rnd()
        m = 3 + math.floor(rnd() * 3)
        for _ in range(m):
            ex, ey = cx + (rnd() - 0.5) * 40, cy + (rnd() - 0.5) * 40
            rx, ry = 8 + 18 * rnd(), 6 + 14 * rnd()
            u, v = rnd() * 2 - 1, rnd() * 2 - 1
            n = math.sqrt(u * u + v * v)
            if n < 1e-6:
                u, v, n = 1.0, 0.0, 1.0
            ells.append((ex, ey, rx, ry, u / n, v / n))
    img = bytearray(W * H)
    for j in range(H):
        y = j + 0.5
        for i in range(W):
            x = i + 0.5
            for (ex, ey, rx, ry, c, s) in ells:
                dx, dy = x - ex, y - ey
                a = (dx * c + dy * s) / rx
                b = (-dx * s + dy * c) / ry
                if a * a + b * b <= 1:
                    img[j * W + i] = 1
                    break
    return img


def key(a, b):
    return (a + 2000) * 8192 + (b + 2000)


def cell_of(shape, A):
    """回傳把像素中心 (x,y) 對應到格子編號的函式。A 為每格面積。"""
    if shape == "square":
        s = math.sqrt(A)
        return lambda x, y: key(math.floor(x / s), math.floor(y / s))
    if shape == "tri":
        a = math.sqrt(4 * A / SQ3)          # 正三角形邊長
        th = a * SQ3 / 2                     # 列高

        def f(x, y):
            r = math.floor(y / th)
            X = x - (a / 2 if r % 2 else 0)
            fx = X / a
            k = math.floor(fx)
            fr = fx - k
            yy = (y - r * th) / th
            if fr < 0.5 - yy / 2:
                return key(r, 2 * (k - 1) + 1)
            if fr > 0.5 + yy / 2:
                return key(r, 2 * k + 1)
            return key(r, 2 * k)
        return f
    # 正六角形（尖頂朝上），邊長 h
    h = math.sqrt(2 * A / (3 * SQ3))

    def g(x, y):
        q = (SQ3 / 3 * x - y / 3) / h
        r = (2 / 3 * y) / h
        cx, cz = q, r
        cy = -cx - cz
        rx, ry, rz = math.floor(cx + 0.5), math.floor(cy + 0.5), math.floor(cz + 0.5)
        dx, dy, dz = abs(rx - cx), abs(ry - cy), abs(rz - cz)
        if dx > dy and dx > dz:
            rx = -ry - rz
        elif dy > dz:
            ry = -rx - rz
        else:
            rz = -rx - ry
        return key(rx, rz)
    return g


def describe(img, shape, A):
    f = cell_of(shape, A)
    tot, blk = {}, {}
    for j in range(H):
        y = j + 0.5
        for i in range(W):
            k = f(i + 0.5, y)
            tot[k] = tot.get(k, 0) + 1
            if img[j * W + i]:
                blk[k] = blk.get(k, 0) + 1
    err = 0
    nblack = 0
    for k, t in tot.items():
        b = blk.get(k, 0)
        if 2 * b >= t:
            nblack += 1
            err += t - b
        else:
            err += b
    return {"cells": len(tot), "cover": len(blk), "black": nblack, "err": err / (W * H)}


def area_list():
    """與 sim 的滑桿一致：等效邊長 s = 40, 39, …, 2，每格面積 A = s²。"""
    return [s * s for s in range(40, 1, -1)]


def coarsest(img, shape, target):
    """由粗到細掃描面積清單，回傳第一個誤差 ≤ target 的網格（最粗、描述最短）。"""
    for A in area_list():
        d = describe(img, shape, A)
        if d["err"] <= target:
            return A, d
    return None, None


img = make_image()
black_px = sum(img)

# ---------- Q1：方格邊長從 16 減半到 8，格數變幾倍
d16 = describe(img, "square", 256)
d8 = describe(img, "square", 64)
q1 = d8["cells"] / d16["cells"]

# ---------- Q2：方格邊長 12（A=144）時的誤差（百分比）
d12 = describe(img, "square", 144)
q2 = round(d12["err"] * 100, 2)

# ---------- Q3：誤差 ≤ 2% 時，方格網最少要幾格（掃描清單中最粗的那一個）
TARGET = 0.02
res = {s: coarsest(img, s, TARGET) for s in ("square", "tri", "hex")}
q3 = res["square"][1]["cells"]


# ---------- Q4：哪些是重言式
def imp(a, b):
    return (not a) or b


FORMS = [
    ("p ∨ ~p", lambda p, q: p or not p),
    ("(p ⊃ q) . p : ⊃ : q", lambda p, q: imp(imp(p, q) and p, q)),
    ("p ⊃ q", lambda p, q: imp(p, q)),
    ("~(p . ~p)", lambda p, q: not (p and not p)),
    ("(p ⊃ q) ⊃ (q ⊃ p)", lambda p, q: imp(imp(p, q), imp(q, p))),
]
taut = [name for name, f in FORMS if all(f(p, q) for p, q in product([True, False], repeat=2))]
q4 = len(taut)

name = {"square": "方格", "tri": "三角", "hex": "六角"}
print("斑點圖 240×240，黑像素", black_px, f"（{black_px / (W * H) * 100:.2f}%）")
print("Q1 方格邊長 16 → 8：格數", d16["cells"], "→", d8["cells"], "，變成", q1, "倍")
print("Q2 方格邊長 12（每格 144 px²）的誤差 =", q2, "%",
      f"（總格數 {d12['cells']}、覆蓋黑斑需 {d12['cover']} 格、判黑 {d12['black']} 格）")
print("Q3 誤差 ≤ 2% 的最粗方格網：格數 =", q3,
      f"（每格 {res['square'][0]} px²，邊長 {math.isqrt(res['square'][0])}，誤差 {res['square'][1]['err'] * 100:.2f}%）")
print("Q4 五個式子中的重言式個數 =", q4, "：", "、".join(taut))
print("--- 參考：誤差 ≤ 2% 的最粗網格（三種形狀）")
for s in ("square", "tri", "hex"):
    A, d = res[s]
    print(f"    {name[s]}網：等效邊長 {math.isqrt(A):2d}（每格 {A:4d} px²），描述長度 {d['cells']:5d} 位元，覆蓋需 {d['cover']:4d} 格，誤差 {d['err'] * 100:.2f}%")
print("--- 參考：同樣每格面積下三種網格的誤差（%）")
for A in (400, 256, 144, 64):
    row = [describe(img, s, A) for s in ("square", "tri", "hex")]
    print(f"    A={A:4d}：" + "　".join(f"{name[s]} {r['err'] * 100:5.2f}%（{r['cells']} 格）" for s, r in zip(("square", "tri", "hex"), row)))
# 6.341「較粗的三角網可能比較細的方格網更精確」：找一組實例
found = None
for At in area_list():
    dt = describe(img, "tri", At)
    for As in area_list():
        if As >= At:
            continue
        ds = describe(img, "square", As)
        if dt["err"] < ds["err"]:
            found = (At, dt, As, ds)
            break
    if found:
        break
if found:
    At, dt, As, ds = found
    print(f"--- 參考（6.341）：三角網等效邊長 {math.isqrt(At)}（較粗）誤差 {dt['err'] * 100:.2f}% ＜ 方格網邊長 {math.isqrt(As)}（較細）誤差 {ds['err'] * 100:.2f}%")
print("--- 參考：放寬誤差目標後，哪一張網最省（描述長度最短）")
for tgt in (0.05, 0.055):
    rr = {s: coarsest(img, s, tgt) for s in ("square", "tri", "hex")}
    win = min(rr, key=lambda s: rr[s][1]["cells"])
    print(f"    目標 ≤ {tgt * 100:.1f}%：" + "　".join(
        f"{name[s]} 邊長 {math.isqrt(rr[s][0])}／{rr[s][1]['cells']} 格" for s in ("square", "tri", "hex")), "→ 最省：", name[win] + "網")
