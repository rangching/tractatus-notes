"""EP10 練習題答案：我的語言的界限，就是我的世界的界限（5.6–5.641）。
Q1 用 source/tlp_props.json 的 parent 欄位實算 5.6 這棵子樹的大小。
Q2 八個句子的分類（說 / 嘗試說只能顯示的），逐句標註理由後計數。
Q3、Q4 用與 sims/u10.html「視野模型」完全相同的世界與光線投射演算法（同一個 mulberry32 種子）實算。
  世界：以眼睛為原點的 20×20 方形庭院，16 個圓形物件（樹、石頭、燈柱），一面平面鏡。
  視野：視線方向 dir、視角 fov；每 0.5° 投一條光線，記下第一個碰到的東西；碰到鏡子就反射一次。
  眼睛是所有光線的起點，直射光線不會「碰到」它；只有被鏡子反射回來的光線才可能碰到眼睛的外殼（身體）。
執行：python3 calc_u10.py
"""
import json
import math
from pathlib import Path

src = Path(__file__).resolve().parents[2] / "source" / "tlp_props.json"
P = json.loads(src.read_text(encoding="utf-8"))
by = {p["num"]: p for p in P}


# ---------- Q1：5.6 子樹（含 5.6 本身）
def ancestors(num):
    while num is not None:
        yield num
        num = by[num]["parent"]


sub56 = [p["num"] for p in P if "5.6" in ancestors(p["num"])]
q1 = len(sub56)
max_depth = max(by[n]["depth"] for n in sub56)

# ---------- Q2：哪些句子在嘗試「說」只能「顯示」的東西
SENT = [
    ("世界是我的世界。", True, "5.62：唯我論的意思正確，但只能顯示，不能說"),
    ("這杯咖啡是熱的。", False, "普通的經驗命題，可以和事實比對真假"),
    ("命題和實在共有同一個邏輯形式。", True, "4.12–4.121：邏輯形式只能映現，不能被命題呈現"),
    ("我的視野左邊有一棵樹。", False, "描述視野裡的一件事，可以是真或假"),
    ("邏輯上，世界裡就是沒有獨角獸。", True, "5.61：不能在邏輯中說「世界有這個、沒有那個」"),
    ("那個在思考的我，位在大腦的前額葉。", True, "5.631–5.641：形上主體不是世界中的一部分，無法被定位"),
    ("明天可能會下雨。", False, "有意義的命題，等明天就能比對"),
    ("我的眼睛是深棕色的。", False, "眼睛當作身體的一部分，是世界中的物，可以描述（5.631）"),
]
q2 = sum(1 for _, s, _ in SENT if s)


# ---------- 世界與光線投射（與 sims/u10.html 的 CORE 區塊逐行對應）
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


HALF = 10.0          # 庭院半寬
EYE_R = 0.3          # 眼睛（身體）外殼半徑
MA, MB = (3.5, -7.5), (8.0, -3.0)   # 鏡子兩端
MF = (5.5, -5.5)                     # 眼睛在鏡面上的垂足（鏡子所在直線 y = x - 11）
EPS = 1e-9


def seg_dist(px, py, ax, ay, bx, by_):
    ex, ey = bx - ax, by_ - ay
    u = ((px - ax) * ex + (py - ay) * ey) / (ex * ex + ey * ey)
    u = max(0.0, min(1.0, u))
    dx, dy = px - (ax + u * ex), py - (ay + u * ey)
    return math.sqrt(dx * dx + dy * dy)


def make_world(seed=5633, n=16):
    rnd = mulberry32(seed)
    objs, tries = [], 0
    while len(objs) < n and tries < 5000:
        tries += 1
        x = -9 + 18 * rnd()
        y = -9 + 18 * rnd()
        r = 0.35 + 0.5 * rnd()
        k = math.floor(rnd() * 3)
        if math.sqrt(x * x + y * y) < 2.2:
            continue
        if any(math.sqrt((x - o[0]) ** 2 + (y - o[1]) ** 2) < r + o[2] + 0.4 for o in objs):
            continue
        if seg_dist(x, y, MA[0], MA[1], MB[0], MB[1]) < r + 0.4:
            continue
        if seg_dist(x, y, 0.0, 0.0, MF[0], MF[1]) < r + 1.0:   # 讓眼睛到鏡子中點的通道保持空曠
            continue
        objs.append((x, y, r, k))
    return objs


def hit_circle(ox, oy, dx, dy, cx, cy, r):
    px, py = ox - cx, oy - cy
    b = px * dx + py * dy
    c = px * px + py * py - r * r
    disc = b * b - c
    if disc < 0:
        return None
    s = math.sqrt(disc)
    t = -b - s
    if t > EPS:
        return t
    t = -b + s
    return t if t > EPS else None


def hit_mirror(ox, oy, dx, dy):
    ex, ey = MB[0] - MA[0], MB[1] - MA[1]
    den = dx * ey - dy * ex
    if abs(den) < 1e-12:
        return None
    wx, wy = MA[0] - ox, MA[1] - oy
    t = (wx * ey - wy * ex) / den
    u = (wx * dy - wy * dx) / den
    return t if (t > EPS and 0 <= u <= 1) else None


def hit_wall(ox, oy, dx, dy):
    tx = (HALF - ox) / dx if dx > 0 else (-HALF - ox) / dx if dx < 0 else math.inf
    ty = (HALF - oy) / dy if dy > 0 else (-HALF - oy) / dy if dy < 0 else math.inf
    return min(tx, ty)


def cast(objs, ox, oy, dx, dy, mirror_on, bounced=False):
    """回傳 (種類, 編號, 總距離, 是否經過鏡子)。種類：obj / wall / eye。"""
    best_t, best = hit_wall(ox, oy, dx, dy), ("wall", -1)
    for i, (cx, cy, r, _) in enumerate(objs):
        t = hit_circle(ox, oy, dx, dy, cx, cy, r)
        if t is not None and t < best_t:
            best_t, best = t, ("obj", i)
    if bounced:                       # 只有反射回來的光線才可能碰到眼睛的外殼
        t = hit_circle(ox, oy, dx, dy, 0.0, 0.0, EYE_R)
        if t is not None and t < best_t:
            best_t, best = t, ("eye", -1)
    if mirror_on and not bounced:
        t = hit_mirror(ox, oy, dx, dy)
        if t is not None and t < best_t:
            px, py = ox + t * dx, oy + t * dy
            ex, ey = MB[0] - MA[0], MB[1] - MA[1]
            L = math.sqrt(ex * ex + ey * ey)
            nx, ny = -ey / L, ex / L
            dn = dx * nx + dy * ny
            rx, ry = dx - 2 * dn * nx, dy - 2 * dn * ny
            k, i, t2, _ = cast(objs, px, py, rx, ry, mirror_on, True)
            return (k, i, t + t2, True)
    return (best[0], best[1], best_t, False)


def fan(objs, dir_deg, fov_deg, mirror_on, step=0.5):
    K = int(fov_deg / step)
    out = []
    for k in range(K + 1):
        th = (dir_deg - fov_deg / 2 + k * step) * math.pi / 180
        out.append(cast(objs, 0.0, 0.0, math.cos(th), math.sin(th), mirror_on))
    return out


world = make_world()
FOV = 90
vis_counts = []
eye_dirs = []
for d in range(360):
    f0 = fan(world, d, FOV, False)
    vis_counts.append(len({h[1] for h in f0 if h[0] == "obj"}))
    f1 = fan(world, d, FOV, True)
    if any(h[0] == "eye" for h in f1):
        eye_dirs.append(d)
q3 = max(vis_counts)
q3_dir = vis_counts.index(q3)
q4 = len(eye_dirs)

print("世界：", len(world), "個物件；前三個 =", [tuple(round(v, 3) for v in o) for o in world[:3]])
print("Q1 5.6 子樹（含 5.6）的命題數                         =", q1, "；最深層級 =", max_depth, "；", " ".join(sub56))
print("Q2 八句中「嘗試說只能顯示的東西」的句數                =", q2)
for s, flag, why in SENT:
    print("    ", "嘗試說" if flag else "可說　", s, "—", why)
print("Q3 視角 90°、不放鏡子，視線轉一圈（0°…359°）最多同時看見 =", q3, "個物件（第一次出現在方向", q3_dir, "°）")
print("Q4 放上鏡子、視角 90°，360 個方向中「鏡中的眼睛」出現的方向數 =", q4,
      "（視線方向在", sorted(((d + 180) % 360) - 180 for d in eye_dirs)[0], "°到",
      sorted(((d + 180) % 360) - 180 for d in eye_dirs)[-1], "°之間；鏡中眼睛位在 -45° 方向）")
print("--- 參考：每個方向可見物件數 =", vis_counts[::30], "（每 30° 取一次）")
