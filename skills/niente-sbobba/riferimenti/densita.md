# Densità: quanta roba c'è dentro

Il canale 6. Gli altri cinque guardano **come** è scritto un testo. Questo
guarda **quanto dice**, ed è il pezzo che mancava.

Viene da [*Measuring AI Slop in Text*](https://arxiv.org/abs/2509.19163), che
intervista redattori di mestiere e fa annotare a tre copy-editor professionisti
150 articoli e 100 risposte, span per span. Delle sette dimensioni che ne
escono, tre predicono il giudizio «questo è slop» meglio di tutte: *relevance*,
**density**, *tone*. La densità è la sostanza rispetto alla lunghezza.

⚠️ Gli autori scrivono anche che **le metriche automatiche da sole non bastano**:
tre dei cinque predittori significativi non hanno uno strumento che li misuri
bene. E l'accordo fra annotatori sul giudizio binario è basso (κ fra 0,06 e
0,29). Quindi anche questo canale dà candidati, come gli altri.

## Come si conta, senza librerie

Si contano gli **appigli**: un numero, una data, una percentuale, un'unità di
misura, un nome proprio, una sigla, una cifra in euro, una citazione fra
virgolette. Roba che qualcuno ha dovuto sapere per scriverla.

Due misure, e si leggono insieme:

- `app` = appigli ogni 100 parole.
- `vuote` = quota di periodi che non ne hanno **nessuno**.

⚠️ La seconda di solito dice di più. Un testo può avere una media decente
perché due paragrafi sono pieni di numeri mentre tutto il resto gira a vuoto.

⚠️ La maiuscola a inizio periodo non conta come nome proprio. In italiano ce
l'ha qualunque parola, e contarla regalerebbe un appiglio a ogni frase.

È la **prova del trasloco** della `SKILL.md` detta con un conto: un periodo
senza appigli è un periodo che si sposta identico sul sito di un altro.

## I numeri, misurati

| corpus | app / 100 parole | periodi senza appigli |
| --- | --- | --- |
| Manoscritti di Federico (136 file) | mediana **8,0** | mediana **60%** |
| Wiki del sito (89 pagine) | mediana **9,5** | mediana **49%** |
| Pubblicazioni (22 pagine) | mediana **6,4** | mediana **66%** |
| Gli esempi di sbobba della repo | **0,0 – 3,7** | **83% – 100%** |

La soglia del cancello di corroborazione sta a **`vuote` sopra l'80%**, che è
appena sopra il p90 umano (78,7%).

⚠️ **Densità bassa non è un difetto in sé.** Un testo narrativo o riflessivo
sta in basso e fa bene. Serve su quello che promette di informare: una guida,
una landing, una relazione, una pagina di prodotto.

## La cosa che ha fatto scattare il canale

Negli esempi della repo, `prima-argomentativo-3.txt` e
`dopo-argomentativo-3.txt` sono la stessa pagina prima e dopo una revisione.
Le formule scendono da 0 a 0, l'epanortosi pure, il ritmo migliora.

Appigli: **0,0 prima e 0,0 dopo**. Periodi vuoti: **100% prima e 100% dopo**.

La revisione ha tolto il modo di dire e ha lasciato il niente. Nessuno degli
altri cinque canali se ne accorge, perché tutti e cinque misurano la forma. Per
questo il canale esiste.

## Come si alza

Non allungando. Si prende un periodo vuoto e gli si mette dentro la cosa che si
sa e che il lettore no:

- **un numero**: «più veloce» → «2,6 s contro 18,7»
- **un nome**: «gli esperti» → «Fontanier», «la Sapienza», «Marta del reparto»
- **una data**: «di recente» → «il 3 settembre alle 17:49»
- **un meccanismo**: «ottimizza i processi» → «toglie dalle opzioni le mosse
  che in quel turno sono impossibili»
- **un caso**: «a volte fallisce» → «un refuso nella pagina contatti, dato come
  fastidioso invece che trascurabile, con probabilità 1,000»

Se per un periodo non si trova nessuna delle cinque, quel periodo probabilmente
non serve.
