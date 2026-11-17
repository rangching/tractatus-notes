"""EP05 練習題答案：思想、命題與名稱。
與 sims/u05.html 使用同一套小詞庫與規則：
  句型「A 是 B」。A 必須是名稱（專名或確定描述）。
  B 的種類決定「是」屬於哪一個符號：
     B 是名稱／確定描述 → 等號（a = b）
     B 是概念詞（形容詞、類名）→ 繫詞（F(a)）
     B 是「存在的」     → 存在（∃x(x = a)）
  一個記號若有多種用法，就列舉所有讀法，再用上面的規則篩出合乎邏輯語法的讀法。
執行：python3 calc_u05.py
"""
from itertools import product, permutations

LEX = {  # 記號 → 可能的符號種類
    "白": ["名稱", "概念"], "白的": ["概念"],
    "金星": ["名稱"], "晨星": ["名稱"], "昏星": ["名稱"],
    "維根斯坦": ["名稱"], "羅素": ["名稱"], "哲學家": ["概念"], "英國人": ["概念"],
    "台北101": ["名稱"], "台灣最高的大樓": ["名稱"],   # 確定描述在等式裡當名稱用
    "上帝": ["名稱"], "獨角獸": ["概念"], "存在的": ["存在"],
    "2+2": ["名稱"], "4": ["名稱"],
}
IS = ["繫詞", "等號", "存在"]

def readings(a, b):
    """列舉 A、是、B 三個記號所有可能的符號組合，回傳（全部, 合乎邏輯語法的）。"""
    allr = list(product(LEX[a], IS, LEX[b]))
    def ok(r):
        ra, ris, rb = r
        if rb == "存在":                    # 存在可以談一個名稱 ∃x(x=a)，也可以談一個概念 ∃x F(x)
            return ris == "存在" and ra in ("名稱", "概念")
        if ra != "名稱": return False
        need = {"名稱": "等號", "概念": "繫詞", "存在": "存在"}[rb]
        return ris == need
    return allr, [r for r in allr if ok(r)]

PRESETS = [("白", "白的"), ("金星", "晨星"), ("晨星", "昏星"), ("維根斯坦", "哲學家"),
           ("台北101", "台灣最高的大樓"), ("上帝", "存在的"), ("2+2", "4"),
           ("羅素", "英國人"), ("獨角獸", "存在的")]

use = {}
for a, b in PRESETS:
    allr, good = readings(a, b)
    assert len(good) == 1, (a, b, good)
    use[f"{a}是{b}"] = good[0][1]
count = {k: sum(1 for v in use.values() if v == k) for k in IS}

# ---------- Q1：九句範例中，「是」當等號用的有幾句
Q1 = count["等號"]
# ---------- Q2：「白是白的」三個記號一共有幾種符號讀法（合乎邏輯語法的只剩幾種）
allr, good = readings("白", "白的")
Q2, Q2_ok = len(allr), len(good)
# ---------- Q3：三個基本命題 p、q、r 的邏輯空間有 8 個世界；命題「p 且 q」在其中幾個世界為真
Q3 = sum(1 for p, q, r in product([True, False], repeat=3) if p and q)
# ---------- Q4：三個名稱 a、b、c 與一個二元關係 R，可寫出幾個「xRy」（x ≠ y）的不同命題記號
Q4 = sum(1 for _ in permutations("abc", 2))

for s, u in use.items(): print(f"  {s:<14} → {u}")
print("各用法句數：", count)
print("Q1 九句範例中「是」當等號的句數       =", Q1)
print("Q2 「白是白的」的全部讀法數            =", Q2, "；合乎邏輯語法的 =", Q2_ok, good)
print("Q3 「p 且 q」為真的世界數（共 8 個）   =", Q3)
print("Q4 三個名稱可組出的 xRy（x≠y）命題數 =", Q4)
