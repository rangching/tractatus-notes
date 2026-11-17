"""source/tlp_props.json → learning_site/data/tlp_props.js（window.TLP_PROPS），網站命題瀏覽器、引文卡、首頁命題樹共用。"""
import json, re
from pathlib import Path
here = Path(__file__).resolve().parent
src = here.parent.parent / "source" / "tlp_props.json"
P = json.loads(src.read_text(encoding="utf-8"))
def tidy(s):  # 圖片佔位改成文字
    return re.sub(r"\[img:[^\]]+\]", "□", s or "")
keep = [{"n": p["num"], "p": p["parent"], "d": p["depth"], "m": int(p["main"]), "e": p["ep"],
         "zh": tidy(p["zh"]), "de": tidy(p["de"]), "en": tidy(p["en"])} for p in P]
out = here.parent / "data" / "tlp_props.js"
out.write_text("// 由 _units/build_props_js.py 產生，請勿手改。來源：source/tlp_props.json\n"
               "// 德文：1921 原文（公有領域）；英文：C. K. Ogden 1922 英譯（公有領域）；中文：本系列自譯。\n"
               "window.TLP_PROPS = " + json.dumps(keep, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print(out, len(keep), "props;", sum(bool(k["zh"]) for k in keep), "with zh")
