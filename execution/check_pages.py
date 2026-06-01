import pathlib

ROOT = pathlib.Path(__file__).parent.parent.resolve()
pages = [
    "pages/login.html",
    "pages/register.html",
    "pages/pricing.html",
    "pages/index.html",
]

all_ok = True
for p in pages:
    f = ROOT / p
    c = f.read_text(encoding="utf-8", errors="ignore")
    lines      = c.count("\n")
    kb         = len(c) // 1024
    div_open   = c.count("<div")
    div_close  = c.count("</div>")
    div_ok     = div_open == div_close
    responsive = "@media" in c or "max-width" in c
    placeholder = "TODO" in c and lines < 10
    ok = div_ok and not placeholder
    if not ok:
        all_ok = False
    tag = "[OK]" if ok else "[X] "
    div_tag = "OK" if div_ok else "MISMATCH"
    print(tag, p, ":", lines, "lines ~" + str(kb) + "KB",
          "| div", str(div_open) + "/" + str(div_close), div_tag,
          "| responsive=" + str(responsive))

print()
print("All pages OK!" if all_ok else "Some pages FAILED!")
