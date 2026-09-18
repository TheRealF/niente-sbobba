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

Le liste anti-slop che girano sono inglesi: *delve*, *tapestry*, *leverage*,
*it's not X, it's Y*. Tradotte non funzionano, perché in italiano l'effetto
sbobba lo fanno altre parole e altre costruzioni. Una spia grossa da noi è il
**verbo svuotato**, che in inglese non esiste:

> L'integrazione **rappresenta** una svolta **fondamentale** e **permette di**
> ridurre i tempi, **dimostrando** l'attenzione all'innovazione.

Quattro formule in venti parole, e non ci è stato comunicato niente.

## Come decide quanto togliere

Con pesi e misure, presi dal mio paper
**[Artificial Epanorthosis](https://arxiv.org/abs/2607.21498)**.

La figura più riconoscibile della sbobba è l'epanortosi: «non è un corso, è un
percorso». Il paper la misura per genere e scopre che i modelli la mettono al
**doppio** del tasso umano in un discorso e a **un quinto** in una chiacchierata.
E che spegnerla del tutto porta il testo **sotto** il tasso umano: zero
correzioni suona artificiale quanto il doppio.

Quindi il bersaglio è il tasso di chi scrive quel genere, e lo strumento lo
calcola.

| Genere | Umani | Modelli | Indice |
| --- | --- | --- | --- |
| Enciclopedico | 1,2 | 1,4 | 1,2× |
| Giornalistico | 2,4 | 2,0 | 0,9× |
| Narrativo | 7,5 | 4,1 | 0,5× |
| Domanda e risposta | 8,2 | 1,3 | **0,2×** |
| Argomentativo (IT) | ~12 | 56,9 | **4,7×** |
| Oratorio (IT) | ~14 | 39,6 | **2,8×** |

Occorrenze ogni 10.000 parole. Per il promozionale una base umana pubblica non
esiste, e lo strumento lo dice invece di inventarsela.

Due conseguenze pratiche. **Vietare una forma la sposta sulle altre**, perché
Fontanier la classifica fra le figure di *pensiero*: tolto il «non X, ma Y»
ricompare in «più che X, Y», «X, o meglio Y», «definirlo X è riduttivo». E
**sul testo umano il rilevatore sbaglia**: precisione 0,82 sul generato, 0,17 su
quello scritto da una persona, misurata su 206 finestre annotate a mano. Su un
testo tuo una spia è un indizio da leggere, mai una sentenza.

## Quanto ci si può fidare del rilevatore

Poco, ed è misurato. Su dodici testi italiani, scritti da modelli che non
sapevano cosa stavo misurando, la regex ha trovato **zero** epanortosi.
Leggendoli, ce n'erano **quattro**:

> «Il valore vero **non sta** nel codice: **sta** nel capire come lavora un'azienda.»
>
> «**Non serve** nessuna esperienza precedente, **serve** voglia di guardare le cose.»
>
> «**Non inseguiamo** lo stile del momento: cerchiamo edifici che durino.»
>
> «Una biblioteca **non si misura** dal numero dei libri. **Si misura** da quante persone entrano.»

Gli sfuggono perché il verbo è «sta» o «serve» invece di «è», perché il
separatore sono i due punti, e perché la coppia è spezzata in due frasi. Il paper
lo dichiara già: quel canale copre la famiglia «non… ma» e ha recall 0,52.

La skill invece le ha trovate tutte e quattro, perché a leggerla è un modello.
E ne ha lasciate due, quelle dove la seconda parte porta un fatto nuovo.

⚠️ **Lo zero del rilevatore vuol dire una cosa sola: non ha trovato la forma che
sa cercare.** Del resto del testo non sa niente.

## Provata

    python3 test/prova_sbobba.py

Sessantuno casi: quelli che il rilevatore deve prendere, quelli che deve
lasciare stare, e i buchi noti bloccati così come sono. Gira a ogni push.
Tre prima e dopo veri stanno in [`esempi/`](esempi/).

⚠️ Il buco più curioso è in quei test: «Questo non è un corso. È un percorso.»,
cioè lo specimen dell'abstract del paper, **sfugge al pattern del paper**. In
`NEG` c'è `questa?`, che copre il femminile e non il maschile. Lo prende il
secondo canale. Il primo resta verbatim, sennò la misura non è più confrontabile
con quella pubblicata.

## Installazione

```bash
npx skills add TheRealF/niente-sbobba --skill niente-sbobba --global --yes
```

Oppure incolla nel tuo agente: `Installa la skill /niente-sbobba da
https://github.com/TheRealF/niente-sbobba`

## Funziona anche fuori da Claude

Le istruzioni sono Markdown e il rilevatore è Python 3 senza dipendenze, quindi
non c'è niente di legato a un modello o a uno strumento.

| Dove | Come |
| --- | --- |
| Claude Code | `npx skills add TheRealF/niente-sbobba …`, poi `/niente-sbobba` |
| Codex, Cursor, e chi legge `AGENTS.md` | clona il repo: il file in radice punta già alle istruzioni |
| ChatGPT, Gemini, altri | carica `SKILL.md` e i tre file di `riferimenti/` in un progetto, oppure incollali come istruzioni |
| Senza nessun modello | `python3 sbobba.py --frasi testo.md`, che misura e basta |

## Come si usa

| Comando | Cosa fa |
| --- | --- |
| `/niente-sbobba (testo)` | lo rivede, tiene la voce, e dice cosa ha cambiato e cosa ha lasciato stare |
| `/niente-sbobba è sbobba questo? (testo)` | nomina le formule e cita le righe, senza riscrivere |
| `python3 sbobba.py --frasi testo.md` | solo la misura, senza modello |

Il rilevatore gira su `.html`, `.md`, `.txt` e da standard input, senza
dipendenze. Le colonne: `ind` è l'indice contro la base umana del genere, `sup`
le altre superfici della figura, `form` le formule, `io` i segni della prima
persona. **`io` a zero vuol dire che il testo parla come un manuale**, ed è
spesso il difetto vero.

## Cosa trova

Il lessico italiano che nessuna lista inglese ha:

- **verbi svuotati**: rappresenta, costituisce, permette di, è in grado di;
- **riempitivi**: fondamentale, cruciale, essenziale, strategico;
- **aperture che non aprono**: nel mondo di oggi, nell'era digitale, «Ecco»;
- **meta-discorso**: in questa guida, vedremo, In conclusione;
- **gerundio di commento**: «…, evidenziando l'attenzione all'innovazione»,
  che è il trailing `-ing` inglese fatto col gerundio;
- **gonfiaggio**: segna una svolta, una pietra miliare;
- **attribuzione senza nome**: gli esperti concordano, gli studi dimostrano;
- **schiarirsi la voce**: Diciamocelo, Andiamo con ordine, Facciamola semplice;
- **finta rivelazione**: quello che nessuno ti dice, la verità è che, Spoiler:;
- **elenco negato**: «Non è un corso. Non è un webinar. È un percorso.»;
- **guida al lettore**: come puoi vedere, questa distinzione conta;
- **apostrofi**: Fidati, Credimi, Pensaci un attimo;
- **punteggiatura**: trattini lunghi, due punti a effetto, chiuse profonde.

Ogni voce ha la sua cura **e le sue eccezioni**, perché una lista di divieti
senza eccezioni produce testi storti: «rappresentare» resta quando un vettore
rappresenta una parola, «significativo» quando dietro c'è un p-value,
«fondamentale» nei diritti fondamentali.

## Una cosa da fare prima di usarla

⚠️ **Riempi `riferimenti/voce.md`.** Ci si scrive chi parla, cosa non usa mai,
cosa usa e sembra un difetto, e le frasi che l'autore ha scritto di suo pugno e
non si toccano. Senza, la skill toglie le formule e ti restituisce una prosa
corretta e di nessuno, che è il secondo modo di suonare artificiale.

Gli altri file: `SKILL.md` ha le regole, `eval.md` i controlli che la skill fa
sul proprio lavoro, `sbobba.py` il rilevatore, `riferimenti/epanortosi.md` la
figura e i suoi limiti, `riferimenti/formule.md` il lessico con le eccezioni.

## Crediti

L'idea di impacchettare tutto questo come skill viene da
**[no-ai-slop](https://github.com/petergyang/no-ai-slop)** di Peter Yang, che fa
la stessa cosa per l'inglese. Qui il lessico è italiano e il criterio viene dal
paper.

La ricerca è **Federico Boggia** (aka TheRealF aka io), *Artificial
Epanorthosis*, arXiv:2607.21498. I pattern del canale principale sono copiati
verbatim dallo script di valutazione del paper (§7.8), così la misura qui
coincide con quella pubblicata.

## Licenza

MIT.
