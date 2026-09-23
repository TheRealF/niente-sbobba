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

# ------------------------------------------------------------- confronto
# Il confronto e le soglie servono a mettere il rilevatore dentro a un
# controllo automatico: senza un codice di uscita non puo' fermare niente.
import io as _io
import contextlib as _cx

def _confronta(a, b):
    buf = _io.StringIO()
    with _cx.redirect_stdout(buf):
        esito = sb.confronta(a, b, None)
    return esito, buf.getvalue()

ESEMPI = RADICE / "esempi"
codice, uscita = _confronta(str(ESEMPI / "prima-promozionale-1.txt"),
                            str(ESEMPI / "dopo-promozionale-1.txt"))
prova("confronto: due file con nomi diversi si accoppiano", "Niente da confrontare" not in uscita)
prova("confronto: una revisione buona esce con 0", codice == 0)

codice, uscita = _confronta(str(ESEMPI / "dopo-promozionale-1.txt"),
                            str(ESEMPI / "prima-promozionale-1.txt"))
prova("confronto: al contrario segnala il peggioramento", codice == 1)
prova("confronto: lo dice a schermo", "PEGGIO" in uscita)

# ---------------------------------------------------------------------------
# CANALE 4 — ritmo, ripetizione, elencazione.
# ⚠️ Ogni lente entra con un caso che DEVE scattare e uno che NON deve, perché
# qui il rischio è tutto sul secondo: queste lenti girano su forme che la prosa
# italiana usa per mestiere.
def ritmo_lenti(t):
    return {k for k, _ in sb.canale4(t)}


prova("tricolon: tre aggettivi scattano",
      "tricolon-secco" in ritmo_lenti("Una soluzione flessibile, scalabile e affidabile."))
prova("tricolon: tre NOMI non scattano (è un elenco di cose vere)",
      "tricolon-secco" not in ritmo_lenti("Lascia telefono, email e indirizzo."))
prova("tricolon: tre membri con contenuto non scattano",
      "terna" not in ritmo_lenti("Registra chi è entrato, che cosa ha aperto, "
                                 "che cosa ha modificato."))
prova("terna: tre membri secchi scattano",
      "terna" in ritmo_lenti("Il metodo. Analisi, progetto, verifica."))

prova("catena negata: «né X né Y» scatta",
      "catena-negata" in ritmo_lenti("Non serve né un budget né un team dedicato."))
prova("catena negata: «niente X, niente Y» scatta",
      "catena-negata" in ritmo_lenti("Niente fronzoli, niente giri di parole, si parte."))

prova("sinonimia: tre nomi per la stessa cosa scattano",
      "sinonimia" in ritmo_lenti("Il percorso è un cammino lungo. Questo viaggio "
                                 "si fa in tre tappe."))
prova("sinonimia: due nomi soli non scattano",
      "sinonimia" not in ritmo_lenti("Il percorso è un cammino lungo, e si fa in tre tappe."))
prova("variatio: lo stesso nome ripetuto NON è un difetto in italiano",
      ritmo_lenti("Il corso dura sei mesi. Il corso costa 890 euro. "
                  "Il corso si fa la sera.") <= {"attacchi"})

prova("coppia fissa: «rapido ed efficace» scatta",
      "coppia-fissa" in ritmo_lenti("Un metodo rapido ed efficace."))

prova("attacchi: tre frasi con lo stesso attacco scattano",
      "attacchi" in ritmo_lenti("Serve un metodo. Serve un obiettivo. Serve tempo."))
prova("attacchi: due sole non scattano",
      "attacchi" not in ritmo_lenti("Serve un metodo. Serve un obiettivo. Poi si parte."))

prova("ridondanza: due frasi che dicono la stessa cosa scattano",
      "ridondanza" in ritmo_lenti(
          "L'adozione dell'intelligenza artificiale riduce i tempi della revisione "
          "aziendale. La revisione aziendale riduce i tempi grazie all'adozione "
          "dell'intelligenza artificiale."))

# ritmo piatto: quindici frasi tutte da undici parole contro quindici frasi vere.
piatto = " ".join(["Il metodo prevede una analisi iniziale seguita da una verifica finale."] * 3
                  + ["Ogni fase richiede una misura precisa seguita da una prova sul campo."] * 3
                  + ["La squadra raccoglie i dati oppure li confronta con quelli passati."] * 3
                  + ["Il cliente riceve un documento oppure una scheda con i numeri."] * 3)
_, cv_piatto, flag = sb.ritmo(piatto)
prova("ritmo: frasi tutte uguali danno cv basso", flag is True)
vario = ("Basta. Il metodo prevede una analisi iniziale, una verifica intermedia e una "
         "prova sul campo che dura tre settimane e coinvolge due persone. Poi si guarda. "
         "Se i numeri non tornano si rifà tutto da capo, con calma, partendo dal punto "
         "in cui si era rotto qualcosa. Capita. Non sempre, ma capita, e quando capita "
         "conviene fermarsi invece di tirare dritto. Si riparte il lunedì dopo.")
_, cv_vario, flag_v = sb.ritmo(vario)
prova("ritmo: frasi di lunghezza varia non scattano", flag_v is False)

# CANALE 5 — forma.
def forma_lenti(src, t="", n=500):
    return {k for k, _ in sb.canale5(src, "x.md", n, t)}


prova("Title Case italiano scatta",
      "titolo-inglese" in forma_lenti("# Aspetti Etici e Legali\n\nGli aspetti "
                                      "etici sono tanti, quelli legali pure.",
                                      "gli aspetti etici sono tanti quelli legali pure"))
# ⚠️ «Errori e Best Practice» NON scatta, ed è giusto: due parole su tre sono un
# termine inglese, e il rilevatore non ha come saperlo con sicurezza. Meglio
# perderne uno che segnalare «Core Web Vitals».
prova("termine tecnico inglese in maiuscolo NON scatta",
      "titolo-inglese" not in forma_lenti("# Core Web Vitals\n\nSono tre misure.",
                                          "sono tre misure"))
prova("grassetto nella norma umana non scatta",
      "grassetto" not in forma_lenti("**uno** e **due** testo", "", 500))
prova("elenco con voci tutte uguali scatta",
      "elenco-uniforme" in forma_lenti(
          "- La prima voce dice una cosa chiara\n"
          "- La seconda voce dice altro chiaro\n"
          "- La terza voce dice ancora altro\n"
          "- La quarta voce chiude il discorso\n"))

# Corroborazione e astensione.
r = sb.analizza("x.md", "Testo cortissimo e fondamentale.", "argomentativo", "")
prova("astensione: sotto 120 parole il verdetto si sospende", r["corto"] and r["segnali"] == 0)

# ------------------------------------------------- superfici aggiunte dopo

def superfici(x):
    return {k for k, _ in sb.canale1b(x)}


prova("«invece di» e una superficie dell'epanortosi, e mancava",
      "invece-di" in superfici("Legge la risposta invece di generarla."))
prova("«invece di» scatta anche sull'uso normale: e un candidato, non un errore",
      "invece-di" in superfici("Vado a piedi invece di prendere l'auto."))
prova("l'ordine rovesciato, affermo e poi nego",
      "afferma-poi-nega" in superfici("E un percorso, non un corso.".replace("E ", "\u00c8 ")))
prova("una distinzione vera non scatta",
      "afferma-poi-nega" not in superfici("\u00c8 un corso di Excel, non di Word."))
prova("un fatto qualunque non scatta",
      superfici("Ho comprato il pane, non il latte.") == set())
prova("piuttosto che", "piuttosto-che" in superfici("Piuttosto che aspettare, ho scritto."))
prova("tutt'altro che", "tutt-altro" in superfici("Il risultato \u00e8 tutt'altro che scontato."))

# ------------------------------------------------------------- densita'

def dens(x):
    return sb.densita(x)


_PIENO = ("Il deploy \u00e8 passato da 40 minuti a 4. La revisione la fa Marta il gioved\u00ec. "
          "Il file pesa 2,5 GB e sta su GitHub. Costa 890 euro, in tre rate. "
          "A Livorno il corso parte il 6 ottobre. Le prove sono 85 e girano in 0,2 s.")
_VUOTO = ("La soluzione rappresenta una svolta importante per il settore. "
          "Permette di ottimizzare i processi in modo efficace. "
          "Il valore aggiunto si vede fin da subito. "
          "L'approccio garantisce risultati concreti nel tempo. "
          "La qualit\u00e0 resta sempre al centro del lavoro. "
          "Ogni fase viene curata con grande attenzione.")

app_pieno, vuote_pieno, _ = dens(_PIENO)
app_vuoto, vuote_vuoto, _ = dens(_VUOTO)
prova("densita: il testo con numeri e nomi ha piu' appigli", app_pieno > app_vuoto)
prova("densita: il testo che gira a vuoto ha quasi tutti i periodi senza appigli",
      vuote_vuoto >= 80 and vuote_pieno <= 40)
prova("densita: sotto cinque periodi non si giudica", dens("Una frase. Due.")[0] is None)
prova("densita: la maiuscola a inizio periodo non vale come appiglio",
      dens("Questo testo gira a vuoto in ogni sua parte. "
           "Quello che conta resta sempre lo stesso. "
           "Ogni parola qui dentro non dice niente. "
           "Niente numeri e niente nomi in queste righe. "
           "Sempre la stessa aria fritta per tutti. "
           "Alla fine non resta proprio nulla.")[1] == 100.0)
prova("densita: entra nel conto dei segnali",
      sb.analizza("x.md", _VUOTO * 3, "argomentativo", "")["segnali"] >= 1)

# ---------------------------------------------------------------------------
falliti = [n for n, ok in esiti if not ok]
print(f"\n{len(esiti) - len(falliti)}/{len(esiti)} casi a posto")
for n in falliti:
    print(f"  FALLITO  {n}")
sys.exit(1 if falliti else 0)

