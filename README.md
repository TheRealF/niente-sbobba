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
*it's not X, it's Y*. Tradotte non servono a niente. In italiano l'effetto sbobba
lo fanno altre parole. La spia più grossa da noi è il **verbo svuotato**, e in
inglese non esiste proprio:

> L'integrazione **rappresenta** una svolta **fondamentale** e **permette di**
> ridurre i tempi, **dimostrando** l'attenzione all'innovazione.

Quattro formule in venti parole, e non ci è stato comunicato niente.

Quando la faccio leggere in aula succede sempre la stessa cosa. La gente
annuisce. Poi mi chiede se c'è un errore. Errori non ce ne sono, e il punto è
quello. La sbobba non suona male. Suona neutra. Per questo ti finisce dentro al
testo senza che te ne accorga.

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

Novanta parole. Undici formule. Due epanortosi. Fa ridere, e quel paragrafo lo
trovi su un sito vero su tre.

`ind` è l'indice contro la base umana del genere, `sup` le altre superfici della
figura, `form` le formule, `io` i segni della prima persona. **Se `io` ti esce
zero, il tuo testo parla come un manuale**, ed è quasi sempre il difetto vero.

Gira su `.html`, `.md`, `.txt` e da standard input, ed è Python 3 senza
dipendenze.

### Confrontare un prima e un dopo

Un numero da solo dice poco. Con un prima e un dopo ti dice se la revisione ha
tolto o ha aggiunto. È l'unica domanda a cui una regex risponde bene.

```bash
python3 sbobba.py --confronta bozza.md rivisto.md
python3 sbobba.py --confronta sito-vecchio/ sito-nuovo/
```

Esce con 1 se una pagina ha **più** sbobba di prima. Succede davvero. Correggendo
un difetto se ne scrive uno nuovo, e capita più spesso di quanto sembri.

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

La sbobba ha una figura sua. Si chiama epanortosi, e la riconosci a colpo
d'occhio: «non è un corso, è un percorso». Nel paper l'ho misurata per genere.
I modelli la mettono al **doppio** del tasso umano in un discorso. In una
chiacchierata scendono a **un quinto**.

Poi ho provato a spegnerla del tutto, con un adapter addestrato apposta. Il testo
è finito **sotto** il tasso umano. Zero correzioni suona finto quanto il doppio.

Quindi non te la tolgo tutta. Te la riporto al tasso di chi scrive quel genere.
Questi sono i numeri che uso.

| Genere | Umani | Modelli | Indice |
| --- | --- | --- | --- |
| Enciclopedico | 1,2 | 1,4 | 1,2× |
| Giornalistico | 2,4 | 2,0 | 0,9× |
| Narrativo | 7,5 | 4,1 | 0,5× |
| Domanda e risposta | 8,2 | 1,3 | **0,2×** |
| Argomentativo (IT) | ~12 | 56,9 | **4,7×** |
| Oratorio (IT) | ~14 | 39,6 | **2,8×** |

Occorrenze ogni 10.000 parole. Per il promozionale una base umana non ce l'ha
nessuno. Lo strumento te lo dice invece di inventarsela.

Da lì vengono due cose che mi sono costate tempo.

La prima. **Se vieti una forma, la sposti sulle altre.** Fontanier mette
l'epanortosi fra le figure di *pensiero*. Togli il «non X, ma Y» e ti ricompare
in «più che X, Y», in «X, o meglio Y», in «definirlo X è riduttivo».

La seconda. **Sul testo umano il rilevatore sbaglia di brutto.** Precisione 0,82
sul generato, 0,17 su quello scritto da una persona. Misurata a mano su 206
finestre. Sul tuo testo una spia ti dice solo di andare a guardare.

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

Perché gli sfuggono? Il verbo è «sta» o «serve» invece di «è». Il separatore sono
i due punti. E la coppia è spezzata in due frasi. Nel paper l'avevo già scritto.
Quel canale copre la famiglia «non… ma», e ha recall 0,52.

Poi ho dato gli stessi dodici testi alla skill. Le ha trovate tutte e quattro,
perché a leggerla è un modello. Due le ha lasciate lì apposta, quelle dove la
seconda parte porta un fatto nuovo.

⚠️ **Occhio allo zero.** Vuol dire che il rilevatore non ha trovato la forma che
sa cercare, e del resto del tuo testo non sa niente.

## L'ho provata

    python3 test/prova_sbobba.py

Sessantacinque casi, e girano a ogni push. Quello che il rilevatore deve
prendere. Quello che deve lasciare stare. E i buchi noti, bloccati così come
sono. Tre prima e dopo veri stanno in [`esempi/`](esempi/).

⚠️ Il buco più bello l'ho scoperto scrivendo quei test. «Questo non è un corso. È
un percorso.» è lo specimen dell'abstract del mio paper. **Il pattern del mio
paper non lo vede.** Dentro c'è un `questa?` che prende il femminile e si perde
il maschile. Lo raccoglie il secondo canale. Il primo lo lascio com'è, sennò i
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

Se un testo l'ha scritto una AI, questa skill non te lo dice. Quelli che lo
promettono tirano a indovinare. Io preferisco nominarti la formula e citarti la
riga, e poi controlli te.

Sull'inglese non ci provo nemmeno. Per quello c'è già
[no-ai-slop](https://github.com/petergyang/no-ai-slop). Refusi, accordi e virgole
li lascia dove stanno. Per quelli ti serve un correttore di bozze.

Il limite grosso però è un altro, e conviene saperlo prima. Le formule te le
toglie. Le cose da dire ce le devi mettere te. Su un testo che non ha niente da
dire ti restituisce un testo pulito che non ha niente da dire.

Una cosa capita a tutti. La prima volta che lo lanci sul tuo testo, ti segnala
una frase a cui tieni. L'hai scritta te, e probabilmente è giusta così. Lo
strumento trova **formule, non autori**. Su un testo scritto da una persona
sbaglia cinque volte su sei. Per questo ti segnala invece di correggere.

## Una cosa da fare prima di usarla

⚠️ **Riempi `riferimenti/voce.md`.** Scrivici chi parla. Cosa non usa mai. Cosa
usa e sembra un difetto. E le frasi che hai scritto di tuo pugno, quelle che
nessuno deve toccare.

Senza quel file ti toglie le formule e ti restituisce una prosa corretta e di
nessuno. È il secondo modo di suonare artificiale.

Gli altri file. `SKILL.md` ha le regole. `eval.md` i controlli che la skill fa
sul proprio lavoro. `sbobba.py` è il rilevatore. `riferimenti/epanortosi.md`
spiega la figura e i suoi limiti, `riferimenti/formule.md` il lessico con le
eccezioni.

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
