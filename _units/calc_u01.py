"""EP01 練習題答案：一本想終結哲學的書——用 source/tlp_props.json 實算全書命題樹的結構。
欄位：num 編號、parent 父編號、depth 深度（主命題為 0）、main 所屬主命題。
執行：python3 calc_u01.py
"""
import json
from collections import Counter
from pathlib import Path

src = Path(__file__).resolve().parents[2] / "source" / "tlp_props.json"
P = json.loads(src.read_text(encoding="utf-8"))
by = {p["num"]: p for p in P}

# 檢查：編號規則與 parent 欄位一致（去掉最後一位數字、再去掉尾端的 0 與小數點，就是父節點）
def parent_by_rule(num):
    if "." not in num:
        return None
    s = num[:-1].rstrip("0").rstrip(".")
    while s not in by:            # 例如 4.0031 → 4.003 不存在 → 4.00 → 4
        s = s[:-1].rstrip("0").rstrip(".")
    return s
mismatch = [p["num"] for p in P if parent_by_rule(p["num"]) != p["parent"]]

total = len(P)
per_main = Counter(p["main"] for p in P)
per_depth = Counter(p["depth"] for p in P)
max_depth = max(per_depth)
deepest = [p["num"] for p in P if p["depth"] == max_depth]
child_cnt = Counter(p["parent"] for p in P if p["parent"])

print("全書命題總數 =", total, "；編號規則與 parent 欄位不符的條數 =", len(mismatch))
print("各主命題（含自身）條數 =", dict(sorted(per_main.items())))
print("各深度條數 =", dict(sorted(per_depth.items())))
print("Q1 主命題 5（含 5 本身）共有幾條命題           =", per_main["5"])
print("Q2 最深的命題深度（主命題為 0）               =", max_depth, "；最深的命題有", len(deepest), "條：", deepest)
print("Q3 2.0121 的父節點                            =", by["2.0121"]["parent"])
print("Q4 七個主命題以外的「註解」命題共幾條         =", total - per_depth[0])
print("--- 參考：直接掛在各主命題下的子命題數       =", {k: child_cnt[k] for k in "1234567"})
print("--- 參考：子命題最多的節點                   =", child_cnt.most_common(3))
print("--- 參考：主命題 4 佔全書比例                 =", round(per_main["4"] / total * 100, 1), "%")
