#!/usr/bin/env python3
"""sbobba.py — misura la sbobba AI in un testo italiano.

Tre canali, e sono tre cose diverse. Non si sommano in un voto unico apposta:
un numero solo nasconderebbe che il primo è misurato e il terzo è un elenco di
gusti.

  canale 1  EPANORTOSI ENFATICA, la correzione al rialzo («non X, ma Y»).
            I pattern sono copiati VERBATIM da
            artificial-epanorthosis-eval.py, §7.8 del paper di Federico Boggia
            (arXiv:2607.21498), così la misura qui coincide con la definizione
            operativa di quella ricerca invece di essere una stima fatta a
            occhio. La densità è per 10.000 parole, come nel paper,
            e si legge contro la base umana del genere: è l'Indice di epanortosi.
            ⚠️ Validato: micro P=0,45 R=0,52 su 206 finestre annotate a mano
            (Appendice B). La precisione si spacca per origine: 0,82 sul testo
            generato, 0,17 sul testo umano. Quindi su una pagina scritta da un
            modello questo canale è affidabile, su una riga scritta da Federico
            no: là segnala e basta.

  canale 1b LE ALTRE SUPERFICI della stessa figura, che il canale 1 non prende
            («più che X, Y», «X, o meglio Y», «definirlo X è riduttivo»…).
            Fontanier la classifica come figura di PENSIERO, cioè senza una
            forma canonica: vietare una forma sola sposta il fenomeno sulle
            altre. Questi sono candidati DA LEGGERE, non un conto da abbassare:
            «anzi», «cioè» e «in realtà» sono italiano normale.

  canale 2  LE FORMULE, cioè il lessico che fa suonare generato un testo
            italiano: i riempitivi, «rappresenta», «permette di», «Ecco»,
            il gerundio di commento, l'attribuzione vaga, i trattini lunghi.

  canale 3  LA PRIMA PERSONA: quante volte l'autore c'è. A zero, il testo parla
            come un manuale generato. Non è un difetto da togliere, è una cosa
            che manca.

Uso
---
    sbobba.py articolo.html                   # un file
    sbobba.py testi/ articoli/                # cartelle
    sbobba.py --frasi testi/                  # stampa le righe da rivedere
    sbobba.py --json testi/                   # per un altro programma
    cat bozza.txt | sbobba.py -               # dallo standard input
    sbobba.py --genere oratorio discorso.md   # forza il genere

Le basi umane per genere (occorrenze ogni 10.000 parole) vengono dalla Tabella 1
e dal §7.8 del paper. Dove una base umana non esiste lo dice, invece di
inventarne una.
"""
from __future__ import annotations

import argparse
import glob
import html as H
import json
import os
import re
import sys

# --------------------------------------------------------------------------
# CANALE 1 — pattern del paper, §7.8. Copiati verbatim: non si "migliorano"
# qui, sennò la misura smette di essere confrontabile con quella pubblicata.
# --------------------------------------------------------------------------
RE_NONMA = re.compile(r"\bnon\b(?:(?!\bma\b|\bbens[iì]\b)[^.;:!?\n]){2,70}?\b(ma|bens[iì])\b", re.I)
RE_NONSOLO = re.compile(r"\bnon solo\b(?:[^.;:!?\n]){2,90}?\bma\b", re.I)
RE_NONVIRG = re.compile(r"\bnon\b(?:(?!\bma\b)[^.;:!?\n]){2,55}?,\s*(è|e'|sono|era|significa)\b", re.I)
NEG = re.compile(r"^\W*(non è|non sono|non ho|non facc|non vend|questa? non è|non si tratta di)\b", re.I)
IDIT = re.compile(r"non solo|non appena|non che\b", re.I)

# --------------------------------------------------------------------------
# CANALE 1b — le due lenti aggiunte per il testo scritto a mano
# più le superfici elencate nel §02 dell'articolo divulgativo che accompagna
# il paper. Il paper dice che il «non… ma» è la parte esposta
# del fenomeno: questo canale guarda il resto.
# --------------------------------------------------------------------------
NEG_INTERNA = re.compile(r"\b(non (?:è|e'|sono|era|vuol dire|significa|si tratta di|serve|sta ))", re.I)
AFFERMA = re.compile(r"^\W*(è|e'|sono|vuol dire|significa|serve|sta |si tratta di|lo e'|"
                     r"e' (?:proprio|invece|piuttosto))\b", re.I)
SUPERFICI = {
    "più-che": r"\bpiù che [^.;:!?\n]{3,50}?,\s*\b",
    "o-meglio": r"\b(o meglio|per meglio dire|o per meglio dire|più precisamente|per essere precisi|a dirla tutta)\b,?",
    "definirlo-riduttivo": r"\b(definir\w+|chiamar\w+) [^.;:!?\n]{2,40}? (è riduttivo|non rende giustizia|sarebbe riduttivo)",
    "in-realtà": r"\b(quello che sembra|ciò che sembra)[^.;:!?\n]{2,50}?\bin realtà\b|\bsolo in apparenza\b",
    "non-tanto": r"\bnon tanto [^.;:!?\n]{2,50}?\bquanto\b",
    "altro-che": r"(?:^|[.;!?]\s)Altro che\b",
    "anzi": r"(?:^|[,;] )anzi\b",
    "se-non-almeno": r"\bse non [^.;:!?\n]{2,40}?,\s*almeno\b",
}

# --------------------------------------------------------------------------
# CANALE 2 — le formule. Ogni voce ha la sua riga di cura in
# riferimenti/formule.md.
# --------------------------------------------------------------------------
FORMULE = {
    "riempitivi": r"\b(fondamental\w+|crucial\w+|essenzial\w+|prezios\w+|decisiv\w+"
                  r"|imprescindibil\w+|ottimal\w+|strategic\w+|efficac\w+|di valore"
                  r"|valore aggiunto|significativ\w+|notevol\w+|straordinari\w+"
                  r"|di primaria importanza|di fondamentale importanza)\b",
    "svuotaverbi": r"\b(rappresent\w+|costituisc\w+|si configura|si traduce in|si rivela"
                   r"|risulta essere|va a costituire|si pone come|funge da)\b",
    "permette-di": r"\b(permett\w+ di|consent\w+ di|offr\w+ la possibilità di"
                   r"|dà la possibilità di|ha la capacità di|è in grado di)\b",
    "la-chiave": r"\b(la chiave (?:è|sta)|il segreto (?:è|sta)|fa (?:tutta )?la differenza"
                 r"|il punto di partenza|un ruolo (?:chiave|centrale|fondamentale|vitale)"
                 r"|il vero punto è|la vera domanda è|il bello è che)\b",
    "ecco": r"(?:^|[.;!?] )Ecco\b",
    "mondo-oggi": r"\b(nel mondo (?:di oggi|digitale|del)|nell'era (?:dell|digitale|di)|nel panorama"
                  r"|nello scenario|oggi più che mai|in un contesto sempre più"
                  r"|nell'epoca (?:in cui|dell))\b",
    "meta-guida": r"\b(in questa guida|in questo articolo (?:vedremo|scopriremo)|analizzeremo"
                  r"|approfondiremo|In conclusione|Come abbiamo visto|Vediamo insieme"
                  r"|Scopriamo insieme|Facciamo un passo indietro|Prima di tutto, però)\b",
    "gerundio-commento": r",\s*(evidenziando|sottolineando|dimostrando|confermando"
                         r"|testimoniando|riflettendo|mettendo in luce|a testimonianza d)\w*",
    "puffery": r"\b(segna una svolta|una pietra miliare|consolida la sua posizione"
               r"|a testimonianza del|non a caso|degno di nota|vale la pena sottolineare)\b",
    "attribuzione-vaga": r"\b(gli esperti (?:concordano|sostengono|dicono)|gli studi (?:dimostrano|mostrano)"
                         r"|è (?:ormai )?noto che|molti sostengono|secondo gli esperti"
                         r"|le ricerche (?:mostrano|dimostrano)|si stima che|è risaputo)\b",
    "rinforzi": r"\b(semplicemente|letteralmente|assolutamente|davvero incredibil\w+"
                r"|estremamente|incredibilmente|assolutamente fondamentale)\b",
    "anglicismi": r"\b(best practice|step by step|mindset|know-how|deep dive|actionable"
                  r"|game changer|must have|win-win|asset strategico)\b",
    "marketing": r"\b(rivoluzionar\w+|sblocca il tuo|percorso trasformativo|viaggio nel mondo"
                 r"|cambia le regole del gioco|porta(?:re)? al livello successivo)\b",
    "domanda-retorica": r"(?:^|[.;!?] )(E se ti dicessi|Ti sei mai chiest|Immagina di"
                        r"|Cosa succederebbe se|Sai qual è|Hai mai pensato)",
    "due-punti-a-effetto": r"\b(La parte migliore|Il bello|Il punto|La verità|Il risultato"
                           r"|La cosa interessante)\s*:\s+[a-zà-ù]",
    "frammento": r"(?:^|[.!?] )(Punto\.|Tutto qui\.|Ed è tutto\.|Fine della storia\.|Semplice\.|Nient'altro\.)",
    "trattino-lungo": r"—|&mdash;|–|&ndash;",
}

# CANALE 3 — i segni che dietro al testo c'è qualcuno.
IO = (r"\b(in aula|nei miei corsi|ai (?:miei )?corsi|ai miei studenti|secondo me|ho visto"
      r"|mi capita|quando insegno|lo ripeto in ogni corso|nella mia esperienza|mi è capitato"
      r"|me lo chiedono|io (?:faccio|uso|scrivo|lo dico)|te lo dico|l'ho provato)\b")

# --------------------------------------------------------------------------
# Le basi umane, per 10.000 parole. Tabella 1 e §7.8 del paper.
# None = una base umana non esiste, e non se ne inventa una.
# --------------------------------------------------------------------------
BASI = {
    "enciclopedico": (1.2, "Tabella 1, Wikipedia"),
    "giornalistico": (2.4, "Tabella 1, Common Crawl News"),
    "accademico": (3.6, "Tabella 1, abstract"),
    "didattico": (3.6, "giudizio: la base pubblicata più vicina è l'abstract accademico"),
    "narrativo": (7.5, "Tabella 1, Liber Liber"),
    "conversazionale": (8.2, "Tabella 1, domanda e risposta informale"),
    "argomentativo": (12.0, "§7.8, base italiana (Beccaria)"),
    "oratorio": (14.0, "§7.8, orazioni di pubblico dominio in italiano"),
    "promozionale": (None, "il paper dichiara che per il promozionale una base umana pubblica non esiste"),
}

# Il genere si indovina dal percorso; --genere lo forza. Le voci qui sotto sono
# un esempio: si adattano alle cartelle del proprio progetto, e quello che conta
# è la mappa fra una cartella e uno dei generi di BASI.
GENERE_DA_PERCORSO = [
    (r"(?i)(^|/)(wiki|enciclopedia|glossario|voci)/", "enciclopedico"),
    (r"(?i)(^|/)(news|notizie|stampa|comunicati)/", "giornalistico"),
    (r"(?i)(^|/)(paper|abstract|ricerca)/", "accademico"),
    (r"(?i)(^|/)(corsi|lezioni|didattica|manuale|guide)/", "didattico"),
    (r"(?i)(^|/)(racconti|narrativa|romanzo)/", "narrativo"),
    (r"(?i)(^|/)(faq|forum|risposte|domande)/", "conversazionale"),
    (r"(?i)(^|/)(discorsi|speech|keynote|video)/", "oratorio"),
    (r"(?i)(^|/)(landing|vendita|prodotti|shop)/|index\.html$", "promozionale"),
    (r"(?i)(^|/)(articoli|pubblicazioni|blog|saggi|libri)/", "argomentativo"),
]


def genere_di(percorso: str) -> str:
    p = percorso.lstrip("./")
    for pat, g in GENERE_DA_PERCORSO:
        if re.search(pat, p):
            return g
    return "argomentativo"


def parole(t: str) -> list:
    return re.findall(r"[A-Za-zÀ-ÿ']+", t)


# --------------------------------------------------------------------------
def testo(percorso: str) -> str | None:
    """Il testo che una persona legge. Il resto resta fuori."""
    src = open(percorso, encoding="utf-8").read()
    return da_sorgente(src, percorso)


def da_sorgente(src: str, percorso: str = "") -> str | None:
    if percorso.endswith(".md") or (not percorso.endswith(".html") and "<" not in src[:400]):
        if src.startswith("---"):
            src = src.split("---", 2)[-1]
        src = re.sub(r"^### QUIZ\n(?:- .*\n)+", "", src, flags=re.M)
        src = re.sub(r"```.*?```|`[^`]+`", " ", src, flags=re.S)
        src = re.sub(r"^[#@|].*$", " ", src, flags=re.M)
        src = re.sub(r"[*_\[\]]", "", src)
        return re.sub(r"[ \t]+", " ", src).strip()

    corpo = re.search(r"<article[^>]*>(.*?)</article>", src, re.S)
    if corpo:
        dentro = corpo.group(1)
    else:
        fra = re.search(r"</nav>(.*?)<footer", src, re.S)
        if not fra:
            return None
        dentro = fra.group(1)
    g = re.sub(r"<!--.*?-->", " ", dentro, flags=re.S)
    g = re.sub(r"<(script|style|pre|code|svg|noscript)\b.*?</\1>", " ", g, flags=re.S)
    # Un tag chiuso vale come fine frase: sennò due paragrafi diventano una frase
    # sola e la lente «frase negata + frase affermata» non scatta mai.
    g = re.sub(r"</(p|li|h[1-6]|div|section|td|blockquote)>", ". ", g)
    g = H.unescape(re.sub(r"<[^>]+>", " ", g))
    return re.sub(r"[ \t]+", " ", re.sub(r"\s*\n\s*", "\n", g)).strip()


# --------------------------------------------------------------------------
def canale1(t: str) -> list:
    """Epanortosi enfatica, i quattro pattern del paper."""
    esiti = []
    for m in RE_NONMA.finditer(t):
        if not IDIT.search(m.group(0)):
            esiti.append(("non…ma", m.group(0).strip()))
    for m in RE_NONSOLO.finditer(t):
        esiti.append(("non solo…ma", m.group(0).strip()))
    for m in RE_NONVIRG.finditer(t):
        esiti.append(("non…, è", m.group(0).strip()))
    frasi = re.split(r"(?<=[.!?])\s+", t)
    for i in range(len(frasi) - 1):
        if NEG.match(frasi[i].strip()) and not NEG.match(frasi[i + 1].strip()):
            esiti.append(("frase negata + affermata",
                          (frasi[i].strip() + " " + frasi[i + 1].strip())[:160]))
    return esiti


def canale1b(t: str) -> list:
    """Le altre superfici. Candidati da leggere, non un conto da abbassare."""
    esiti = []
    frasi = re.split(r"(?<=[.!?])\s+", t)
    for i in range(len(frasi) - 1):
        a, b = frasi[i].strip(), frasi[i + 1].strip()
        if NEG_INTERNA.search(a) and AFFERMA.match(b) and not NEG.match(a):
            esiti.append(("negazione interna + affermazione", (a + " " + b)[:160]))
    for m in re.finditer(r",\s*(?:e|ma)\s+non (?:è|e'|sono)\b[^.;:!?\n]{2,60}", t, re.I):
        esiti.append(("coda negata", m.group(0).strip()))
    for nome, pat in SUPERFICI.items():
        for m in re.finditer(pat, t, re.I):
            esiti.append((nome, t[max(0, m.start() - 30):m.end() + 40].strip()))
    return esiti


def canale2(t: str) -> dict:
    return {k: [m for m in re.finditer(p, t, re.I)] for k, p in FORMULE.items()}


# --------------------------------------------------------------------------
def analizza(percorso: str, t: str, genere: str | None) -> dict:
    g = genere or genere_di(percorso)
    n = max(len(parole(t)), 1)
    c1, c1b, c2 = canale1(t), canale1b(t), canale2(t)
    dens = round(len(c1) * 10000 / n, 1)
    base, fonte = BASI.get(g, (None, ""))
    ei = round(dens / base, 2) if base else None
    formule = sum(len(v) for v in c2.values())
    return {
        "file": percorso, "genere": g, "parole": n,
        "epanortosi": len(c1), "densita": dens,
        "base_umana": base, "fonte_base": fonte, "indice": ei,
        "superfici": len(c1b),
        "formule": formule, "formule_x1000": round(formule * 1000 / n, 1),
        "per_tipo": {k: len(v) for k, v in c2.items() if v},
        "io": len(re.findall(IO, t, re.I)),
        "esempi_c1": c1[:12], "esempi_c1b": c1b[:12],
        "esempi_c2": {k: [t[max(0, m.start() - 55):m.end() + 55].strip() for m in v[:4]]
                      for k, v in c2.items() if v},
    }


def raccogli(args: list) -> list:
    out = []
    for a in args:
        if os.path.isdir(a):
            for e in ("html", "md", "txt"):
                out += glob.glob(f"{a}/**/*.{e}", recursive=True)
        else:
            out.append(a)
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser(description="Misura la sbobba AI in un testo italiano.")
    ap.add_argument("percorsi", nargs="*", default=["."])
    ap.add_argument("--frasi", action="store_true", help="stampa le righe da rivedere")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--genere", choices=sorted(BASI))
    ap.add_argument("--soglia", type=float, default=0.0,
                    help="mostra solo i file oltre questo indice o queste formule per 1000")
    a = ap.parse_args()

    esiti, saltati = [], []
    if a.percorsi == ["-"]:
        t = da_sorgente(sys.stdin.read(), "stdin.txt")
        esiti.append(analizza("(stdin)", t, a.genere or "argomentativo"))
    else:
        for f in raccogli(a.percorsi):
            try:
                t = testo(f)
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            if not t:
                saltati.append(f)
                continue
            esiti.append(analizza(f, t, a.genere))

    if a.json:
        print(json.dumps({"file": esiti, "saltati": saltati}, ensure_ascii=False, indent=1))
        return 0

    esiti.sort(key=lambda r: (-(r["indice"] or 0), -r["formule_x1000"]))
    print(f"\n{'file':52}{'genere':16}{'parole':>7}{'epan':>5}{'/10k':>7}{'ind':>6}"
          f"{'sup':>5}{'form':>6}{'/1k':>6}{'io':>4}")
    for r in esiti:
        if a.soglia and (r["indice"] or 0) < a.soglia and r["formule_x1000"] < a.soglia:
            continue
        ind = "—" if r["indice"] is None else f"{r['indice']:.2f}"
        print(f"{r['file'][:52]:52}{r['genere']:16}{r['parole']:7}{r['epanortosi']:5}"
              f"{r['densita']:7}{ind:>6}{r['superfici']:5}{r['formule']:6}"
              f"{r['formule_x1000']:6}{r['io']:4}")

    tot = {}
    for r in esiti:
        for k, v in r["per_tipo"].items():
            tot[k] = tot.get(k, 0) + v
    print("\n--- formule per tipo ---")
    for k, v in sorted(tot.items(), key=lambda x: -x[1]):
        print(f"{k:22}{v}")
    pw = sum(r["parole"] for r in esiti)
    pe = sum(r["epanortosi"] for r in esiti)
    print(f"\nfile: {len(esiti)}   parole: {pw}   epanortosi: {pe}"
          f"   formule: {sum(tot.values())}")
    print("ind = Indice di epanortosi: densità del file diviso la base umana del genere.")
    print("      1,00 = come scrive una persona in quel genere. Sopra = correzione al rialzo di troppo.")
    print("      «—» = per quel genere una base umana pubblica non esiste (promozionale).")
    print("sup = altre superfici della stessa figura: da leggere, non da azzerare.")
    if saltati:
        print(f"⚠️ saltati (né <article> né corpo fra </nav> e <footer>): {len(saltati)}")
        for f in saltati[:8]:
            print(f"     {f}")

    if a.frasi:
        print("\n=== righe da rivedere ===")
        for r in esiti:
            if not (r["esempi_c1"] or r["esempi_c1b"] or r["esempi_c2"]):
                continue
            print(f"\n## {r['file']}  [{r['genere']}]")
            for tipo, s in r["esempi_c1"]:
                print(f"  EPAN [{tipo}] {re.sub(chr(10), ' ', s)[:150]}")
            for tipo, s in r["esempi_c1b"]:
                print(f"  sup  [{tipo}] {re.sub(chr(10), ' ', s)[:150]}")
            for k, ss in r["esempi_c2"].items():
                for s in ss:
                    print(f"  form [{k}] …{re.sub(chr(10), ' ', s)[:130]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
