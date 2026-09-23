# Ritmo, ripetizione, elencazione

Il canale 4 di `sbobba.py`. I canali 1 e 2 guardano **parole**: una stringa c'è
o non c'è. Questo guarda la **forma di un paragrafo**, che è dove un testo
generato si riconosce anche quando il lessico è pulito. È il pezzo che mancava:
si poteva togliere «rappresenta» da ogni riga e avere ancora un testo che suona
di macchina, perché il difetto stava nel disegno delle frasi.

Le lenti vengono dallo stato dell'arte inglese e sono **ritarate sull'italiano**:
`phrase-echo`, `rule-of-three`, `no-x-no-y` e la dimensione *cadence* di
[sloplint](https://github.com/benjaminjackson/sloplint), le dimensioni
*redundancy* e *cadence* di [slopscore](https://github.com/jman4162/slopscore),
le *structural formulas* di [no-slop](https://github.com/Byk3y/no-slop) e di
[WP:AISIGNS](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

⚠️ **Le soglie non sono importate: sono misurate.** 139 manoscritti di Federico,
351.411 parole, con `sbobba.py --taratura _libri`. Ogni soglia sta al 90°
percentile del corpus umano, così nove testi scritti a mano su dieci restano
sotto. È la stessa logica per cui il canale 1 prende la base dal paper invece
che da un'opinione. Chi cambia una soglia rifà quella misura.

---

## Due cose che cambiano passando all'italiano

### 1. «Elegant variation» va capovolta

In inglese lo stile chiede di **ripetere** la stessa parola, e chi la cambia a
ogni riga commette un errore: per questo `no-slop` ha la regola *elegant
variation*, che segnala chi gira i sinonimi. In italiano la scuola insegna
l'esatto contrario, la **variatio**, e chi scrive «corso» cinque volte di fila
scrive bene lo stesso.

Quindi qui **un sostantivo ripetuto non si segnala**. Si segnala il contrario:
la lente `sinonimia`, la stessa cosa chiamata in quattro modi in poche righe.

> Il **percorso** verso l'adozione è un **cammino** che richiede metodo. Questo
> **viaggio** si articola in tre fasi, e l'**iter** completo dura sei mesi.

**Cura.** Scegli il nome e tienilo. «Il percorso dura sei mesi e si fa in tre
fasi.» Se due nomi diversi servono davvero, è perché sono due cose diverse: e
allora si dice qual è la differenza.

### 2. Il tricolon non è un difetto

Tre membri che portano ciascuno un fatto diverso è retorica buona, e sta in
Cicerone. La prima taratura, che segnalava qualunque terna, dava **249
segnalazioni sul corpus umano**: prendeva «telefono, email e partita IVA», che è
un elenco di cose vere.

Quello che i modelli producono in serie è la terna di **aggettivi**: tre giudizi
al posto di un fatto. In italiano l'aggettivo si riconosce dalla coda (`-ato`,
`-ivo`, `-bile`, `-ente`, `-oso`, `-ale`), e `tricolon-secco` scatta solo quando
**tutti e tre** i membri ce l'hanno. Dopo la correzione: 22 segnalazioni, undici
volte meno.

> Una soluzione **flessibile, scalabile e affidabile**.

**Cura.** Tieni quello che porta un fatto e butta gli altri due, poi dì il fatto:
«Regge 500 utenti in contemporanea.»

---

## Le lenti, una per una

| lente | cosa prende | falsi allarmi (umano, ogni 10.000 parole) |
| --- | --- | --- |
| `eco` | lo stesso 3-gram di contenuto ≥4 volte in 150 parole | 2,3 |
| `terna` | tre membri di ≤2 parole, asindetici: «X, Y, Z.» | 2,7 |
| `attacchi` | ≥3 frasi di fila che attaccano con la stessa parola | 1,5 |
| `tricolon-secco` | tre aggettivi in fila | 0,6 |
| `catena-negata` | «né X né Y», «niente X, niente Y», «senza X, senza Y» | 0,4 |
| `coppia-fissa` | «semplice e intuitivo», «rapido ed efficace» | 0,1 |
| `ridondanza` | due frasi vicine che dicono la stessa cosa (Jaccard ≥ 0,52) | 0,2 |
| `sinonimia` | la stessa cosa con tre nomi diversi | 0,2 |
| `ritmo-piatto` | frasi tutte lunghe uguale (cv < 0,42) | umano: mediana 0,58 |

⚠️ La colonna dei falsi allarmi è la cosa più utile della tabella, ed è la
stessa lettura della precisione 0,17 del paper: una lente che scatta spesso sul
testo umano dà **candidati da leggere**, non errori da correggere. `eco` e
`terna` stanno in cima, quindi si guardano prima di toccarli.

### Il ritmo piatto

> L'AI permette di ottimizzare i processi. L'adozione richiede un metodo chiaro.
> Il percorso si articola in tre fasi. Ogni fase ha un obiettivo misurabile.

Quattro frasi, tutte fra le dieci e le tredici parole, tutte soggetto-verbo-
complemento. Nessuna regola è violata e il paragrafo è morto. Il corpus umano ha
un coefficiente di variazione mediano di **0,58**: le frasi vere sono lunghe e
corte a caso, perché seguono quello che c'è da dire.

**Cura.** Non allungare né accorciare a caso: **unisci due frasi che parlano
della stessa cosa e spezza quella che porta il punto**. La frase corta va dove
serve il colpo. Se un paragrafo resta piatto, spesso è perché non ha niente da
dire e il rimedio è tagliarlo.

### Gli attacchi uguali

Tre frasi di fila che cominciano con la stessa parola. In un discorso è
l'anafora e funziona; in un paragrafo di manuale è il modello che ha messo in
riga le voci di un elenco fingendo di fare prosa.

**Cura.** Se è un elenco, scrivilo come elenco. Se è prosa, cambia l'attacco di
due frasi su tre.

---

## Canale 5 — la forma

Gira sul **sorgente** e non sul testo estratto, perché queste spie stanno nei
tag e negli asterischi. Sono le sezioni *Style* e *Markup* di WP:AISIGNS.

| lente | soglia (p90 umano) | nota |
| --- | --- | --- |
| `grassetto` | > 50 ogni 1000 parole | ⚠️ il grassetto umano qui sta a **19 di mediana**: la soglia di 12 che avevo messo a occhio segnalava due terzi dei capitoli scritti a mano |
| `etichetta-elenco` | ≥ 9 voci «**Etichetta:** testo» | l'*inline-header vertical list* |
| `elenco-uniforme` | ≥ 4 voci tutte lunghe uguale (±35%) | un elenco vero ha voci di lunghezza diversa |
| `titolo-inglese` | Title Case su parole italiane | vedi sotto |
| `emoji-titolo` | una emoji in un titolo | |
| `virgolette-curve` | ≥ 4 | qui si usano « » e " " |
| `linea-orizzontale` | ≥ 4 stacchi | |

### Title Case: come si distingue dall'inglese tecnico

«Errori e Best Practice» è Title Case all'inglese su parole italiane, e in
italiano nel titolo la maiuscola va alla prima parola e ai nomi propri. Ma «Core
Web Vitals» e «Zero-Shot Prompting» sono termini tecnici inglesi, e maiuscoli
stanno giusti.

Il modo per distinguerli senza tenere una lista di parole: **guardare se quella
parola, minuscola, compare nel corpo del testo**. «errori» sì, «vitals» no. Una
parola comune italiana messa in maiuscolo nel titolo si tradisce da sé. Sul sito
questo ha portato le segnalazioni da 102 a 60, e le 60 che restano sono vere.

---

## Il cancello di corroborazione

Da slopscore. Una spia sola non fa un verdetto: il **⚠** compare quando **tre
canali su cinque** stanno sopra il p90 umano. Serve a non mettere il bollino su
una pagina che ha un tricolon e basta.

E sotto le **120 parole** il verdetto si sospende del tutto (la riga dice
`corto`): tre formule in sessanta parole fanno «50 ogni 1000», che non vuol dire
niente.
