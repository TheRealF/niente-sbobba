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

file              genere        parole  ind  sup  form   /1k  rip  /1k forma  cv  io
esempi/sbobba.txt promozionale      90    —    1    11 122.2    0  0.0     0   —   0  corto

--- formule per tipo ---
riempitivi 1   svuotaverbi 1   permette-di 1   la-chiave 1   mondo-oggi 1
gerundio-commento 1   attribuzione-vaga 1   rinforzi 1   due-punti-a-effetto 1
schiarirsi-la-voce 1   finta-rivelazione 1

  EPAN [non…, è] Non è un corso, è
  EPAN [frase negata + affermata] Non è un corso, è un percorso di crescita. Gli
       esperti concordano: la chiave è partire dal lavoro vero.
  sup  [negazione interna + affermazione] Il futuro della formazione non sta
       arrivando. È già qui.
  form [mondo-oggi] …Nel mondo di oggi la formazione aziendale rappresenta…
```

L'altro file di prova, `esempi/sbobba-ritmo.txt`, ha il lessico più pulito e si
fa prendere dai canali nuovi: la stessa cosa chiamata in quattro modi, le coppie
fisse, i tre aggettivi in fila, la catena negata e le frasi tutte lunghe uguale.

```
$ python3 skills/niente-sbobba/sbobba.py --frasi esempi/sbobba-ritmo.txt

file                                        genere         parole   ind  sup  form   /1k  rip   /1k forma    cv  io  
esempi/sbobba-ritmo.txt                     promozionale      180     —    1    13  72.2    9  50.0     0  0.32   0  ⚠ •••
## esempi/sbobba-ritmo.txt  [promozionale]

  rip  [tricolon-secco] misurabili, verificabili e sostenibili
  rip  [catena-negata] Non serve un budget enorme, non serve
  rip  [coppia-fissa] pratico e concreto
  rip  [coppia-fissa] chiaro e diretto
  rip  [coppia-fissa] rapido ed efficace
  rip  [coppia-fissa] flessibile e scalabile
  rip  [sinonimia] percorso: cammino, percorso, viaggio
  rip  [sinonimia] strumento: risorsa, soluzione, strumento
  rip  [sinonimia] metodo: approccio, metodo, paradigma
  rip  [ritmo-piatto] 12 frasi, cv 0.322: lunghezze tutte uguali
```

`ind` è l'indice calcolato rispetto alla baseline umana per genere, `sup` le altre
superfici della figura, `form` le formule, `rip` il ritmo, `forma` l'impaginazione,
`cv` quanto variano le lunghezze delle frasi, `io` i segni della prima persona.
**Se `io` ti esce zero, il tuo testo parla come un manuale, può essere positivo o
negativo, chiaramente dipende dai casi d'uso**. `corto` vuol dire che sotto le 120
parole il verdetto si sospende: su novanta parole una densità non vuol dire niente.

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

## Cosa guarda, oltre alle parole

Le liste anti-slop guardano il **lessico**: una parola c'è o non c'è. Ma un testo
può avere il lessico pulito e suonare lo stesso di macchina, perché il difetto sta
nel disegno delle frasi. Quindi qui i canali sono cinque.

| Canale | Cosa prende |
| --- | --- |
| 1 — **epanortosi** | «non è X, è Y», e le altre superfici della stessa figura |
| 2 — **formule** | il lessico: «rappresenta», «permette di», «Ecco», i trattini lunghi `—` |
| 3 — **prima persona** | quante volte l'autore c'è. A zero il testo è un manuale |
| 4 — **ritmo** | echi, attacchi uguali, tricolon secchi, catene negate, ridondanze, sinonimia forzata, frasi tutte lunghe uguale |
| 5 — **forma** | grassetto sparso, elenchi a etichetta, elenchi tutti uguali, Title Case, emoji nei titoli, virgolette curve |

Sì: **i trattini lunghi li toglie** (canale 2), e da adesso prende anche **le
ripetizioni e le elencazioni** (canale 4), che prima gli sfuggivano.

### Due cose che ho dovuto capovolgere passando all'italiano

**La «elegant variation» va al contrario.** In inglese lo stile chiede di
ripetere la stessa parola, e i linter anti-slop segnalano chi gira i sinonimi. In
italiano la scuola insegna l'opposto, la *variatio*, e chi scrive «corso» cinque
volte di fila scrive bene lo stesso. Quindi qui un sostantivo ripetuto **non** si
segnala. Si segnala il contrario: la stessa cosa chiamata in quattro modi in
poche righe — «il percorso… il cammino… il viaggio… l'iter» — che è la forma che
la ripetizione prende in italiano, mascherata da eleganza.

**Il tricolon non è un difetto.** Tre membri che portano tre fatti diversi è
retorica buona e sta in Cicerone. La prima versione, che segnalava qualunque
terna, dava **249 falsi allarmi** sul mio corpus: prendeva «telefono, email e
partita IVA», che è un elenco di cose vere. Quello che i modelli producono in
serie è la terna di **aggettivi**, tre giudizi al posto di un fatto
(«flessibile, scalabile e affidabile»). In italiano l'aggettivo si riconosce
dalla coda (`-ato`, `-ivo`, `-bile`, `-ente`), e adesso scatta solo se ce l'hanno
tutti e tre. Da 249 a 22.

### Le soglie non le ho scelte, le ho misurate

```bash
python3 sbobba.py --taratura miei-testi/
```

Prende un corpus di roba scritta a mano — la tua — e stampa, per ogni lente,
**quanto scatta su testo umano**. Quella colonna è il tasso di falsi allarmi
della lente, e si legge come la precisione 0,17 qui sotto: una lente rumorosa dà
candidati da leggere, non errori da correggere. Le soglie di serie stanno al 90°
percentile di 139 miei capitoli, 351.411 parole, così nove testi scritti a mano
su dieci restano sotto.

Esempio di cosa ti dice, e di come mi ha fatto cambiare idea: il grassetto umano
nei miei capitoli sta a **19 ogni 1000 parole** di mediana. La soglia di 12 che
avevo messo a occhio segnalava due terzi dei capitoli che avevo scritto io.

E c'è un **cancello di corroborazione**: il `⚠` compare solo quando tre canali su
cinque stanno sopra soglia. Una spia sola non fa un verdetto.

### Da dove ho preso le idee

Il canale 4 e il canale 5 non li ho inventati. Ho guardato lo stato dell'arte
inglese e ho ritarato quello che aveva senso:
[WP:AISIGNS](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) della
squadra di pulizia di Wikipedia (la sezione *Style* e *Markup*),
[sloplint](https://github.com/benjaminjackson/sloplint) (`phrase-echo`,
`rule-of-three`, `no-x-no-y`, la dimensione *cadence*),
[slopscore](https://github.com/jman4162/slopscore) (l'astensione sotto le 100
parole, il cancello di corroborazione, i profili per genere, la pubblicazione dei
falsi positivi per regola) e [no-slop](https://github.com/Byk3y/no-slop) (le
*structural formulas*). Quello che ho aggiunto è la taratura sull'italiano e le
due inversioni qui sopra.

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
