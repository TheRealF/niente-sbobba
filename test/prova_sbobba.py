#!/usr/bin/env python3
"""I casi che sbobba.py deve prendere, e quelli che deve lasciare stare.

Si lancia dalla radice del repository, senza installare niente:

    python3 test/prova_sbobba.py

Esce con 1 se un caso non torna. Ogni caso qui dentro viene da un testo vero:
i falsi positivi sono quelli trovati passando lo strumento su 209 pagine di un
sito pubblicato, e i limiti noti sono quelli che il paper dichiara.

⚠️ **Regola per chi aggiunge una formula**: una voce nuova entra con almeno un
caso che deve scattare E un caso che NON deve scattare. Una lista di divieti
senza eccezioni produce testi storti, ed è il modo più veloce per far smettere
alla gente di guardare il rilevatore.
"""
import importlib.util
import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "sbobba", RADICE / "skills" / "niente-sbobba" / "sbobba.py")
sb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sb)

esiti = []


def prova(nome, ok):
    esiti.append((nome, ok))


def formule(t):
    return {k for k, v in sb.canale2(t).items() if v}


def epan(t):
    return len(sb.canale1(t))


def superfici(t):
    return {k for k, _ in sb.canale1b(t)}


# ---------------------------------------------------------------- epanortosi
# I quattro pattern del paper (§7.8). Se uno di questi smette di scattare, la
# misura non coincide più con quella pubblicata.
PRENDE_EPAN = [
    ("non...ma", "Non è un problema di soldi, ma di tempo."),
    ("non solo...ma", "Non solo veloce, ma anche preciso."),
    ("non..., è", "Non è pigrizia, è metodo."),
    ("frase negata + affermata", "Non è un corso. È un percorso."),
]
for nome, t in PRENDE_EPAN:
    prova(f"epanortosi «{nome}»", epan(t) >= 1)

# Modi di dire che contengono «non» e non sono la figura.
LASCIA_EPAN = [
    "Non appena arriva il file, lo controlliamo.",
    "Il corso non costa niente e dura tre ore.",
]
for t in LASCIA_EPAN:
    prova(f"non è epanortosi: {t[:38]}…", epan(t) == 0)

# ⚠️ SOVRA-SCATTO NOTO del pattern del paper: «non che…, è» è un modo di dire,
# e RE_NONVIRG lo prende comunque. IDIT lo esclude solo da RE_NONMA. Resta così,
# perché il pattern è copiato verbatim e cambiarlo scollegherebbe la misura da
# quella pubblicata. È uno dei motivi per cui la precisione sul testo umano è 0,17.
prova("sovra-scatto noto: «non che…, è»", epan("Non che sia sbagliato, è solo lungo.") == 1)

# ⚠️ IL BUCO PIÙ CURIOSO, e vale la pena saperlo: «Questo non è un corso. È un
# percorso.» è LO SPECIMEN dell'abstract del paper, e il pattern del paper NON lo
# vede. In NEG c'è `questa? non è`, che copre «quest» e «questa» ma non «questo»:
# il dimostrativo femminile passa, il maschile no. Il canale delle altre
# superfici lo prende, ed è per questo che quel canale esiste.
SPECIMEN = "Questo non è un corso. È un percorso."
prova("lo specimen del paper sfugge al canale del paper", epan(SPECIMEN) == 0)
prova("lo specimen del paper lo prende il secondo canale",
      "negazione interna + affermazione" in superfici(SPECIMEN))
prova("il femminile invece il paper lo prende",
      epan("Questa non è una scuola. È una comunità.") == 1)

# ⚠️ LIMITI NOTI, e sono dichiarati nel paper: recall 0,52, il canale lessicale
# copre la famiglia «non… ma». Queste QUATTRO sono epanortosi vere che la regex
# NON vede, trovate leggendo dodici testi generati. Il test le blocca così come
# sono: se un giorno una di queste comincia a scattare, il README va aggiornato
# perché smette di essere vero.
LIMITI_NOTI = [
    "Il valore vero non sta nel codice: sta nel capire come lavora un'azienda.",
    "Non serve nessuna esperienza precedente, serve voglia di guardare le cose.",
    "Non inseguiamo lo stile del momento: cerchiamo edifici che durino.",
    "Una biblioteca non si misura dal numero dei libri. Si misura da quante persone entrano.",
]
for t in LIMITI_NOTI:
    prova(f"limite noto (la regex non la vede): {t[:34]}…", epan(t) == 0)

# ------------------------------------------------------------------ superfici
PRENDE_SUP = [
    ("più-che", "Più che un corso, un percorso di crescita."),
    ("o-meglio", "È un assistente, o meglio un collaboratore."),
    ("definirlo-riduttivo", "Definirlo un gestionale è riduttivo."),
    ("non-tanto", "Non tanto la velocità quanto la precisione."),
]
for nome, t in PRENDE_SUP:
    prova(f"superficie «{nome}»", nome in superfici(t))

# ------------------------------------------------------------------- formule
PRENDE_FORM = [
    ("svuotaverbi", "L'integrazione rappresenta una svolta."),
    ("riempitivi", "Un backup è fondamentale."),
    ("permette-di", "Il sistema permette di ridurre i tempi."),
    ("ecco", "Il dato è chiaro. Ecco perché conviene."),
    ("la-chiave", "La chiave è iniziare."),
    ("mondo-oggi", "Nel mondo di oggi tutto corre."),
    ("meta-guida", "In questa guida vedremo come si fa."),
    ("gerundio-commento", "Aggiunge due lezioni, dimostrando l'attenzione al tema."),
    ("puffery", "L'apertura segna una svolta per l'azienda."),
    ("attribuzione-vaga", "Gli esperti concordano sul punto."),
    ("rinforzi", "È semplicemente perfetto."),
    ("anglicismi", "Seguiamo le best practice del settore."),
    ("marketing", "Un approccio rivoluzionario al problema."),
    ("domanda-retorica", "Il punto è chiaro. E se ti dicessi che sbagli?"),
    ("due-punti-a-effetto", "La parte migliore: impara da sola."),
    ("frammento", "Funziona. Tutto qui."),
    ("trattino-lungo", "Il corso — tre ore — costa poco."),
    ("schiarirsi-la-voce", "Diciamocelo: il problema sono i dati."),
    ("finta-rivelazione", "Quello che nessuno ti dice è che serve tempo."),
    ("elenco-negato", "Non è un corso. Non è un webinar. È un percorso."),
    ("guida-al-lettore", "Il numero sale. Come puoi vedere, il tema conta."),
    ("apostrofe", "Il conto torna. Fidati, funziona così."),
]
for nome, t in PRENDE_FORM:
    prova(f"formula «{nome}»", nome in formule(t))

# I falsi positivi che la REGEX evita da sé, perché li ho stretti dopo averli
# visti su 209 pagine vere.
LASCIA_FORM = [
    ("«Attenzione:» come etichetta di un riquadro",
     "Il totale non torna. Attenzione: la pivot non si aggiorna da sola.", "apostrofe"),
    ("elenco di errori da evitare",
     "Errori comuni. Non ottimizzare per mobile. Non testare le performance.", "elenco-negato"),
]
for nome, t, famiglia in LASCIA_FORM:
    prova(f"falso positivo evitato dalla regex: {nome}", famiglia not in formule(t))

# ⚠️ I falsi positivi che la regex NON può evitare, perché la differenza è di
# significato e non di forma. Il rilevatore li segnala, e la skill dice di
# lasciarli stare. Il test controlla tutte e due le cose: che la spia scatti
# (così chi legge il rapporto sa che è un candidato) e che l'eccezione sia
# scritta in formule.md, dove il modello la legge.
FORMULE_MD = (RADICE / "skills" / "niente-sbobba" / "riferimenti" / "formule.md").read_text(encoding="utf-8")
DA_GIUDICARE = [
    ("rappresentare tecnico", "Un embedding rappresenta una parola come un vettore.",
     "svuotaverbi", "un embedding rappresenta una"),
    ("diritti fondamentali", "Usi incompatibili con i diritti fondamentali della Carta.",
     "riempitivi", "diritti fondamentali"),
    ("differenza significativa", "La differenza è significativa, con p uguale a 0,03.",
     "riempitivi", "differenza significativa"),
]
for nome, t, famiglia, eccezione in DA_GIUDICARE:
    prova(f"da giudicare, la spia scatta: {nome}", famiglia in formule(t))
    prova(f"da giudicare, l'eccezione è scritta: {nome}", eccezione in FORMULE_MD)

# ------------------------------------------------------------- calibrazione
# L'indice è la densità diviso la base umana del genere. Un testo promozionale
# non ha una base umana pubblica, e lo strumento lo dice invece di inventarla.
r = sb.analizza("x.txt", "Non è un corso, è un percorso. " * 10, "promozionale")
prova("promozionale: nessun indice inventato", r["indice"] is None)
prova("promozionale: base dichiarata assente", r["base_umana"] is None)

r = sb.analizza("x.txt", "Non è un corso, è un percorso. " * 10, "enciclopedico")
prova("enciclopedico: indice calcolato", r["indice"] is not None and r["indice"] > 1)
prova("enciclopedico: base 1,2 come nel paper", r["base_umana"] == 1.2)

for genere, base in (("argomentativo", 12.0), ("oratorio", 14.0),
                     ("giornalistico", 2.4), ("narrativo", 7.5),
                     ("conversazionale", 8.2), ("accademico", 3.6)):
    prova(f"base «{genere}» = {base} (Tabella 1 / §7.8)", sb.BASI[genere][0] == base)

# ------------------------------------------------------------------- lettura
prova("legge il markdown", bool(sb.da_sorgente("# Titolo\n\nUn testo.", "a.md")))
prova("legge l'html dentro <article>",
      "dentro" in (sb.da_sorgente("<html><article><p>dentro</p></article></html>", "a.html") or ""))
prova("l'html salta il codice",
      "print" not in (sb.da_sorgente(
          "<article><p>testo</p><pre>print(1)</pre></article>", "a.html") or ""))

# ---------------------------------------------------------------------------
falliti = [n for n, ok in esiti if not ok]
print(f"\n{len(esiti) - len(falliti)}/{len(esiti)} casi a posto")
for n in falliti:
    print(f"  FALLITO  {n}")
sys.exit(1 if falliti else 0)
