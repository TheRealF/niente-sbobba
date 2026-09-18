# L'epanortosi, e quanta ne regge un testo

Fonte: Federico Boggia, *Artificial Epanorthosis* (arXiv:2607.21498), più
l'articolo divulgativo `pubblicazioni/epanortosi-artificiale.html`.

## Cos'è

Chi scrive afferma una cosa e subito la rivede, lasciando visibile quello che ha
rivisto. La prima versione resta nel testo e fa parte del messaggio.

> Eppure vive. Vive? Anzi, viene addirittura in senato.
> — Cicerone, *In Catilinam* I, 2

Funziona perché mette in scena un pensiero che si muove: chi legge assiste a una
revisione in diretta, e ne ricava un effetto di sincerità. Nel parlato la usiamo
tutti, ogni «cioè», «anzi», «o meglio» è uno di questi.

La revisione va in due direzioni: al rialzo, quando la seconda parola è più forte
(«è buono, anzi eccellente»), e al ribasso, quando attenua («è un disastro,
cioè… un imprevisto»). Quella che i modelli producono in eccesso è la prima.

## Perché i modelli ne fanno troppa

Due cause, in ordine di peso.

1. **I dati.** Nel testo raccolto dal web una fetta grossa è copywriting,
   contenuti motivazionali e pagine di vendita, cioè i generi dove la figura
   abbonda.
2. **Il preference tuning.** Nella fase in cui delle persone scelgono fra due
   risposte, le formulazioni sicure e assertive vincono più spesso, e una
   correzione al rialzo suona sicura.

La generazione da sinistra a destra è un **amplificatore**, non la causa: un
modello emette di norma il token adeguato al primo colpo, e quando la tendenza
appresa lo porta a correggere al rialzo la correzione resta scritta, perché non
c'è un cestino. Chi scrive a mano fa la stessa revisione in privato e mostra solo
il risultato pulito.

⚠️ Nei testi non si scrive che la scrittura token-per-token «la produce per
necessità»: il paper dice il contrario, ed è un errore già corretto due volte.

## Le forme, che sono più di una

Fontanier la classifica fra le figure di **pensiero**: agisce sull'idea, e non ha
una forma obbligata. Il detector del paper copre la famiglia «non X, ma Y», che è
la parte esposta. Le altre superfici, tutte della stessa figura:

- «più che X, Y»
- «X, o meglio Y»
- «definirlo X è riduttivo»
- «chiamarla X non le rende giustizia: è Y»
- «quello che sembra X in realtà è Y»
- «non tanto X quanto Y»
- «se non X, almeno Y», nella variante che attenua
- «diciamo X. Anzi, Y»

Conseguenza pratica: chi vieta una forma sola ottiene una redistribuzione sulle
altre. Il paper lo verifica, e l'istruzione che funziona nomina **densità e
registro**, non la stringa: «al massimo una correzione enfatica in tutto il
testo, e solo se chiarisce qualcosa».

## Quanta ne regge un genere

Occorrenze ogni 10.000 parole. La colonna «umani» è la base contro cui si calcola
l'indice, e viene dalla Tabella 1 del paper (inglese) e dal §7.8 (italiano).

| Genere | Umani | Modelli senza istruzioni | Indice |
| --- | --- | --- | --- |
| Enciclopedico | 1,2 | 1,4 | 1,2× |
| Giornalistico | 2,4 | 2,0 | 0,9× |
| Abstract accademico | 3,6 | 7,8 | 2,2× |
| Narrativo | 7,5 | 4,1 | 0,5× |
| Domanda e risposta informale | 8,2 | 1,3 | 0,2× |
| Argomentativo (italiano, Beccaria) | ~12 | 56,9 | 4,7× |
| Oratorio (italiano) | ~14 | 39,6 | 2,8× |
| Promozionale | non esiste una base pubblica | 68,5 | — |

Due letture che servono al lavoro:

- **La mis-calibrazione va in due sensi.** Nell'oratoria i modelli stanno al
  doppio degli umani; nella scrittura informale di domanda e risposta scendono a
  un quinto, perché le persone si correggono e si qualificano con naturalezza e
  loro restano piatti. Un testo con zero correzioni in un registro colloquiale è
  fuori calibro quanto uno gonfio in un discorso.
- **Il promozionale non ha una base umana**, e il paper lo dichiara. Sulle
  landing quindi non si cita un numero: la regola è quella di chi firma il sito,
  e per Federico è zero.

## Spegnerla del tutto è un altro errore

Tabella 2 del paper, l'esperimento con la manopola (il coefficiente α di un
adapter LoRA addestrato apposta):

| α | Complessiva | Oratoria | Argomentazione |
| --- | --- | --- | --- |
| 0 (spento) | 61,4 | 22,5 | 75,0 |
| 0,75 | — | — | **12,3** (base umana ~12) |
| 1,0 (pieno) | 4,7 | ~0 | ~0 |

A piena forza la figura sparisce e il testo finisce **sotto** il tasso umano.
Il bersaglio giusto è α intermedio, cioè il tasso di chi scrive quel genere.
Tradotto nel lavoro di revisione: in un testo lungo e argomentativo una o due
correzioni al rialzo vere ci stanno, e toglierle tutte è un'altra forma di
artificiale.

## Quanto ci si può fidare del rilevatore

Validazione su 206 finestre da ~150 parole, annotate da due persone e
riconciliate (Appendice B del paper):

| Misura | Valore |
| --- | --- |
| Precisione micro | 0,45 |
| Recall micro | 0,52 |
| Accordo fra annotatori (κ di Cohen) | 0,35 |
| **Precisione su testo generato** | **0,82** |
| **Precisione su testo umano** | **0,17** |

Quel 0,17 è la ragione della regola più importante della skill: su un testo
scritto da una persona, cinque spie su sei sono contrasti ordinari e non
correzioni al rialzo. Sul testo generato invece il frame canonico è davvero
quello, e la misura tiene.

Il recall più basso sta nel parlato (0,14), e la ragione è utile: cinque delle
sei correzioni mancate erano marcate, ma da «cioè», «diciamo», «come potrei
dire», che il canale lessicale non implementa. È il canale a essere stretto, non
il parlato a essere senza marcatori.

## Falsi positivi da conoscere

Non si «correggono»:

- **I testi che parlano della figura.** Un articolo, un paper o una guida che
  cita gli esempi ha per forza una densità alta: gli esempi sono l'oggetto del
  discorso. Anche questa skill esce con l'indice sopra 3.
- **Le citazioni.** La frase di un altro resta com'è, anche quando contiene la
  figura. Si corregge la parafrasi intorno, mai la citazione.
- **Il lessico tecnico.** «Rappresentare» quando un vettore rappresenta una
  parola o un grafico rappresenta dei dati; «rappresentatività» nella
  linguistica dei corpora; «differenza significativa» quando dietro c'è una
  statistica; «diritti fondamentali» in un testo giuridico; «chiave» quando è
  una chiave di cifratura o di un servizio.
- **Le antitesi vere.** «Produce traffico ma non conversioni» dice due fatti che
  convivono, e non è una correzione al rialzo. È esattamente il caso in cui il
  rilevatore vale 0,17.
