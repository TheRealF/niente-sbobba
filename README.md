<p align="center">
  <img src="assets/niente-sbobba.png" alt="niente sbobba" width="760">
</p>

# Niente sbobba

BASTA SBOBBA INUTILE!

Niente sbobba toglie da un testo italiano le formule che lo fanno percepire come
generato da una AI. In gergo inglese si parla di AI slop. Quindi questa repo
contiene un anti-slop italiano. Ho voluto tradurre slop come sbobba, quindi
niente più sbobba per te amico dell'internet!

## Il problema

Le liste anti-slop che girano sono inglesi. *Delve*, *tapestry*, *leverage*,
*it's not X, it's Y*. In italiano l'effetto sbobba
lo fanno altre costruzioni; un esempio è il **verbo svuotato**:

> L'integrazione **rappresenta** una svolta **fondamentale** e **permette di**
> ridurre i tempi, **dimostrando** l'attenzione all'innovazione.

Tanti giri di parole, ma ci è stato comunicato poco o nulla.

Il punto che rende difficile riconoscere la sbobba artificiale è che non suona male. Per questo ti finisce dentro al
testo senza che te ne accorga e rischi di finire come la maggior parte delle persone a scrivere e parlare come una macchina (boia deh!)

## Come si usa (daje usala)

```bash
npx skills add TheRealF/niente-sbobba --skill niente-sbobba --global --yes
```

Oppure incolla nel tuo agente: `Installa la skill /niente-sbobba da
https://github.com/TheRealF/niente-sbobba`

Poi:

| Comando | Cosa fa |
| --- | --- |
| `/niente-sbobba (testo)` | te lo revisiona e ti dice cosa ha cambiato |
| `/niente-sbobba è sbobba questo? (testo)` | nomina le formulazioni sbobbose e ti indica la posizione e il tipo di sbobba artificiale rilevata|
| `python3 sbobba.py --frasi testo.md` | solo la misura |

Nel repo c'è un file di prova per capire come usarlo

```
$ python3 skills/niente-sbobba/sbobba.py --frasi esempi/sbobba.txt

file                 genere        parole epan   /10k  ind  sup  form   /1k  io
esempi/sbobba.txt    promozionale      90    2  222.2    —    1    11 122.2   0

--- formule per tipo ---
riempitivi 1   svuotaverbi 1   permette-di 1   la-chiave 1   mondo-oggi 1
gerundio-commento 1   attribuzione-vaga 1   rinforzi 1   due-punti-a-effetto 1
schiarirsi-la-voce 1   finta-rivelazione 1

  EPAN [non…, è] Non è un corso, è
  EPAN [frase negata + affermata] Non è un corso, è un percorso di crescita. Gli
       esperti concordano: la chiave è partire dal lavoro vero.
```

`ind` è l'indice calcolato rispetto alla baseline umana per genere, `sup` le altre superfici della
figura, `form` le formule, `io` i segni della prima persona. **Se `io` ti esce
zero, il tuo testo parla come un manuale, può essere positivo o negativo, chiaramente dipende dai casi d'uso**.

Niente sbobba gira su `.html`, `.md`, `.txt` e da standard input, ed è Python 3 senza
dipendenze.

### Confrontare un prima e un dopo

Con la funzionalità confronta vedi il prima e il dopo e capisci se la revisione ha
tolto o ha aggiunto. 

```bash
python3 sbobba.py --confronta bozza.md rivisto.md
python3 sbobba.py --confronta sito-vecchio/ sito-nuovo/
```

Ti restituisce 1 se una pagina ha **più** sbobba di prima. Può succedere. Correggendo
un difetto se ne scrive uno nuovo.

### Dentro a un controllo automatico

```bash
python3 sbobba.py --max-formule 3 --max-indice 1.5 testi/
```

Esce con 1 se un file supera le soglie. Così puoi fermare una pubblicazione.
Su GitHub c'è l'azione già pronta:

```yaml
- uses: TheRealF/niente-sbobba@main
  with:
    percorsi: docs/
    max-formule: '3'
```

### Anche fuori da Claude

Le istruzioni sono Markdown, quindi niente sbobba gira con qualunque modello e dentro a
qualunque strumento.

| Dove | Come |
| --- | --- |
| Claude Code | `npx skills add …`, poi `/niente-sbobba` |
| Codex, Cursor, e chi legge `AGENTS.md` | clona il repo: il file in radice punta già alle istruzioni |
| ChatGPT, Gemini, altri | carica `SKILL.md` e i tre file di `riferimenti/` in un progetto |
| Senza nessun modello | `python3 sbobba.py --frasi testo.md` |

## Come decido quanto togliere

Con pesi e misure, che ho preso dal mio paper
**[Artificial Epanorthosis](https://arxiv.org/abs/2607.21498)**.

La figura più riconoscibile della sbobba è l'epanortosi. «Non è un corso, è un
percorso». L'ho misurata per genere. I modelli la mettono al **doppio** del tasso
umano in un discorso. In una chiacchierata scendono a **un quinto**.

Poi ho provato a spegnerla del tutto, con un adapter addestrato apposta. Il testo
è finito **sotto** il tasso umano. Zero correzioni suona finto quanto il doppio.

Quindi non te la tolgo tutta. Te la riporto al tasso di chi scrive quel genere.
Questi sono i numeri che uso.

| Genere | Umani | Modelli |
| --- | --- | --- |
| Enciclopedico | 1,2 | 1,4 |
| Giornalistico | 2,4 | 2,0 |
| Narrativo | 7,5 | 4,1 |
| Domanda e risposta | 8,2 | **1,3** |
| Argomentativo (IT) | ~12 | **56,9** |
| Oratorio (IT) | ~14 | **39,6** |

Occorrenze ogni 10.000 parole. Per il promozionale una base umana non ce l'ha
nessuno. Lo strumento te lo dice invece di inventarsela.

## Quanto ti puoi fidare del rilevatore

Poco, e lo dico io che l'ho scritto. Ho fatto scrivere dodici testi italiani a
dei modelli, senza dirgli cosa stavo misurando. La regex ci ha trovato **zero**
epanortosi. Io leggendoli ne ho trovate **quattro**. Tipo questa:

> «Non serve nessuna esperienza precedente, serve voglia di guardare le cose.»

Gli sfugge perché il verbo è «serve» invece di «è». Nel paper l'avevo già
scritto: quel canale ha recall 0,52, e sul testo scritto da una persona la
precisione scende a 0,17.

La skill invece le ha trovate tutte e quattro, perché a leggerla è un modello.

⚠️ **Occhio allo zero.** Vuol dire che il rilevatore non ha trovato la forma che
sa cercare. Del resto del tuo testo non sa niente.

## Quello che non fa

Se un testo l'ha scritto una AI, questa skill non te lo dice. Chi te lo promette
tira a indovinare. Io preferisco nominarti la formula e citarti la riga, poi
controlli te. In inglese non ci provo nemmeno, per quello c'è già
[no-ai-slop](https://github.com/petergyang/no-ai-slop). Refusi, accordi e virgole
li lascia dove stanno.

Il limite grosso però è un altro. Le formule te le toglie. Le cose da dire ce le
devi mettere te. Su un testo che non ha niente da dire ti restituisce un testo
pulito che non ha niente da dire.

## Una cosa da fare prima di usarla

⚠️ **Riempi `riferimenti/voce.md`.** Scrivi chi parla. Tono di voce, stile, esempi. Inserisci frasi che hai scritto di tuo pugno, dai riferimenti alla skill.

Senza quel file ti toglie le formule e ti restituisce una prosa corretta e di
nessuno. È il secondo modo di suonare artificiale.

Gli altri file. `SKILL.md` ha le regole. `eval.md` i controlli che la skill fa
sul proprio lavoro. `sbobba.py` è il rilevatore. `riferimenti/epanortosi.md`
spiega la figura e i suoi limiti, `riferimenti/formule.md` il lessico con le
eccezioni. I casi di prova stanno in `test/`, sono 65 e girano a ogni push.

## Crediti

L'idea di impacchettare tutto questo come skill viene da
**[no-ai-slop](https://github.com/petergyang/no-ai-slop)** di Peter Yang. Lui fa
la stessa cosa per l'inglese. Qui il lessico è italiano, e il criterio viene dal
paper.

La ricerca è mia. **Federico Boggia** (aka TheRealF aka io), *Artificial
Epanorthosis*, arXiv:2607.21498. I pattern del canale principale li ho copiati
verbatim dal mio script di valutazione. Quello che misuri qui è quello che ho
pubblicato là.

## Licenza

MIT.
