#!/usr/bin/env python3
"""Baut die Projekttabelle der Profilseite aus den öffentlichen Repos der Organisation.

Angezeigt wird jedes öffentliche Repo außer .github, Forks und archivierten Repos.
Name und Text kommen in dieser Reihenfolge aus:
  1. projekte.json (Schlüssel = Repo-Name, Felder "name", "text", "link")
  2. der Beschreibung des Repos (About)
  3. der ersten Überschrift und dem ersten Absatz der README
"""
import base64
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request

ORG = os.environ.get("ORG", "seidenbit")
README = "profile/README.md"
OVERRIDES = "projekte.json"
START = "<!-- projekte:start -->"
END = "<!-- projekte:end -->"
AUSGENOMMEN = {".github"}
MAX_TEXT = 280


def api(path):
    req = urllib.request.Request("https://api.github.com" + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    token = os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def oeffentliche_repos():
    repos, seite = [], 1
    while True:
        teil = api(f"/orgs/{ORG}/repos?type=public&per_page=100&page={seite}")
        repos += teil
        if len(teil) < 100:
            return [
                r for r in repos
                if not r["private"] and not r["fork"] and not r["archived"]
                and r["name"] not in AUSGENOMMEN
            ]
        seite += 1


def readme_von(repo):
    try:
        daten = api(f"/repos/{ORG}/{repo}/readme")
    except urllib.error.HTTPError as fehler:
        if fehler.code == 404:
            return ""
        raise
    return base64.b64decode(daten["content"]).decode("utf-8", "replace")


def normal(text):
    text = text.lower()
    for alt, neu in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(alt, neu)
    return re.sub(r"[^a-z0-9]", "", text)


def ohne_markdown(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"(\*\*|__|`)", "", text)
    return re.sub(r"\s+", " ", text).strip()


def anzeigename(repo, readme):
    treffer = re.search(r"^#\s+(.+?)\s*#*\s*$", readme, re.M)
    if treffer:
        titel = ohne_markdown(treffer.group(1))
        if normal(titel) == normal(repo):
            return titel
    return " ".join(teil.capitalize() for teil in re.split(r"[-_]+", repo) if teil)


def erster_absatz(readme):
    zeilen = readme.splitlines()
    beginn = next((i + 1 for i, z in enumerate(zeilen) if z.startswith("# ")), 0)
    absatz, im_code = [], False
    for zeile in zeilen[beginn:]:
        s = zeile.strip()
        if s.startswith("```"):
            im_code = not im_code
            continue
        if im_code:
            continue
        if not s:
            if absatz:
                break
            continue
        if not absatz and (s.startswith(("#", "<", "!", "|", ">", "- ", "* ")) or re.match(r"\d+\.\s", s)):
            continue
        absatz.append(s)
    return kuerzen(ohne_markdown(" ".join(absatz)))


def kuerzen(text):
    if len(text) <= MAX_TEXT:
        return text
    schnitt = text[:MAX_TEXT]
    satzende = max(schnitt.rfind(". "), schnitt.rfind("? "), schnitt.rfind("! "))
    if satzende > MAX_TEXT // 2:
        return schnitt[: satzende + 1]
    return schnitt.rsplit(" ", 1)[0] + " …"


def zelle(text):
    return text.replace("|", "\\|")


def zeile(repo, vorgaben):
    name = repo["name"]
    eigen = vorgaben.get(name, {})
    readme = "" if ("name" in eigen and "text" in eigen) else readme_von(name)
    titel = eigen.get("name") or anzeigename(name, readme)
    text = eigen.get("text") or (repo.get("description") or "").strip() or erster_absatz(readme)
    link = eigen.get("link") or (repo.get("homepage") or "").strip()
    if not link and repo.get("has_pages"):
        link = f"https://{ORG}.github.io/{name}/"
    spalte = zelle(text)
    if link:
        spalte = (spalte + " " if spalte else "") + f"[Ausprobieren]({link})"
    return titel, f"| **[{zelle(titel)}]({repo['html_url']})** | {spalte} |"


def tabelle(repos, vorgaben):
    zeilen = sorted((zeile(r, vorgaben) for r in repos), key=lambda z: z[0].lower())
    kopf = ["| Projekt | Worum es geht |", "|---|---|"]
    if not zeilen:
        return "\n".join(kopf + ["| – | Noch keine öffentlichen Projekte. |"])
    return "\n".join(kopf + [z for _, z in zeilen])


def main():
    with open(OVERRIDES, encoding="utf-8") as datei:
        vorgaben = json.load(datei)
    with open(README, encoding="utf-8") as datei:
        inhalt = datei.read()
    if START not in inhalt or END not in inhalt:
        sys.exit(f"Markierungen {START} / {END} fehlen in {README}")
    # Der Monat im Kommentar sorgt für einen Commit pro Monat. Ohne Commits schaltet
    # GitHub zeitgesteuerte Workflows in öffentlichen Repos nach 60 Tagen ab.
    stand = datetime.date.today().strftime("%Y-%m")
    block = f"{START}\n<!-- Stand: {stand} -->\n{tabelle(oeffentliche_repos(), vorgaben)}\n{END}"
    vorher, rest = inhalt.split(START, 1)
    _, nachher = rest.split(END, 1)
    neu = vorher + block + nachher
    if neu != inhalt:
        with open(README, "w", encoding="utf-8") as datei:
            datei.write(neu)
        print("Profilseite aktualisiert")
    else:
        print("Keine Änderung")


if __name__ == "__main__":
    main()
