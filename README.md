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

Quando faccio questo esercizio in aula la reazione è sempre la stessa: la gente
legge la frase, annuisce, e poi mi chiede se è sbagliata. No, è normale. Il punto
è proprio quello: la sbobba non suona male, suona *neutra*. Ed è per questo che
ti finisce dentro al testo senza che te ne accorga.
## Come si usa

```bash
npx skills add TheRealF/niente-sbobba --skill niente-sbobba --global --yes
```

Oppure incolla nel tuo agente: `Installa la skill /niente-sbobba da
https://github.com/TheRealF/niente-sbobba`

Poi:

| Comando | Cosa fa |
| --- | --- |
| `/niente-sbobba (testo)` | te lo rivede, ti tiene la voce, e ti dice cosa ha cambiato e cosa ha lasciato stare |
| `/niente-sbobba è sbobba questo? (testo)` | ti nomina le formule e ti cita le righe, senza riscrivere niente |
| `python3 sbobba.py --frasi testo.md` | solo la misura, senza nessun modello |

Il rilevatore da solo, se vuoi guardare un testo in fretta. Nel repo c'è un file
di prova, così vedi subito che aria tira:

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

Novanta parole, undici formule e due epanortosi. Fa ridere, ma quel paragrafo lo
trovi su un sito vero su tre.

`ind` è l'indice contro la base umana del genere, `sup` le altre superfici della
figura, `form` le formule, `io` i segni della prima persona. **Se `io` ti esce
zero, il tuo testo parla come un manuale**, ed è quasi sempre il difetto vero.

Gira su `.html`, `.md`, `.txt` e da standard input, ed è Python 3 senza
dipendenze.

### Anche fuori da Claude

Le istruzioni sono Markdown, quindi gira con qualunque modello e dentro a
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

La sbobba ha una figura sua, che riconosci a colpo d'occhio: l'epanortosi, cioè
«non è un corso, è un percorso». Nel paper l'ho misurata per genere, e i modelli
la mettono al **doppio** del tasso umano in un discorso e a **un quinto** in una
chiacchierata. Poi ho provato a spegnerla del tutto, con un adapter addestrato
apposta, e il testo è finito **sotto** il tasso umano. Zero correzioni suona
finto quanto il doppio.

Quindi non te la tolgo tutta. Te la riporto al tasso di chi scrive quel genere, e
questi sono i numeri che uso.

| Genere | Umani | Modelli | Indice |
| --- | --- | --- | --- |
| Enciclopedico | 1,2 | 1,4 | 1,2× |
| Giornalistico | 2,4 | 2,0 | 0,9× |
| Narrativo | 7,5 | 4,1 | 0,5× |
| Domanda e risposta | 8,2 | 1,3 | **0,2×** |
| Argomentativo (IT) | ~12 | 56,9 | **4,7×** |
| Oratorio (IT) | ~14 | 39,6 | **2,8×** |

Occorrenze ogni 10.000 parole. Per il promozionale una base umana pubblica non
ce l'ha nessuno, e lo strumento te lo dice invece di inventarsela.

Due cose che vengono da lì e che mi sono costate tempo. **Se vieti una forma, la
sposti sulle altre**: Fontanier mette l'epanortosi fra le figure di *pensiero*,
quindi togli il «non X, ma Y» e ti ricompare in «più che X, Y», «X, o meglio Y»,
«definirlo X è riduttivo». E **sul testo umano il rilevatore sbaglia di brutto**:
precisione 0,82 sul generato e 0,17 su quello scritto da una persona, misurata a
mano su 206 finestre. Sul tuo testo una spia ti dice solo di andare a guardare.
## Quanto ti puoi fidare del rilevatore

Ho fatto scrivere dodici testi italiani a dei modelli senza dirgli cosa stavo
misurando. La regex ci ha trovato **zero** epanortosi.
Io, leggendoli, ne ho trovate **quattro**:

> «Il valore vero **non sta** nel codice: **sta** nel capire come lavora un'azienda.»
>
> «**Non serve** nessuna esperienza precedente, **serve** voglia di guardare le cose.»
>
> «**Non inseguiamo** lo stile del momento: cerchiamo edifici che durino.»
>
> «Una biblioteca **non si misura** dal numero dei libri. **Si misura** da quante persone entrano.»

Gli sfuggono perché il verbo è «sta» o «serve» invece di «è», perché il
separatore sono i due punti, e perché la coppia è spezzata in due frasi. Nel
paper l'avevo già scritto: quel canale copre la famiglia «non… ma» e ha recall
0,52.

Poi ho dato gli stessi dodici testi alla skill, e le ha trovate tutte e quattro.
Perché a leggerla è un modello, e un modello legge. Due le ha lasciate lì
apposta, quelle dove la seconda parte porta un fatto nuovo.

⚠️ **Occhio allo zero.** Vuol dire che il rilevatore non ha trovato la forma che
sa cercare, e del resto del tuo testo non sa niente.
## L'ho provata

    python3 test/prova_sbobba.py

Sessantuno casi, che girano a ogni push: quello che il rilevatore deve prendere,
quello che deve lasciare stare, e i buchi noti bloccati così come sono. Tre
prima e dopo veri stanno in [`esempi/`](esempi/).

⚠️ Il buco più bello l'ho scoperto scrivendo quei test. «Questo non è un corso.
È un percorso.» è lo specimen dell'abstract del mio paper, e **il pattern del mio
paper non lo vede**: dentro c'è `questa?`, che prende il femminile e si perde il
maschile. Lo raccoglie il secondo canale. Il primo lo lascio com'è, sennò i
numeri non sono più confrontabili con quelli che ho pubblicato.
## Cosa trova

Tredici famiglie. Le prime due sono la spia italiana per eccellenza, e in
inglese non esistono proprio:

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

Ogni voce ha la sua cura **e le sue eccezioni**, perché se vieti senza eccezioni
ti ritrovi un testo storto: «rappresentare» resta quando un vettore rappresenta
una parola, «significativo» quando dietro c'è un p-value, «fondamentale» nei
diritti fondamentali.

## Quello che non fa

Se un testo l'ha scritto una AI, questa skill non te lo dice: quelli che lo
promettono tirano a indovinare, e io preferisco nominarti la formula e citarti la
riga, così vai a controllare te. Sull'inglese non ci provo nemmeno, perché per
quello c'è già [no-ai-slop](https://github.com/petergyang/no-ai-slop). Refusi,
accordi e virgole li lascia dove stanno: per quelli ti serve un correttore di
bozze, che è un altro mestiere.

Il limite grosso però è un altro, e conviene saperlo prima di installarla. Le
formule te le toglie. Le cose da dire ce le devi mettere te. Su un testo che non
ha niente da dire ti restituisce un testo pulito che non ha niente da dire.

La prima volta che lo lanci sul tuo testo ti segnala una frase a cui tieni.
Capita a tutti. L'hai scritta te, e probabilmente è giusta così.
Lo strumento trova **formule, non autori**, e su un testo scritto da una persona
sbaglia cinque volte su sei. Per questo ti segnala invece di correggere.

## Una cosa da fare prima di usarla

⚠️ **Riempi `riferimenti/voce.md`.** Scrivici chi parla, cosa non usa mai, cosa
usa e sembra un difetto, e le frasi che hai scritto di tuo pugno e che nessuno
deve toccare. Senza, ti toglie le formule e ti restituisce una prosa corretta e
di nessuno, che è il secondo modo di suonare artificiale.

Gli altri file: `SKILL.md` ha le regole, `eval.md` i controlli che la skill fa
sul proprio lavoro, `sbobba.py` il rilevatore, `riferimenti/epanortosi.md` la
figura e i suoi limiti, `riferimenti/formule.md` il lessico con le eccezioni.
## Crediti

L'idea di impacchettare tutto questo come skill viene da
**[no-ai-slop](https://github.com/petergyang/no-ai-slop)** di Peter Yang, che fa
la stessa cosa per l'inglese. Qui il lessico è italiano e il criterio viene dal
paper.

La ricerca è mia: **Federico Boggia** (aka TheRealF aka io), *Artificial
Epanorthosis*, arXiv:2607.21498. I pattern del canale principale li ho copiati
verbatim dal mio script di valutazione (§7.8), così quello che misuri qui è
quello che ho pubblicato là.
## Licenza

MIT.
