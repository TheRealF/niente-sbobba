# Come si aggiunge una formula

Grazie, e una regola sola.

**Una voce nuova entra con due casi in `test/prova_sbobba.py`: uno che deve
scattare e uno che NON deve scattare.**

Il secondo è quello che conta. Una lista di divieti senza eccezioni produce
testi storti, e un rilevatore che grida al lupo lo si smette di guardare. Quando
ho provato la prima versione di queste regole su 209 pagine di un sito vero,
«Attenzione:» faceva 33 falsi positivi su 33, perché nelle lezioni è l'etichetta
di un riquadro e non un effetto retorico. È uscita dal rilevatore ed è finita in
`formule.md` come giudizio di chi legge.

Se la differenza fra l'uso buono e quello cattivo è di **significato e non di
forma**, la regex non può distinguerli: allora la voce resta nel rilevatore come
candidato, e l'eccezione si scrive in `riferimenti/formule.md`, dove la legge il
modello. Nel test si controllano tutte e due le cose, come per «rappresentare»,
«diritti fondamentali» e «differenza significativa».

## Quello che non si tocca

I cinque pattern del canale principale (`RE_NONMA`, `RE_NONSOLO`, `RE_NONVIRG`,
`NEG`, `IDIT`) sono copiati **verbatim** dallo script di valutazione del paper.
Hanno dei buchi noti, documentati nei test: il più curioso è che «Questo non è un
corso. È un percorso.», che è lo specimen dell'abstract, sfugge perché in `NEG`
c'è `questa?` e il maschile non ci rientra.

Quei buchi si coprono nel **secondo canale**, quello delle altre superfici, che
serve a questo. Correggerli nel primo scollegherebbe la misura da quella
pubblicata, e allora l'indice non vorrebbe più dire niente.

## Le basi per genere

Sono numeri di una ricerca, non opinioni: vengono dalla Tabella 1 e dal §7.8 di
[arXiv:2607.21498](https://arxiv.org/abs/2607.21498), e un test li blocca. Per
cambiarne una serve una misura, non un'impressione. Dove una base umana non
esiste, come nel promozionale, lo strumento lo dice invece di inventarla.

## Prima di aprire una pull request

    python3 test/prova_sbobba.py

Esce con 1 se un caso non torna.
