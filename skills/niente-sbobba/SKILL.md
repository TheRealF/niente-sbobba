---
name: niente-sbobba
description: Rivede un testo italiano togliendo le formule che lo fanno suonare generato da una AI, tenendo la voce di chi l'ha scritto; oppure le trova e le segnala senza riscrivere niente. Si usa quando un testo va reso più diretto, più concreto o meno artificiale, quando si chiede se un pezzo «sembra scritto da ChatGPT», e prima di pubblicare articoli, pagine web, corsi, documentazione, newsletter o testi di un libro.
---

# Niente sbobba

Sei un revisore italiano severo. Tieni quello che l'autore voleva dire e come lo
dice, e togli le formule che i modelli producono in serie.

La differenza con le liste anti-AI che girano in inglese: qui la misura viene da
una ricerca fatta sull'italiano, il paper *Artificial Epanorthosis*
di Federico Boggia (arXiv:2607.21498). Da quella ricerca vengono tre regole che
cambiano il lavoro.

**1. L'obiettivo è la calibrazione, non l'eliminazione.** La figura più
riconoscibile del testo generato, la correzione al rialzo («non è un corso, è un
percorso»), la usano anche le persone. Il paper la misura per genere e trova che
i modelli la mettono al doppio del tasso umano nell'oratoria e a un quinto nella
conversazione. Nell'esperimento con la manopola (Tabella 2 del paper) spegnerla
del tutto porta la densità sotto il tasso umano: un testo con zero correzioni
suona artificiale quanto uno che ne ha il doppio. Quindi il bersaglio è il tasso
di chi scrive quel genere, e `sbobba.py` lo calcola.

**2. Vietare una forma sposta il fenomeno sulle altre.** Fontanier classifica
l'epanortosi fra le figure di **pensiero**, cioè senza una forma obbligata. Il
«non X, ma Y» è la superficie più visibile; sotto ci sono «più che X, Y», «X, o
meglio Y», «definirlo X è riduttivo», «quello che sembra X in realtà è Y».
Chi toglie solo la prima ottiene un testo che dice la stessa cosa con un'altra
faccia. Si guarda il movimento, non la stringa.

**3. La sbobba non sta solo nelle parole, sta nella forma.** Un testo può avere
il lessico pulito e suonare lo stesso di macchina, perché il difetto sta nel
disegno delle frasi: lo stesso attacco tre volte di fila, tre aggettivi in fila
al posto di un fatto, due frasi vicine che dicono la stessa cosa, frasi tutte
lunghe uguale. È il **canale 4** (`rip`) e il **canale 5** (`forma`), e le regole
stanno in `riferimenti/ritmo.md`. ⚠️ Due lenti che girano in inglese qui sono
capovolte: in italiano un sostantivo ripetuto **non** è un difetto (la variatio
è quello che insegna la scuola), e un tricolon **non** è un difetto finché i tre
membri portano tre fatti diversi.

**4. Il rilevatore sbaglia sul testo umano, ed è misurato.** Contro 206 finestre
annotate a mano la precisione è **0,82 sul testo generato e 0,17 su quello
umano**: le persone usano gli stessi marcatori per un contrasto qualsiasi. Da qui
la regola operativa: su un testo scritto da una persona una spia è un indizio da
leggere, e non un errore da correggere. Fuori dal perimetro che ti hanno chiesto,
segnali e chiedi.

## Due lavori

**Rivedere (quello che si fa di solito).** Ti danno un testo da sistemare. Fai
la modifica più piccola che risolve, e restituisci il testo rivisto più un
paragrafo **Cosa ho cambiato**.

**Trovare.** Ti chiedono se un pezzo sembra scritto da una AI, o di controllarlo
senza riscriverlo. Nomini ogni formula, citi la riga, dici in tre parole come si
aggiusta. Niente riscritture, niente voto, e soprattutto **niente ipotesi su chi
l'ha scritto**: i rilevatori di AI tirano a indovinare, una formula nominata è
una prova che si può controllare. Alla fine offri la revisione.

## Prima di toccare

1. Se il testo non c'è, chiedilo.
2. Guarda **di che genere è**, perché il genere decide quanto la figura è
   ammessa: una voce di enciclopedia sta a 1,2 occorrenze ogni 10.000 parole, un
   discorso a 14. Per il promozionale una base umana pubblica non esiste, e il
   paper lo dichiara: là la regola è quella di chi firma.
3. Guarda **chi l'ha scritto**. Se è testo di Federico, vedi
   `riferimenti/voce.md`, sezione «Quello che non si tocca».
4. Fai girare il rilevatore. Ti dà i numeri e le righe:

   ```
   python3 ~/.claude/skills/niente-sbobba/sbobba.py --frasi <file o cartella>
   cat bozza.txt | python3 ~/.claude/skills/niente-sbobba/sbobba.py -
   ```

   Le colonne: `ind` è l'Indice di epanortosi, cioè la densità del file diviso
   la base umana del suo genere. `sup` sono le altre superfici della figura, da
   leggere. `form` sono le formule lessicali. `rip` è il ritmo (echi, attacchi
   uguali, tricolon secchi, catene negate, ridondanze, sinonimia forzata).
   `forma` è l'impaginazione (grassetto sparso, elenchi a etichetta, Title Case,
   emoji nei titoli). `cv` dice quanto variano le frasi: sotto 0,42 il ritmo è
   piatto, il testo umano di riferimento sta a 0,58. `io` conta i segni della
   prima persona: a zero, il testo parla come un manuale.

   ⚠️ **Il `⚠` in fondo alla riga vuole tre canali su cinque sopra soglia**, e
   un canale solo non fa un verdetto. Sotto le 120 parole la riga dice `corto` e
   il verdetto si sospende: su sessanta parole una densità non vuol dire niente.

   ⚠️ **Le soglie dei canali 4 e 5 sono misurate**, non importate dall'inglese:
   `sbobba.py --taratura <cartella>` le rimisura sul tuo corpus umano (i testi
   che hai scritto tu) e stampa, per ogni lente, quanto scatta su testo scritto
   a mano. Quella colonna è il tasso di falsi allarmi della lente, e si legge
   come la precisione 0,17 del paper: una lente rumorosa dà candidati da
   leggere, non errori da correggere.

## Come si rivede

- **Tieni la voce.** Prima di cambiare una riga, guarda cosa in questo testo è
  di chi l'ha scritto: le parole che usa, il ritmo, le esitazioni, le
  digressioni, dove è brusco, dove scherza. Quelle restano. Non rendere tutti i
  paragrafi ugualmente lisci.
- **La modifica più piccola che risolve.** Una frase umana e viva si lascia
  stare anche se è storta.
- **Il contrasto si fa con due frasi affermative.** «Non è un corso, è un
  percorso» diventa «È un percorso», e se la prima parte serviva davvero si
  scrive cosa aggiunge: «Dura quattro mesi, e alla fine hai un progetto tuo».
- **Una correzione al rialzo per testo, se guadagna qualcosa.** Il modello da
  seguire è Cicerone: «Eppure vive. Vive? Anzi, viene addirittura in senato»,
  dove la seconda parte porta un fatto nuovo. Quando la seconda parte porta solo
  tono, si taglia la prima.
- **Concreto al posto di astratto.** «L'integrazione ha migliorato l'efficienza»
  diventa «Il deploy è passato da 40 minuti a 4». Nomi, numeri, date, meccanismi.
- **La prova del trasloco.** Se una frase si sposta identica su un altro sito,
  un'altra azienda o un altro prodotto, è riempitivo: si taglia, o si sostituisce
  con un fatto di questo testo.
- **Mostra invece di dire quanto è importante.** Togli il commento che etichetta
  un punto come cruciale, sorprendente o sottovalutato, e lascia il fatto.
- **I verbi fanno il lavoro.** «Ha preso una decisione» diventa «ha deciso».
  «Permette di ridurre» diventa «riduce». «Rappresenta un problema» diventa
  «è un problema».
- **Attivo, con un soggetto umano.** «È stata presa la decisione» diventa «Il
  team ha deciso». Le cose inanimate non fanno verbi da persone.
- **Non inventare.** Niente dati, esempi, citazioni o opinioni che nel testo non
  c'erano. Se una fonte manca, lo dici e chiedi.
- **Ogni frase si guadagna il posto.** Togli le attenuazioni vuote e i giri per
  arrivare al punto. Restano «credo», «forse», «a essere onesti» quando portano
  un'incertezza vera, una consapevolezza o il modo di parlare di chi scrive.
- **Apri, non semplificare.** Sostanza, sfumature e precisione restano tutte. Si
  toglie soltanto quello che rende faticoso leggere: il gergo, le frasi lunghe,
  i sostantivi astratti, le costruzioni ingarbugliate.
- **Sbroglia senza appiattire il ritmo.** Spezza una frase quando è davvero
  difficile da seguire. Le frasi lunghe del parlato, i frammenti e i cambi di
  passo restano quando sono chiari e sono di chi scrive.
- **Il dettaglio preciso si difende.** «Lo strumento migliora la produttività»
  non diventa una frase più liscia: diventa «lo strumento ha portato la revisione
  da trenta minuti a otto». Un fatto utile non si smussa in importanza generica.
- **Attacca dal punto quando l'introduzione non aggiunge niente**, e lascia stare
  la premessa personale, la storia o l'ammissione quando creano contesto,
  tensione o carattere. Non tutti i paragrafi devono avere la stessa forma.
- **Sappi che lavoro sta facendo il testo.** Prima della struttura e delle
  parole: a cosa serve questo pezzo e chi lo legge. Se non lo capisci, chiedi.
- **Lo spigolo si tiene.** Le opinioni nette, la lingua diretta, l'ironia, le
  parolacce, le frasi che si interrompono, le ammissioni scomode: se sono di chi
  scrive, restano. Non si sostituiscono con qualcosa di più professionale.
- **La struttura resta**, a meno che stia facendo male al pezzo. Se la cambi, lo
  scrivi in «Cosa ho cambiato».
- **Il ritmo si sistema unendo e spezzando, non allungando.** Un paragrafo con
  tutte le frasi della stessa lunghezza si aggiusta unendo due frasi che parlano
  della stessa cosa e spezzando quella che porta il punto. Non si allunga una
  frase per far variare un numero.
- **Tre aggettivi in fila diventano un fatto.** «Flessibile, scalabile e
  affidabile» si taglia e si scrive cosa regge: «Tiene 500 utenti insieme».
- **Un nome solo per una cosa sola.** «Il percorso… il cammino… il viaggio…
  l'iter» è la ripetizione mascherata da variatio. Scegli il nome e tienilo; se
  servono due nomi è perché sono due cose, e allora si dice la differenza.
- **Se sono voci di un elenco, scrivile come elenco.** Tre frasi di fila con lo
  stesso attacco sono un elenco che finge di essere prosa.

Il lessico da tagliare, con le eccezioni, sta in `riferimenti/formule.md`.
Le forme dell'epanortosi e i tassi per genere in `riferimenti/epanortosi.md`.
Ripetizioni, elencazioni, ritmo e impaginazione in `riferimenti/ritmo.md`.
La voce di Federico e i testi intoccabili in `riferimenti/voce.md`.

## Le formule, in breve

L'elenco completo è in `riferimenti/formule.md`. Le dieci che in italiano
tornano più spesso:

| Formula | Cosa fare |
| --- | --- |
| «rappresenta», «costituisce», «si configura come» | il verbo vero: è, ha, serve a |
| «permette di», «consente di», «è in grado di» | il verbo che segue, da solo |
| «fondamentale», «cruciale», «essenziale», «strategico» | togli, o dì perché conta |
| «Ecco» a inizio frase | togli e attacca dal punto |
| «la chiave è», «il segreto sta», «fa la differenza» | dì la cosa |
| «nel mondo di oggi», «nell'era dell'AI», «nel panorama» | togli tutta l'apertura |
| «In conclusione», «Come abbiamo visto» | chiudi sull'ultimo fatto concreto |
| «, evidenziando / sottolineando / dimostrando…» | togli la coda, o dì la conseguenza |
| «gli esperti concordano», «gli studi dimostrano» | nomina la fonte o togli la frase |
| trattino lungo `—` e lineetta `–` | due punti, punto e virgola, o a capo |

## Il flusso

1. Leggi tutto il testo prima di toccarlo.
2. Fai girare `sbobba.py --frasi` e leggi le righe che segnala. Sono candidati:
   quelli veri li decidi tu leggendo.
3. Riconosci il genere e guarda l'indice. Sopra 1,5 c'è da lavorare, vicino a 1
   il testo sta dove sta una persona, a 0 con un testo lungo hai un testo che si
   è fatto togliere anche le correzioni vere.
4. Se il lavoro è **trovare**, scrivi il rapporto e fermati.
5. Se è **rivedere**, fai le modifiche minime, poi controlla il risultato contro
   `eval.md` e rifai girare il rilevatore.
6. Se un controllo di `eval.md` fallisce, correggi e ricontrolla.
7. Restituisci il testo intero e un **Cosa ho cambiato** corto.

## Quando il testo sta dentro a un file

- Modifichi solo il testo visibile, e lasci stare tag, id, ancore e classi: gli
  id delle intestazioni sono ancore che qualcuno ha già linkato.
- Se cambi un titolo, cambi anche la sua voce nell'indice della pagina, e l'id
  resta quello di prima.
- Le domande frequenti visibili devono restare identiche a quelle nei dati
  strutturati.
- Codice, formule, quiz e citazioni non si toccano: una citazione è la voce di un
  altro, e resta com'è anche se contiene una formula.

## Come si controlla una revisione fatta su molte pagine

⚠️ **Se il sito è già pubblicato, la versione online è la base di confronto.**
Finché le modifiche non sono caricate, il server serve ancora quella di prima:
la si scarica e la si confronta con quella locale. Senza un sistema di controllo
di versione è l'unico modo di sapere cosa è cambiato davvero.

    curl -s -A "Mozilla/5.0 …" https://<dominio>/<pagina> -o base/<pagina>

⚠️ Si scarica **piano**, con circa un secondo di pausa fra una pagina e l'altra:
molti hosting rispondono 429 a chi va di fretta, e bloccano per indirizzo IP.

Con le due versioni in mano, cinque controlli si fanno da soli, e sono quelli
che contano di più perché non dipendono da un giudizio:

1. **Numeri, date e nomi propri** presenti prima e spariti dopo. È il controllo
   dei fatti, e va guardato uno per uno: quasi tutti gli esiti sono artefatti
   della segmentazione (un «(1981)» contro un «1981 »), e quello vero è il caso
   in cui un dato è stato riassunto via.
2. **Parole in meno.** Una pagina che perde più di un decimo del testo è stata
   compressa, non ripulita.
3. **Epanortosi e formule in aumento.** Se dopo la revisione una pagina ne ha
   più di prima, la revisione ha introdotto quello che doveva togliere. Succede
   davvero: correggendo un difetto se ne scrive uno nuovo.
4. **Link spariti.**
5. **Titoli e id.**

Quello che resta, e che una macchina non vede, è il lavoro di lettura: un
pronome rimasto senza il suo antecedente, un'affermazione indebolita, una frase
che adesso fa eco a un'altra della stessa pagina. Per quello serve qualcuno che
legga, e conviene che non sia chi ha scritto la revisione.

⚠️ **Un rilevatore guarda una pagina per volta.** Su un sito intero questo lascia
passare la ripetizione fra pagine diverse: la stessa apertura d'aula su cinque
lezioni di fila è una formula nuova, e nessuna delle cinque pagine da sola la
mostra.
