#!/usr/bin/env python3
"""sbobba.py — misura la sbobba AI in un testo italiano.

Tre canali, e sono tre cose diverse. Non si sommano in un voto unico apposta:
un numero solo nasconderebbe che il primo è misurato e il terzo è un elenco di
gusti.

  canale 1  EPANORTOSI ENFATICA, la correzione al rialzo («non X, ma Y»).
            I pattern sono copiati VERBATIM da
            pubblicazioni/artificial-epanorthosis-eval.py (§7.8 del paper di
            Federico Boggia, arXiv:2607.21498), così la misura qui coincide con
            la definizione operativa della sua ricerca invece di essere una
            stima fatta a occhio. La densità è per 10.000 parole, come nel paper,
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
            Superset della lista di _strumenti/spie-ai.py.

  canale 3  LA PRIMA PERSONA: quante volte l'autore c'è. A zero, il testo parla
            come un manuale generato. Non è un difetto da togliere, è una cosa
            che manca.

Uso
---
    sbobba.py wiki/seo/cos-e-seo.html         # un file
    sbobba.py wiki pubblicazioni              # cartelle
    sbobba.py --frasi wiki/ai                 # stampa le righe da rivedere
    sbobba.py --json wiki                     # per un altro programma
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
# (_libri/strumenti/epanortosi.py) più le superfici elencate nel §02
# dell'articolo divulgativo. Il paper dice che il «non… ma» è la parte esposta
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
    # ⚠️ «X invece di Y» mancava, ed e' la superficie che scappa piu' spesso:
    # non nega e non corregge, sostituisce, quindi nessuno dei pattern del
    # paper la prende. Segnalata da Federico il 2026-09-23 dopo averla vista
    # cinque volte in una pagina che il rilevatore dava a zero.
    # ⚠️ E' anche italiano normalissimo («vado a piedi invece di prendere
    # l'auto»): sta nel canale 1b, che e' un elenco di candidati da leggere.
    # Si guarda cosa c'e' dopo «invece di». Se e' un'alternativa vera che
    # qualcuno poteva scegliere, e' una frase; se e' la versione scadente
    # della stessa cosa, messa li' per far brillare la prima, e' la figura.
    "invece-di": r"\binvece (?:di|che)\b(?=[^.;:!?\n]{3,45})",
    "piuttosto-che": r"\bpiuttosto che\b|\bpiu' che altro\b|\bpiù che altro\b",
    "tutt-altro": r"\b(tutt'altro che|lungi da|ben lontano da|nulla a che vedere con)\b",
    # L'ordine rovesciato: prima si afferma e poi si nega quello che si e'
    # lasciato indietro. «E' un percorso, non un corso.» I pattern del paper
    # guardano la negazione per prima e questa gli passa sotto.
    "afferma-poi-nega": r"\b(?:è|e'|sono|era|resta|diventa) [^.;:!?\n]{3,40}, non (?:un|una|uno|il|lo|la|i|gli|le|solo|soltanto|proprio)\b",
    "semmai": r"(?:^|[,;] )(semmai|se mai|caso mai)\b",
    "a-ben-vedere": r"\b(a ben vedere|a guardare bene|a conti fatti|se ci pensi|a pensarci)\b",
    "nel-senso-che": r"\b(nel senso che|per essere chiari|per intenderci|diciamo che)\b",
}

# --------------------------------------------------------------------------
# CANALE 2 — le formule. Superset della lista di _strumenti/spie-ai.py.
# Ogni voce ha la sua riga di cura in riferimenti/formule.md.
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
    "schiarirsi-la-voce": r"(?:^|[.;!?]\s)(Diciamocelo|Sia chiaro|Facciamo chiarezza"
                          r"|Andiamo con ordine|Partiamo dall'inizio"
                          r"|Chiariamo subito|Facciamola semplice|Detto questo|Sgombriamo il campo)\b",
    "finta-rivelazione": r"\b(quello che nessuno (?:ti |vi )?dice|la parte che (?:tutti|quasi tutti) salt\w+"
                         r"|pochi lo sanno|il segreto che non ti dicono|nessuno te lo dice"
                         r"|quello che non ti hanno (?:mai )?detto|la verità è che|hai letto bene"
                         r"|non sto esagerando|spoiler:|la cosa che nessuno)\b",
    "elenco-negato": r"(?:^|[.;!?]\s)Non [^.;!?\n]{2,45}\.\s*Non [^.;!?\n]{2,45}\.\s*(?!Non )[A-ZÀ-Ù][^.;!?\n]{2,32}\.",
    "guida-al-lettore": r"\b(come (?:puoi|potete|si può) vedere|questo punto (?:è importante|conta)"
                        r"|questa distinzione (?:è importante|conta)"
                        r"|in altre parole|come dicevo (?:prima|sopra)|torniamo un attimo)\b",
    "apostrofe": r"(?:^|[.;!?]\s)(Fidati|Credimi|Pensaci(?: un attimo)?[:.]"
                 r"|Colpo di scena:|Indovina un po'|Sorpresa:)",
    "trattino-lungo": r"—|&mdash;|–|&ndash;",
}

# CANALE 3 — i segni che dietro al testo c'è qualcuno.
IO = (r"\b(in aula|nei miei corsi|ai (?:miei )?corsi|ai miei studenti|secondo me|ho visto"
      r"|mi capita|quando insegno|lo ripeto in ogni corso|nella mia esperienza|mi è capitato"
      r"|me lo chiedono|io (?:faccio|uso|scrivo|lo dico)|te lo dico|l'ho provato)\b")

# --------------------------------------------------------------------------
# CANALE 4 — RITMO: ripetizione ed elencazione.
#
# Perché serve un canale a parte. I canali 1 e 2 guardano PAROLE: una stringa
# c'è o non c'è. Questo guarda la FORMA di un paragrafo, che è dove un testo
# generato si riconosce anche quando ha il lessico pulito. Le lenti vengono
# dallo stato dell'arte inglese (sloplint: `phrase-echo`, `rule-of-three`,
# `no-x-no-y`, `cadence`; slopscore: le dimensioni «redundancy» e «cadence»;
# no-slop: le «structural formulas» di WP:AISIGNS) e sono ritarate sull'italiano.
#
# ⚠️ DUE COSE CAMBIANO PASSANDO ALL'ITALIANO, e non sono dettagli.
#
#   1. «Elegant variation» va CAPOVOLTA. In inglese lo stile chiede di ripetere
#      la stessa parola, e chi la cambia a ogni riga fa un errore: per questo
#      no-slop la segnala. In italiano la scuola insegna l'esatto contrario, la
#      variatio, e chi ripete «corso» cinque volte scrive bene lo stesso. Quindi
#      qui NON si segnala un sostantivo ripetuto: si segnala il contrario,
#      cioè la `sinonimia`, la stessa cosa chiamata in quattro modi diversi in
#      poche righe («il percorso… il cammino… il viaggio… l'iter»), che è la
#      forma che la sbobba prende in italiano.
#   2. Il TRICOLON non è un difetto per definizione. Tre membri che portano
#      ciascuno un fatto diverso è retorica buona e sta in Cicerone. Quello che
#      si segnala è il tricolon SECCO, tre parole sole in fila senza contenuto
#      («veloce, affidabile e sicuro»), che è la forma da copy SEO.
#
# ⚠️ Le soglie NON sono importate dall'inglese: sono misurate sui manoscritti
# di Federico in `_libri/*/manoscritto/`, che è il corpus umano di questo
# progetto, con `sbobba.py --taratura _libri`. Stessa logica del canale 1, dove
# la base viene dal paper invece che da un'opinione.
# --------------------------------------------------------------------------
STOP = set("""il lo la i gli le un uno una di a da in con su per tra fra del dello della dei
degli delle al allo alla ai agli alle dal dallo dalla dai dagli dalle nel nello nella nei negli
nelle col coi sul sullo sulla sui sugli sulle e ed o od ma se che chi cui non come dove quando
perche perché più meno molto poco tanto quanto è sono era erano sia siano essere stato stata
stati state ha hanno aveva avevano avere ho hai abbiamo avete si ci vi ne mi ti loro questo
questa questi queste quello quella quelli quelle anche ancora già poi solo sempre mai qui qua
ogni tutti tutto tutta tutte alcuni altri altro altra altre stesso stessa suo sua suoi sue mio
mia miei mie tuo tua tuoi tue nostro nostra vostro quindi però invece cioè cosa fare fa fatto
può puoi posso devi deve dei una del della""".split())

# Le coppie fisse: due aggettivi saldati che viaggiano insieme e non aggiungono
# niente l'uno all'altro. Elenco curato e italiano, invece di una regex
# «aggettivo e aggettivo» che prenderebbe mezza lingua.
# ⚠️ Sempre `ed?`: davanti a vocale l'italiano scrive «ed», e «rapido ed
# efficace» è proprio la forma che si vuole prendere.
COPPIE = (r"\b(semplice ed? (?:intuitiv|immediat|veloc|chiar)\w+|chiar[oa] ed? (?:diret|sempli|conci)\w+"
          r"|rapid[oa] ed? (?:efficac|sicur|semplic)\w+|efficace ed? efficient\w*"
          r"|completo ed? (?:esaustiv|dettagliat)\w+|pratico ed? (?:concret|immediat|utile)\w*"
          r"|solido ed? affidabil\w*|moderno ed? (?:innovativ|accattivant)\w+"
          r"|flessibile ed? scalabil\w*|sicuro ed? affidabil\w*|utile ed? interessant\w*)\b")

# Gli insiemi di sinonimi che i modelli girano per non ripetersi. Quando in
# poche righe compaiono tre nomi diversi per la stessa cosa, il testo sta
# mascherando la ripetizione invece di dire la cosa.
SINONIMI = {
    "percorso": ("percorso", "cammino", "viaggio", "iter", "tragitto"),
    "strumento": ("strumento", "soluzione", "risorsa", "tool", "dispositivo"),
    "mondo": ("mondo", "panorama", "scenario", "universo", "ecosistema", "landscape"),
    "capacità": ("capacità", "abilità", "competenza", "skill", "attitudine"),
    "crescita": ("crescita", "evoluzione", "sviluppo", "progressione", "ascesa"),
    "metodo": ("metodo", "approccio", "metodologia", "modalità", "paradigma"),
    "sfida": ("sfida", "ostacolo", "difficoltà", "criticità", "problematica"),
}

RE_TRICOLON = re.compile(
    r"(?<![,;:])\b([a-zà-ù]{4,15}), ([a-zà-ù]{4,15}) e(?:d)? ([a-zà-ù]{4,15})\b(?![ ]*[a-zà-ù]{3,})")

# ⚠️ IL PUNTO PIÙ ITALIANO DI TUTTO IL CANALE 4. Tre parole in fila non sono
# una spia: «telefono, email e partita IVA» è un elenco di cose vere, e la
# prima taratura sul corpus umano lo segnalava 249 volte. Quello che i modelli
# producono in serie è la terna di AGGETTIVI, «indicizzato, pertinente e
# leggibile», tre giudizi al posto di un fatto. In italiano l'aggettivo si
# riconosce dalla coda, e questa è la differenza che il rilevatore deve fare.
CODA_AGG = re.compile(r"(at[oaie]|it[oaie]|ut[oaie]|iv[oaie]|os[oaie]|bil[ei]|"
                      r"ant[ei]|ent[ei]|ic[oaie]|al[ei]|ar[ei]|ile)$")
RE_TERNA = re.compile(r"(?:^|[.;:!?]\s)([A-ZÀ-Ùa-zà-ù][^.;:!?\n]{3,28}), ([^.,;:!?\n]{3,28}), "
                      r"([^.,;:!?\n]{3,28})\.")
RE_CATENA_NEG = re.compile(r"\b(n[ée] [^.;:!?\n]{2,28} n[ée] [^.;:!?\n]{2,28}"
                           r"|[Nn]iente [^.;:!?\n]{2,25}, niente [^.;:!?\n]{2,25}"
                           r"|[Ss]enza [^.;:!?\n]{2,25}, senza [^.;:!?\n]{2,25}"
                           r"|[Nn]on serve [^.;:!?\n]{2,25}, non serve )", re.I)

# Soglie del canale 4. Misurate, non scelte: vedi --taratura.
# ⚠️ Questi numeri sono MISURATI su 139 manoscritti (351.411 parole) con
# `--taratura`, non scelti a occhio e non copiati da un progetto inglese. Chi
# li cambia rifaccia quella misura: servono a tenere il falso allarme sul testo
# umano sotto un file su dieci, che è la stessa logica del p90.
ECO_FINESTRA = 150      # parole entro cui due copie dello stesso 3-gram contano
ECO_MINIMO = 4          # copie che servono perché sia un'eco e non un termine tecnico
ATTACCHI_MINIMO = 3     # frasi di fila che cominciano con la stessa parola
RITMO_CV = 0.42         # sotto questo il ritmo è piatto (umano: mediana 0,58, p10 0,51)
RITMO_FRASI = 10        # e sotto questo numero di frasi non si giudica
RIDONDANZA_J = 0.52     # Jaccard fra due frasi vicine oltre cui è una ripetizione


def _tok(t: str) -> list:
    return [w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ']{2,}", t)]


def _contenuto(frase: str) -> set:
    return {w for w in _tok(frase) if w not in STOP and len(w) >= 4}


def canale4(t: str) -> list:
    """Ritmo: le forme che si ripetono, non le parole che si ripetono."""
    esiti = []
    frasi = [f.strip() for f in re.split(r"(?<=[.!?])\s+", t) if f.strip()]

    # --- eco di frase: lo stesso 3-gram di contenuto che torna ravvicinato.
    tk = _tok(t)
    pos = {}
    for i in range(len(tk) - 2):
        g = tuple(tk[i:i + 3])
        if sum(1 for w in g if w not in STOP and len(w) >= 4) >= 2:
            pos.setdefault(g, []).append(i)
    for g, p in pos.items():
        vicine = [p[j] for j in range(len(p)) if j and p[j] - p[j - 1] <= ECO_FINESTRA]
        if len(vicine) + 1 >= ECO_MINIMO:
            esiti.append(("eco", f"«{' '.join(g)}» ×{len(p)}"))

    # --- attacchi uguali: tre frasi di fila che partono con la stessa parola.
    #     È l'anafora, che in un discorso è buona e in un paragrafo di manuale
    #     è la firma del modello che mette in fila le voci di un elenco.
    run, prima = 1, None
    for f in frasi + [""]:
        w = (re.match(r"[A-Za-zÀ-ÿ']+", f) or [""])[0].lower() if f else None
        if w and w == prima:
            run += 1
        else:
            if run >= ATTACCHI_MINIMO and prima:
                esiti.append(("attacchi", f"{run} frasi di fila attaccano con «{prima}»"))
            run, prima = 1, w

    # --- tricolon secco: tre parole sole in fila. Il tricolon con contenuto
    #     resta fuori apposta (vedi la nota in cima).
    for m in RE_TRICOLON.finditer(t):
        g = [w.lower() for w in m.groups()]
        if any(w in STOP for w in g):
            continue
        if all(CODA_AGG.search(w) for w in g):
            esiti.append(("tricolon-secco", m.group(0)))
    for m in RE_TERNA.finditer(t):
        pezzi = [p.strip() for p in m.groups()]
        # Due parole per membro al massimo: oltre, i tre membri portano
        # ciascuno una cosa diversa ed è il tricolon buono, quello di Cicerone.
        if all(len(p.split()) <= 2 for p in pezzi):
            esiti.append(("terna", m.group(0).strip()[:120]))

    # --- catena negata: «né X né Y», «niente X, niente Y». In inglese è
    #     `no-x-no-y`; in italiano prende anche la forma con «né».
    for m in RE_CATENA_NEG.finditer(t):
        esiti.append(("catena-negata", m.group(0).strip()[:120]))

    # --- coppie fisse.
    for m in re.finditer(COPPIE, t, re.I):
        esiti.append(("coppia-fissa", m.group(0)))

    # --- ridondanza: due frasi vicine che dicono la stessa cosa.
    for i in range(len(frasi) - 1):
        a, b = _contenuto(frasi[i]), _contenuto(frasi[i + 1])
        if len(a) >= 5 and len(b) >= 5:
            j = len(a & b) / len(a | b)
            if j >= RIDONDANZA_J:
                esiti.append(("ridondanza", (frasi[i] + " ‖ " + frasi[i + 1])[:150]))

    # --- sinonimia forzata: la stessa cosa chiamata in tre modi in poche righe.
    for nome, gruppo in SINONIMI.items():
        visti = {g for g in gruppo if re.search(rf"\b{g}\w{{0,3}}\b", t, re.I)}
        if len(visti) >= 3:
            esiti.append(("sinonimia", f"{nome}: {', '.join(sorted(visti))}"))

    return esiti


def ritmo(t: str) -> tuple:
    """Quanto variano le frasi. Restituisce (numero di frasi, cv, piatto?)."""
    lun = [len(_tok(f)) for f in re.split(r"(?<=[.!?])\s+", t) if len(_tok(f)) >= 3]
    if len(lun) < RITMO_FRASI:
        return len(lun), None, False
    media = sum(lun) / len(lun)
    var = sum((x - media) ** 2 for x in lun) / len(lun)
    cv = (var ** 0.5) / media if media else 0
    return len(lun), round(cv, 3), cv < RITMO_CV


# --------------------------------------------------------------------------
# CANALE 6 — DENSITÀ: quanta roba c'è dentro.
#
# Viene da «Measuring AI Slop in Text» (arXiv:2509.19163), che intervista
# redattori di mestiere e trova tre dimensioni che predicono il giudizio
# «questo è slop» meglio di tutte: *relevance*, *density*, *tone*. La densità
# e' la quantita' di sostanza rispetto alla lunghezza, e qui non si misurava.
#
# In italiano, senza librerie, la sostanza si conta dagli APPIGLI: un numero,
# una data, una percentuale, un'unita', un nome proprio, una cifra in euro,
# una citazione fra virgolette, un pezzo di codice. Un periodo che non ne ha
# nessuno e' un periodo che si sposta identico su un altro sito, che e' la
# «prova del trasloco» della skill detta con un conto.
#
# ⚠️ Le due misure dicono cose diverse e si leggono insieme. `app` e' quanti
# appigli ci sono ogni 100 parole. `vuote` e' la quota di periodi che non ne
# hanno NESSUNO, e di solito e' la piu' utile: un testo puo' avere una media
# decente perche' due paragrafi sono pieni di numeri e tutto il resto gira a
# vuoto.
#
# ⚠️ Non e' un difetto in se'. Un testo narrativo o riflessivo sta in basso ed
# e' giusto cosi'. Serve su quello che promette di informare.
APPIGLI = re.compile(
    r"\d"                                  # un numero qualunque, data e percentuale comprese
    r"|\b[A-ZÀ-Ý][a-zà-ÿ']{2,}"             # nome proprio (in mezzo alla frase: vedi sotto)
    r"|\b[A-Z]{2,}\b"                      # sigla: SEO, IVA, GGUF
    r"|[€$%]"
    r"|«[^»]{2,}»|“[^”]{2,}”"  # una citazione e' roba che qualcuno ha detto
)
# Le unita' di misura piu' comuni, che spesso arrivano senza cifra accanto.
UNITA = re.compile(r"\b(ms|kb|mb|gb|tb|km|cm|mm|kg|mq|min|sec|ore|euro|token|parole)\b", re.I)


def densita(t: str) -> tuple:
    """(appigli ogni 100 parole, quota di periodi senza nessun appiglio, periodi)."""
    frasi = [f.strip() for f in re.split(r"(?<=[.!?])\s+", t) if len(_tok(f)) >= 4]
    if len(frasi) < 5:
        return None, None, len(frasi)
    totale = vuote = parole_tot = 0
    for f in frasi:
        # ⚠️ La prima parola non conta come nome proprio: in italiano la
        # maiuscola a inizio periodo ce l'ha qualunque parola, e contarla
        # darebbe un appiglio gratis a ogni frase.
        corpo = re.sub(r"^\W*\w+", " ", f)
        n = len(APPIGLI.findall(corpo)) + len(UNITA.findall(f))
        totale += n
        vuote += (n == 0)
        parole_tot += len(_tok(f))
    return (round(totale * 100 / max(parole_tot, 1), 1),
            round(vuote * 100 / len(frasi), 1), len(frasi))


# --------------------------------------------------------------------------
# CANALE 5 — FORMA: come è impaginato, non cosa dice.
#
# Gira sul SORGENTE e non sul testo estratto, perché queste spie stanno nei tag
# e negli asterischi, che `testo()` butta via. Sono le «Style» e «Markup» di
# WP:AISIGNS, che qui non c'erano.
# --------------------------------------------------------------------------
EMOJI = re.compile("[\U0001F300-\U0001FAFF←-⇿☀-➿⬀-⯿️]")

# Soglie di forma, misurate sullo stesso corpus (p90). ⚠️ Il grassetto umano
# qui sta a 19 ogni 1000 parole di mediana: la soglia di 12 che avevo messo a
# occhio segnalava due terzi dei capitoli scritti a mano.
GRASSETTO_X1000 = 50
ETICHETTE_MINIMO = 9
STACCHI_MINIMO = 4


def canale5(src: str, percorso: str, n_parole: int, t: str = "") -> list:
    esiti = []
    md = not percorso.endswith(".html")

    # --- grassetto sparso.
    if md:
        gr = re.findall(r"\*\*[^*\n]{2,80}\*\*", src)
        eti = re.findall(r"(?m)^\s*[-*•]\s+\*\*[^*\n]{2,60}\*\*\s*[:—–-]", src)
        tit = re.findall(r"(?m)^#{1,6}\s+(.+)$", src)
        hr = len(re.findall(r"(?m)^\s*(?:---|\*\*\*|___)\s*$", src))
        voci = re.findall(r"(?m)^\s*[-*•]\s+(.+)$", src)
    else:
        gr = re.findall(r"<(?:strong|b)\b[^>]*>(.{2,80}?)</(?:strong|b)>", src, re.S)
        eti = re.findall(r"<li[^>]*>\s*<(?:strong|b)\b[^>]*>[^<]{2,60}</(?:strong|b)>\s*[:—–-]", src)
        tit = re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", src, re.S)
        hr = len(re.findall(r"<hr\b", src))
        voci = [re.sub(r"<[^>]+>", " ", v) for v in
                re.findall(r"<li[^>]*>(.*?)</li>", src, re.S)]

    if n_parole >= 200 and len(gr) * 1000 / n_parole > GRASSETTO_X1000:
        esiti.append(("grassetto", f"{len(gr)} grassetti su {n_parole} parole"))
    if len(eti) >= ETICHETTE_MINIMO:
        esiti.append(("etichetta-elenco", f"{len(eti)} voci «**Etichetta:** testo»"))
    if hr >= STACCHI_MINIMO:
        esiti.append(("linea-orizzontale", f"{hr} righe di stacco fra le sezioni"))

    for h in tit:
        h = re.sub(r"<[^>]+>", "", h).strip()
        if EMOJI.search(h):
            esiti.append(("emoji-titolo", h[:70]))
        parole_h = re.findall(r"[A-Za-zÀ-ÿ']{4,}", h)
        # Title Case: in italiano nel titolo la maiuscola va alla prima parola e
        # ai nomi propri, e basta. «Errori e Best Practice» è inglese travestito.
        #
        # ⚠️ Ma «Core Web Vitals» e «Zero-Shot Prompting» sono termini tecnici
        # inglesi, e maiuscoli stanno giusti. Il modo per distinguerli senza una
        # lista di parole: guardare se quella parola, minuscola, compare nel
        # corpo del testo. «errori» sì, «vitals» no. Una parola comune italiana
        # messa in maiuscolo nel titolo si tradisce da sé.
        if len(parole_h) >= 3 and all(w[0].isupper() for w in parole_h):
            comuni = sum(1 for w in parole_h
                         if re.search(rf"\b{re.escape(w.lower())}\b", t))
            if comuni >= 2:
                esiti.append(("titolo-inglese", h[:70]))

    if len(voci) >= 4:
        lun = [len(_tok(v)) for v in voci]
        med = sum(lun) / len(lun)
        if med >= 4 and max(lun) <= med * 1.35 and min(lun) >= med * 0.65:
            esiti.append(("elenco-uniforme",
                          f"{len(voci)} voci tutte lunghe uguale (~{med:.0f} parole)"))

    curve = len(re.findall(r"[“”‘’]", src))
    if curve >= 4:
        esiti.append(("virgolette-curve", f"{curve} virgolette curve: qui si usano « » e \" \""))
    return esiti


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

# Il genere si indovina dal percorso; --genere lo forza.
GENERE_DA_PERCORSO = [
    (r"^wiki/", "enciclopedico"),
    (r"^pubblicazioni/", "argomentativo"),
    (r"^corsi/|^academy/corsi-fonte/", "didattico"),
    (r"^(workshop|academy|calendario|scuole|corsi)/index\.html$", "promozionale"),
    (r"^index\.html$|^(de|en|es|fr|pt)/", "promozionale"),
    (r"^workshop/", "promozionale"),
    (r"^_libri/", "argomentativo"),
    (r"^_video-lezioni/", "oratorio"),
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
    return leggi(percorso)[1]


def leggi(percorso: str) -> tuple:
    """(sorgente, testo). Il canale 5 guarda il sorgente: grassetti, elenchi e
    titoli stanno nei tag, che `da_sorgente` butta via."""
    src = open(percorso, encoding="utf-8").read()
    return src, da_sorgente(src, percorso)


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
# ⚠️ Sotto questo numero di parole le densità sono rumore: 3 formule in 60
# parole fanno «50 ogni 1000», che non vuol dire niente. slopscore si astiene
# sotto le 100 parole ed è la scelta giusta: qui si conta lo stesso, ma il
# verdetto si sospende e la riga lo dice.
MINIMO_PAROLE = 120


def analizza(percorso: str, t: str, genere: str | None, src: str = "") -> dict:
    g = genere or genere_di(percorso)
    n = max(len(parole(t)), 1)
    c1, c1b, c2 = canale1(t), canale1b(t), canale2(t)
    c4 = canale4(t)
    c5 = canale5(src, percorso, n, t) if src else []
    nfrasi, cv, piatto = ritmo(t)
    app, vuote, _ = densita(t)
    dens = round(len(c1) * 10000 / n, 1)
    base, fonte = BASI.get(g, (None, ""))
    ei = round(dens / base, 2) if base else None
    formule = sum(len(v) for v in c2.values())
    corto = n < MINIMO_PAROLE

    # Cancello di corroborazione (da slopscore): una spia sola non fa un
    # verdetto. Tre canali su cinque sopra soglia sì. Serve a non mettere il
    # bollino su una pagina che ha un tricolon e basta.
    # Le soglie sono il p90 del corpus umano (vedi --taratura): un canale solo
    # sopra il p90 capita a un testo umano su dieci, tre insieme quasi mai.
    segnali = sum([
        bool(ei and ei > 1.30),
        formule * 1000 / n > 4.6,
        len(c4) * 1000 / n > 1.8,
        len(c5) >= 2,
        bool(piatto),
        # Densita': il p90 umano dei periodi senza nessun appiglio e' 78,7%.
        # Gli esempi di sbobba stanno fra 83% e 100%.
        bool(vuote is not None and vuote > 80.0),
    ])
    per_lente = {}
    for k, _ in c4:
        per_lente[k] = per_lente.get(k, 0) + 1
    return {
        "file": percorso, "genere": g, "parole": n, "corto": corto,
        "epanortosi": len(c1), "densita": dens,
        "base_umana": base, "fonte_base": fonte, "indice": ei,
        "superfici": len(c1b),
        "formule": formule, "formule_x1000": round(formule * 1000 / n, 1),
        "per_tipo": {k: len(v) for k, v in c2.items() if v},
        "ritmo": len(c4), "ritmo_x1000": round(len(c4) * 1000 / n, 1),
        "per_lente": per_lente,
        "forma": len(c5), "per_forma": {k: v for k, v in c5},
        "frasi": nfrasi, "cv": cv, "ritmo_piatto": piatto,
        "appigli_x100": app, "frasi_vuote_pct": vuote,
        "segnali": 0 if corto else segnali,
        "io": len(re.findall(IO, t, re.I)),
        "esempi_c1": c1[:12], "esempi_c1b": c1b[:12],
        "esempi_c4": c4[:14], "esempi_c5": c5[:8],
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



def confronta(prima: str, dopo: str, genere: str | None) -> int:
    """Due file o due cartelle, e cosa è cambiato in mezzo.

    ⚠️ Esce con 1 se una pagina ha PIÙ epanortosi o PIÙ formule di prima. È il
    controllo che conta dopo una revisione automatica: correggendo un difetto se
    ne scrive uno nuovo, e capita più spesso di quanto sembri.
    """
    def mappa(base):
        out = {}
        if os.path.isdir(base):
            for f in raccogli([base]):
                t = testo(f)
                if t:
                    out[os.path.relpath(f, base)] = analizza(f, t, genere)
        else:
            t = testo(base)
            if t:
                out[os.path.basename(base)] = analizza(base, t, genere)
        return out

    # Due file singoli si accoppiano fra loro anche se si chiamano diverso:
    # è il caso normale, «questo prima e questo dopo». Due cartelle invece si
    # accoppiano per nome, perché lì i file sono tanti.
    if os.path.isfile(prima) and os.path.isfile(dopo):
        ta, tb = testo(prima), testo(dopo)
        if not ta or not tb:
            print("Uno dei due file non contiene testo leggibile.")
            return 1
        a = {os.path.basename(prima): analizza(prima, ta, genere)}
        b = {os.path.basename(prima): analizza(dopo, tb, genere)}
    else:
        a, b = mappa(prima), mappa(dopo)
    comuni = sorted(set(a) & set(b))
    if not comuni:
        print("Niente da confrontare: i due lati non hanno nessun file in comune.")
        return 1

    print(f"\n{'file':44}{'epan':>12}{'formule':>13}{'io':>10}{'parole':>12}")
    peggio = []
    for k in comuni:
        x, y = a[k], b[k]
        segno = ""
        if y["epanortosi"] > x["epanortosi"] or y["formule"] > x["formule"]:
            segno = "  <-- PEGGIO"
            peggio.append(k)
        elif y["parole"] < x["parole"] * 0.88:
            segno = "  <-- accorciato oltre il 12%"
        print(f"{k[:44]:44}{x['epanortosi']:5}->{y['epanortosi']:<6}"
              f"{x['formule']:6}->{y['formule']:<6}"
              f"{x['io']:4}->{y['io']:<5}{x['parole']:6}->{y['parole']:<6}{segno}")

    def somma(m, campo):
        # ⚠️ Solo i file in comune: sommare anche quelli che stanno da una parte
        # sola fa uscire totali che non si possono confrontare.
        return sum(m[k][campo] for k in comuni)
    pa, pb = somma(a, "parole"), somma(b, "parole")
    print(f"\n  epanortosi  {somma(a, 'epanortosi')} -> {somma(b, 'epanortosi')}")
    print(f"  formule     {somma(a, 'formule')} -> {somma(b, 'formule')}")
    print(f"  io          {somma(a, 'io')} -> {somma(b, 'io')}")
    print(f"  parole      {pa} -> {pb}  ({100 * (pb - pa) / pa:+.1f}%)")
    if peggio:
        print(f"\n⚠️ {len(peggio)} file hanno più sbobba di prima: {', '.join(peggio[:6])}")
        return 1
    print("\nNessun file è peggiorato.")
    return 0


def taratura(cartella: str, genere: str | None) -> int:
    """Le soglie dei canali 4 e 5, misurate su un corpus umano.

    ⚠️ Serve a non importare dall'inglese un numero che in italiano non vale.
    slopscore fissa le sue soglie su 180 documenti pre-LLM; qui il corpus umano
    di riferimento sono i manoscritti di Federico, che è quello che il paper fa
    col canale 1 e la Tabella 1. Si legge la mediana e il 90° percentile: la
    soglia si mette al 90°, così nove testi umani su dieci restano sotto.
    """
    ris = []
    for f in raccogli([cartella]):
        try:
            src, t = leggi(f)
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        if not t:
            continue
        r = analizza(f, t, genere, src)
        if not r["corto"]:
            ris.append(r)
    if not ris:
        print("Niente da misurare.")
        return 1

    def perc(v, q):
        v = sorted(v)
        return v[min(len(v) - 1, int(q * len(v)))]

    print(f"\nCorpus umano: {len(ris)} file, {sum(r['parole'] for r in ris)} parole "
          f"({cartella})\n")
    print(f"{'misura':26}{'mediana':>10}{'p90':>10}{'max':>10}   soglia consigliata")
    for nome, campo, verso in (("formule /1000", "formule_x1000", "su"),
                               ("ritmo /1000", "ritmo_x1000", "su"),
                               ("forma (conteggio)", "forma", "su"),
                               ("frasi vuote %", "frasi_vuote_pct", "su"),
                               ("cv delle frasi", "cv", "giu"),
                               ("appigli /100", "appigli_x100", "giu")):
        v = [r[campo] for r in ris if r[campo] is not None]
        if not v:
            continue
        if verso == "su":
            print(f"{nome:26}{perc(v, .5):>10.2f}{perc(v, .9):>10.2f}{max(v):>10.2f}"
                  f"   > {perc(v, .9):.1f}")
        else:
            print(f"{nome:26}{perc(v, .5):>10.2f}{perc(v, .1):>10.2f}{min(v):>10.2f}"
                  f"   < {perc(v, .1):.2f}  (p10)")

    agg = {}
    for r in ris:
        for k, n in r["per_lente"].items():
            agg[k] = agg.get(k, 0) + n
    tp = sum(r["parole"] for r in ris)
    print("\n--- quanto scatta ogni lente sul testo umano (ogni 10.000 parole) ---")
    print("    ⚠️ È il tasso di falsi allarmi di quella lente: alto = da leggere,")
    print("       non da correggere. Stessa lettura della precisione 0,17 del paper.")
    for k, n in sorted(agg.items(), key=lambda x: -x[1]):
        print(f"{k:22}{n:5}   {n * 10000 / tp:6.1f}")
    aggf = {}
    for r in ris:
        for k in r["per_forma"]:
            aggf[k] = aggf.get(k, 0) + 1
    if aggf:
        print("\n--- forma: su quanti file dei %d scatta ---" % len(ris))
        for k, n in sorted(aggf.items(), key=lambda x: -x[1]):
            print(f"{k:22}{n:5}   {100 * n / len(ris):5.0f}%")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Misura la sbobba AI in un testo italiano.")
    ap.add_argument("percorsi", nargs="*", default=["."])
    ap.add_argument("--frasi", action="store_true", help="stampa le righe da rivedere")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--genere", choices=sorted(BASI))
    ap.add_argument("--soglia", type=float, default=0.0,
                    help="mostra solo i file oltre questo indice o queste formule per 1000")
    ap.add_argument("--max-indice", type=float, metavar="N", dest="max_indice",
                    help="esce con 1 se un file supera questo indice di epanortosi")
    ap.add_argument("--max-formule", type=float, metavar="N", dest="max_formule",
                    help="esce con 1 se un file supera queste formule ogni 1000 parole")
    ap.add_argument("--confronta", nargs=2, metavar=("PRIMA", "DOPO"),
                    help="mette a confronto due file o due cartelle e dice cosa e' cambiato")
    ap.add_argument("--taratura", metavar="CARTELLA",
                    help="misura le soglie dei canali 4 e 5 su un corpus umano "
                         "(qui: _libri/*/manoscritto) invece di importarle dall'inglese")
    a = ap.parse_args()

    # ⚠️ Il confronto e' il modo in cui questo strumento serve davvero: da solo
    # dice se un testo ha delle spie, e un numero senza un prima non vuol dire
    # granche'. Con un prima e un dopo dice se la revisione ha tolto o aggiunto,
    # ed e' l'unica domanda a cui una regex puo' rispondere bene.
    if a.confronta:
        return confronta(a.confronta[0], a.confronta[1], a.genere)
    if a.taratura:
        return taratura(a.taratura, a.genere)

    esiti, saltati = [], []
    if a.percorsi == ["-"]:
        src = sys.stdin.read()
        t = da_sorgente(src, "stdin.txt")
        esiti.append(analizza("(stdin)", t, a.genere or "argomentativo", src))
    else:
        for f in raccogli(a.percorsi):
            try:
                src, t = leggi(f)
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            if not t:
                saltati.append(f)
                continue
            esiti.append(analizza(f, t, a.genere, src))

    if a.json:
        print(json.dumps({"file": esiti, "saltati": saltati}, ensure_ascii=False, indent=1))
        return 0

    esiti.sort(key=lambda r: (-r["segnali"], -(r["indice"] or 0), -r["formule_x1000"]))
    print(f"\n{'file':40}{'genere':13}{'parole':>7}{'ind':>6}{'sup':>5}"
          f"{'form/1k':>8}{'rip/1k':>7}{'forma':>6}{'cv':>6}{'app':>6}{'vuote':>7}{'io':>4}  ")
    for r in esiti:
        if a.soglia and (r["indice"] or 0) < a.soglia and r["formule_x1000"] < a.soglia:
            continue
        ind = "—" if r["indice"] is None else f"{r['indice']:.2f}"
        cv = "—" if r["cv"] is None else f"{r['cv']:.2f}"
        # Il bollino non lo dà un canale solo: ⚠ da tre segnali in su.
        seg = "corto" if r["corto"] else ("⚠ " + "•" * r["segnali"] if r["segnali"] >= 3
                                          else "•" * r["segnali"])
        app = "—" if r["appigli_x100"] is None else f"{r['appigli_x100']:.1f}"
        vuo = "—" if r["frasi_vuote_pct"] is None else f"{r['frasi_vuote_pct']:.0f}%"
        print(f"{r['file'][-40:]:40}{r['genere']:13}{r['parole']:7}{ind:>6}{r['superfici']:5}"
              f"{r['formule_x1000']:8}{r['ritmo_x1000']:7}"
              f"{r['forma']:6}{cv:>6}{app:>6}{vuo:>7}{r['io']:4}  {seg}")

    tot = {}
    for r in esiti:
        for k, v in r["per_tipo"].items():
            tot[k] = tot.get(k, 0) + v
    print("\n--- formule per tipo ---")
    for k, v in sorted(tot.items(), key=lambda x: -x[1]):
        print(f"{k:22}{v}")
    for etichetta, campo in (("ritmo e ripetizione", "per_lente"), ("forma", "per_forma")):
        agg = {}
        for r in esiti:
            for k in r[campo]:
                agg[k] = agg.get(k, 0) + (1 if campo == "per_forma" else r[campo][k])
        if agg:
            print(f"\n--- {etichetta} ---")
            for k, v in sorted(agg.items(), key=lambda x: -x[1]):
                print(f"{k:22}{v}")
    pw = sum(r["parole"] for r in esiti)
    pe = sum(r["epanortosi"] for r in esiti)
    print(f"\nfile: {len(esiti)}   parole: {pw}   epanortosi: {pe}"
          f"   formule: {sum(tot.values())}")
    print("ind = Indice di epanortosi: densità del file diviso la base umana del genere.")
    print("      1,00 = come scrive una persona in quel genere. Sopra = correzione al rialzo di troppo.")
    print("      «—» = per quel genere una base umana pubblica non esiste (promozionale).")
    print("sup = altre superfici della stessa figura: da leggere, non da azzerare.")
    print("rip = canale 4, ritmo: echi, attacchi uguali, tricolon secchi, terne, catene")
    print("      negate, coppie fisse, ridondanze, sinonimia forzata.")
    print("forma = canale 5: grassetto sparso, elenchi a etichetta, elenchi tutti uguali,")
    print("      emoji e Title Case nei titoli, virgolette curve, righe di stacco.")
    print("cv = quanto variano le frasi. Sotto 0,42 il ritmo è piatto; il testo umano")
    print("      di riferimento sta sopra (vedi --taratura).")
    print("app = canale 6, densità: appigli ogni 100 parole (numeri, date, nomi propri,")
    print("      sigle, unità, citazioni). vuote = quota di periodi che non ne hanno")
    print("      NESSUNO, cioè che si spostano identici su un altro sito. Umano: app")
    print("      fra 6 e 10, vuote fra 49% e 66%. Gli esempi di sbobba: app sotto 4,")
    print("      vuote sopra l'83%.")
    print("⚠ = tre canali su sei sopra soglia. Un canale solo non fa un verdetto.")
    if saltati:
        print(f"⚠️ saltati (né <article> né corpo fra </nav> e <footer>): {len(saltati)}")
        for f in saltati[:8]:
            print(f"     {f}")

    sopra = []
    if a.max_indice is not None:
        sopra += [r["file"] for r in esiti if (r["indice"] or 0) > a.max_indice]
    if a.max_formule is not None:
        sopra += [r["file"] for r in esiti if r["formule_x1000"] > a.max_formule]

    if a.frasi:
        print("\n=== righe da rivedere ===")
        for r in esiti:
            if not (r["esempi_c1"] or r["esempi_c1b"] or r["esempi_c2"]
                    or r["esempi_c4"] or r["esempi_c5"]):
                continue
            print(f"\n## {r['file']}  [{r['genere']}]")
            for tipo, s in r["esempi_c1"]:
                print(f"  EPAN [{tipo}] {re.sub(chr(10), ' ', s)[:150]}")
            for tipo, s in r["esempi_c1b"]:
                print(f"  sup  [{tipo}] {re.sub(chr(10), ' ', s)[:150]}")
            for k, ss in r["esempi_c2"].items():
                for s in ss:
                    print(f"  form [{k}] …{re.sub(chr(10), ' ', s)[:130]}…")
            for tipo, s in r["esempi_c4"]:
                print(f"  rip  [{tipo}] {re.sub(chr(10), ' ', s)[:150]}")
            for tipo, s in r["esempi_c5"]:
                print(f"  forma[{tipo}] {re.sub(chr(10), ' ', s)[:150]}")
            if r["ritmo_piatto"]:
                print(f"  rip  [ritmo-piatto] {r['frasi']} frasi, cv {r['cv']}: "
                      f"lunghezze tutte uguali")

    if sopra:
        unici = sorted(set(sopra))
        print(f"\n⚠️ {len(unici)} file oltre la soglia: {', '.join(unici[:6])}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
