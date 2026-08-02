#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Собирает тренажёр и тематический словарь из карточки.csv + грамматика.csv
import json, re, io

SOURCES=["/home/user/English/словарь/карточки.csv",
         "/home/user/English/словарь/грамматика.csv"]
HTML="/home/user/English/приложение/тренажёр.html"
MD="/home/user/English/словарь/словарь_по_темам.md"

entries=[]      # [en, tr, ru, theme]
groups=[]       # [(тема, [(en,tr,ru),...]), ...]

def clean_theme(line):
    t=line.lstrip("#").strip().strip("─ ").strip()
    return t or "Прочее"

for path in SOURCES:
    try:
        f=io.open(path,encoding="utf-8")
    except FileNotFoundError:
        continue
    current="Прочее"; cur=None
    with f:
        for i,raw in enumerate(f):
            line=raw.rstrip("\n")
            if not line.strip():continue
            if line.lstrip().startswith("#"):
                current=clean_theme(line); cur=[]; groups.append((current,cur)); continue
            parts=line.split(",")
            if len(parts)<3:continue
            en=parts[0].strip()
            if en.lower()=="english":continue
            tr=parts[1].strip(); ru=",".join(parts[2:]).strip()
            entries.append([en,tr,ru,current])
            if cur is None:
                cur=[]; groups.append((current,cur))
            cur.append((en,tr,ru))

# 1) залить в тренажёр (4 поля: en, tr, ru, тема)
arr="[\n"+",\n".join(json.dumps(e,ensure_ascii=False) for e in entries)+"\n]"
html=io.open(HTML,encoding="utf-8").read()
html,n=re.subn(r"const DEFAULT = \[.*?\];","const DEFAULT = "+arr+";",html,count=1,flags=re.S)
assert n==1,"не нашёл блок DEFAULT"
io.open(HTML,"w",encoding="utf-8").write(html)

# 2) словарь по темам
out=["# 📚 Словарь и грамматика по темам (A1 → B2)\n",
     "Автосборка из `карточки.csv` + `грамматика.csv`. Формат: **фраза** /транскрипция/ — перевод.\n",
     f"Всего карточек: **{len(entries)}**.\n","## Содержание"]
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

print(f"OK: {len(entries)} карточек в тренажёре; тем: {len([g for g in groups if g[1]])}")
