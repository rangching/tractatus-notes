"""EP06 練習題答案：可說的與可顯示的（4.014 唱片、樂譜、聲波）。
也重現 sims/u06.html 的旋律產生器與「從波形讀回音高」的計算，確認投影規則可以來回翻譯。
執行：python3 calc_u06.py
"""
import math

A4 = 440.0
def freq(midi): return A4 * 2 ** ((midi - 69) / 12)
def midi_of(f): return round(69 + 12 * math.log2(f / A4))

# ---------- Q1：平均律下 E5（MIDI 76）的頻率
Q1 = freq(76)
# ---------- Q2：33⅓ rpm 的唱片連續播放 18 分鐘，唱針沿溝紋走了幾圈
Q2 = (100 / 3) * 18
# ---------- Q3：整段旋律升高 3 個半音，每個音的頻率要乘上多少
Q3 = 2 ** (3 / 12)
# ---------- Q4：下列六句中，有幾句講的是只能「顯示」、不能「說」的東西（說了就成胡說）
SENT = [("台北今天下雨。", "說"),
        ("「fa」和「ga」談的是同一個對象 a。", "顯示"),         # 4.1211
        ("這張樂譜和這張唱片有相同的邏輯構造。", "顯示"),       # 4.014 內在關係
        ("一大氣壓下，水在 100°C 沸騰。", "說"),
        ("p 和「非 p」互相矛盾。", "顯示"),                    # 4.1211
        ("這種藍比那種藍淺（指著兩張色票）。", "顯示")]          # 4.123 內在關係
Q4 = sum(1 for _, k in SENT if k == "顯示")

# ---------- 與 sim 相同的旋律產生器（線性同餘亂數，C 大調音階上的隨機漫步）
SCALE = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76]
def melody(seed, n=8):
    s = seed; deg = 2; out = []                      # 從 E4 出發，最後回到主音 C4
    for i in range(n):
        if i == n - 1: deg = 0
        elif i > 0:
            s = (s * 1103515245 + 12345) % 2 ** 31
            deg += [-2, -1, 1, 2][(s >> 16) % 4]
            if deg < 0: deg = -deg                    # 碰到邊界就反彈
            if deg > 9: deg = 18 - deg
        out.append(SCALE[deg])
    return out

# 投影規則 1：音高 → 波形（為了畫得出來，顯示頻率 = 真實頻率 / 25）；每音 0.4 s，音與音之間 0.05 s 靜音
SR, DUR, GAP, SCALE_DOWN = 1000, 0.4, 0.05, 25
def render(mel):
    sig = []
    for m in mel:
        f = freq(m) / SCALE_DOWN
        for i in range(int(DUR * SR)):
            t = i / SR; env = math.sin(math.pi * t / DUR)
            sig.append(env * math.sin(2 * math.pi * f * t))
        sig += [0.0] * int(GAP * SR)
    return sig
# 投影規則 1 的反方向：由波形讀回音高（找出有聲的段落，數過零點）
def decode(sig, rate_factor=1.0):
    segs, i, n = [], 0, len(sig)
    while i < n:
        if abs(sig[i]) > 1e-9:
            j = i
            while j < n and not (all(abs(x) < 1e-9 for x in sig[j:j + 10])): j += 1
            segs.append((i, j)); i = j
        else: i += 1
    out = []
    for a, b in segs:
        # 用線性內插找出每個過零點的時刻，相鄰過零點相隔半個週期
        zs = [(k - 1 + sig[k - 1] / (sig[k - 1] - sig[k])) / SR
              for k in range(a + 1, b) if (sig[k - 1] < 0) != (sig[k] < 0)]
        f = (len(zs) - 1) / 2 / (zs[-1] - zs[0]) * SCALE_DOWN * rate_factor
        out.append(midi_of(f))
    return out

mel = melody(3)
back = decode(render(mel))
print("Q1 E5 的頻率 440×2^(7/12)               =", round(Q1, 2), "Hz")
print("Q2 33⅓ rpm × 18 分鐘                     =", round(Q2, 1), "圈")
print("Q3 升 3 個半音的頻率倍數 2^(3/12)          =", round(Q3, 4))
print("Q4 六句中只能顯示的句數                    =", Q4)
print("--- 參考：sim 預設旋律（種子 3）MIDI     =", mel)
print("--- 參考：由波形數過零點讀回               =", back, "一致" if back == mel else "不一致")
print("--- 參考：用錯規則（45 rpm 去讀 33⅓ rpm）讀回 =", decode(render(mel), 45 / (100 / 3)))
print("--- 參考：音程序列（相鄰半音差）            =", [b - a for a, b in zip(mel, mel[1:])])
