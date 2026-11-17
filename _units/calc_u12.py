"""EP12 練習題答案：價值、神祕與丟掉梯子（6.4–7）。全部用 source/tlp_props.json 實算。
欄位：num 編號、parent 父編號、depth 深度（主命題為 0）、main 所屬主命題、ep 所屬集數、de 德文原文。
另外印出 sims/u12.html「梯子」每一級的光點數（與 sim 相同的分配規則）：
  第 1 級＝主命題 1–6（EP01 的全書地圖）；第 2–12 級＝ep 欄為 u02…u12 的其餘命題；第 7 命題獨自留在頂端。
執行：python3 calc_u12.py
"""
import json
from collections import Counter
from pathlib import Path

src = Path(__file__).resolve().parents[2] / "source" / "tlp_props.json"
P = json.loads(src.read_text(encoding="utf-8"))
by = {p["num"]: p for p in P}

# ---------- Q1：6.4 到 7 共有幾條命題
last = [p["num"] for p in P if p["ep"] == "u12"]
assert last[0] == "6.4" and last[-1] == "7"
q1 = len(last)


# ---------- Q2：這最後一段的德文字元數占全書的百分比（去掉表示強調的 *）
def clen(s):
    return len(s.replace("*", ""))


tot_de = sum(clen(p["de"]) for p in P)
last_de = sum(clen(by[n]["de"]) for n in last)
q2 = round(last_de / tot_de * 100, 2)
share_n = round(q1 / len(P) * 100, 2)

# ---------- Q3：從 6.4311 沿父節點往上，要幾步才到主命題 6
steps, n, path = 0, "6.4311", ["6.4311"]
while by[n]["parent"] is not None:
    n = by[n]["parent"]; steps += 1; path.append(n)
q3 = steps

# ---------- Q4：七個主命題中，唯一沒有任何註解（子命題）的是第幾號
child = Counter(p["parent"] for p in P if p["parent"])
mains = [p["num"] for p in P if p["depth"] == 0]
no_child = [m for m in mains if child[m] == 0]
assert len(no_child) == 1
q4 = int(no_child[0])

# ---------- 梯子每一級的光點數
rung = Counter()
for p in P:
    if p["num"] == "7":
        continue
    if p["depth"] == 0:
        rung["u01"] += 1
    else:
        rung[p["ep"]] += 1

print("Q1 6.4 到 7 的命題數 =", q1, f"（占全書 {len(P)} 條的 {share_n}%）")
print("Q2 這 22 條的德文字元數占全書德文的百分比 =", q2, "%", f"（{last_de} / {tot_de} 字元）")
print("Q3 6.4311 往上到主命題的步數 =", q3, "：", " → ".join(path))
print("Q4 沒有任何子命題的主命題 =", q4, "；各主命題的直接子命題數 =", {m: child[m] for m in mains})
print("--- 參考：梯子各級光點數 =", [(f"EP{int(k[1:]):02d}", rung[k]) for k in sorted(rung)], "＋頂端的 7；合計",
      sum(rung.values()) + 1)
