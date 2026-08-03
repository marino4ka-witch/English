#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Собирает тренажёр и словарь. Карточка = [en, tr, ru, theme, level].
# Уровневые файлы (a1/a2/b1/b2/frazy/homophones) дедуплицируются между собой по английскому.
import json, re, io

BASE="/home/user/English/словарь/"
# (файл, уровень, участвует_в_дедупе_уровней)
SOURCES=[
  (BASE+"карточки.csv","—",False),
  (BASE+"грамматика.csv","—",False),
  (BASE+"a1.csv","A1",True),
  (BASE+"a1_2.csv","A1",True),
  (BASE+"a2.csv","A2",True),
  (BASE+"b1.csv","B1",True),
  (BASE+"b1_2.csv","B1",True),
  (BASE+"b1_3.csv","B1",True),
  (BASE+"b1_4.csv","B1",True),
  (BASE+"b1_5.csv","B1",True),
  (BASE+"b2.csv","B2",True),
  (BASE+"frazy.csv","Фразы",True),
  (BASE+"homophones.csv","Омофоны",True),
]
HTML="/home/user/English/приложение/тренажёр.html"
MD="/home/user/English/словарь/словарь_по_темам.md"

entries=[]      # [en, tr, ru, theme, level]
groups=[]       # [(тема, [(en,tr,ru),...])]
seen_lvl=set()  # английские, уже занятые уровневыми файлами
RELEVEL={"A1 · МОДАЛЬНЫЕ (30)","A1 · ПРОШЕДШЕЕ ВРЕМЯ (30)","A1 · БУДУЩЕЕ ВРЕМЯ (30)"}  # это A2, не A1

def clean_theme(line):
    t=line.lstrip("#").strip().strip("─ ").strip()
    return t or "Прочее"

for path,level,dedup in SOURCES:
    try:
        f=io.open(path,encoding="utf-8")
    except FileNotFoundError:
        continue
    current="Прочее"; cur=None
    with f:
        for raw in f:
            line=raw.rstrip("\n")
            if not line.strip():continue
            if line.lstrip().startswith("#"):
                current=clean_theme(line); cur=[]; groups.append((current,cur)); continue
            parts=line.split(",")
            if len(parts)<3:continue
            en=parts[0].strip()
            if en.lower()=="english":continue
            tr=parts[1].strip(); ru=",".join(parts[2:]).strip()
            if dedup:
                k=en.lower()
                if k in seen_lvl:continue
                seen_lvl.add(k)
            lv=level; th=current
            if level=="A1" and current in RELEVEL:
                lv="A2"; th=current.replace("A1 ·","A2 ·")
            entries.append([en,tr,ru,th,lv])
            if cur is None:
                cur=[]; groups.append((current,cur))
            cur.append((en,tr,ru))

# 1) залить в тренажёр
arr="[\n"+",\n".join(json.dumps(e,ensure_ascii=False) for e in entries)+"\n]"
html=io.open(HTML,encoding="utf-8").read()
html,n=re.subn(r"const DEFAULT = \[.*?\];","const DEFAULT = "+arr+";",html,count=1,flags=re.S)
assert n==1,"не нашёл блок DEFAULT"
io.open(HTML,"w",encoding="utf-8").write(html)

# 2) словарь по темам
from collections import Counter
lc=Counter(e[4] for e in entries)
out=["# 📚 Словарь и грамматика по темам (A1 → B2)\n",
     "Автосборка из `карточки.csv` + `грамматика.csv` + уровневых файлов.\n",
     f"Всего карточек: **{len(entries)}** (по уровням: "+", ".join(f"{k}={v}" for k,v in sorted(lc.items()))+").\n",
     "## Содержание"]
for theme,items in groups:
    if items: out.append(f"- {theme} ({len(items)})")
out.append("")
for theme,items in groups:
    if not items:continue
    out.append(f"## {theme}")
    for en,tr,ru in items:
        out.append(f"- **{en}** {tr} — {ru}")
    out.append("")
io.open(MD,"w",encoding="utf-8").write("\n".join(out))

print(f"OK: {len(entries)} карточек; по уровням:",dict(lc))
