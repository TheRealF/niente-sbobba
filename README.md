# Niente sbobba

Toglie da un testo italiano le formule che lo fanno suonare generato da una AI,
senza togliere la voce di chi l'ha scritto.

## Il problema

Le liste anti-slop che girano sono inglesi: *delve*, *tapestry*, *leverage*,
*it's not X, it's Y*. Tradotte non funzionano, perché in italiano l'effetto lo
fanno altre parole. La spia numero uno da noi è il **verbo svuotato**, che in
inglese non esiste:

> L'integrazione **rappresenta** una svolta **fondamentale** e **permette di**
> ridurre i tempi, **dimostrando** l'attenzione all'innovazione.

Quattro formule in venti parole, e nessuna compare in una lista inglese.

## Cosa lo rende diverso

Questa skill non è una lista di divieti. La misura viene da una ricerca
sull'italiano, il paper **[Artificial Epanorthosis](https://arxiv.org/abs/2607.21498)**
di Federico Boggia, e da lì vengono tre regole che cambiano il lavoro.

**1. Si calibra, non si elimina.** La figura più riconoscibile del testo
generato è la correzione al rialzo: «non è un corso, è un percorso». La usano
anche le persone. Il paper la misura per genere e trova che i modelli la mettono
al **doppio** del tasso umano nell'oratoria e a **un quinto** nella
conversazione informale. Nell'esperimento con la manopola (un adapter LoRA
addestrato apposta) spegnerla del tutto porta il testo **sotto** il tasso umano:
un testo con zero correzioni suona artificiale quanto uno che ne ha il doppio.
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
esiste, e lo strumento lo dice invece di inventarne una.

**2. Vietare una forma la sposta sulle altre.** Fontanier classifica
l'epanortosi fra le figure di **pensiero**, cioè senza forma obbligata. Tolto il
«non X, ma Y» ricompare in «più che X, Y», «X, o meglio Y», «definirlo X è
riduttivo», «quello che sembra X in realtà è Y». Il rilevatore ha un canale a
parte per quelle, stampato separato perché «anzi» e «cioè» sono italiano
normale.

**3. Sul testo umano il rilevatore sbaglia, ed è misurato.** Contro 206 finestre
annotate a mano da due persone e riconciliate, la precisione è **0,82 sul testo
generato e 0,17 su quello umano**: le persone usano gli stessi marcatori per un
contrasto qualsiasi. Da qui la regola operativa: su un testo scritto da qualcuno,
una spia è un indizio da leggere, non un errore da correggere.

## Installazione

Incolla questo in Claude Code, Codex o nel tuo agente:

```
Installa la skill /niente-sbobba da https://github.com/TheRealF/niente-sbobba
```

Oppure:

```bash
npx skills add TheRealF/niente-sbobba --skill niente-sbobba --global --yes
```

## Come si usa

**Rivedere un testo**

```
/niente-sbobba (il tuo testo)
```

Toglie le formule, tiene la voce, ed elenca cosa ha cambiato e cosa ha lasciato
stare, con il motivo.

**Solo trovare**

```
/niente-sbobba è sbobba questo? (il tuo testo)
```

Nomina ogni formula e cita la riga, senza riscrivere niente. Non dice se l'ha
scritto una AI: i rilevatori di AI tirano a indovinare, una formula nominata è
una prova che si può controllare.

**Misurare, senza modello**

```bash
python3 ~/.claude/skills/niente-sbobba/sbobba.py --frasi testo.md
cat bozza.txt | python3 ~/.claude/skills/niente-sbobba/sbobba.py -
```

Funziona su `.html`, `.md`, `.txt` e da standard input. Le colonne: `ind` è
l'indice di epanortosi contro la base umana del genere, `sup` sono le altre
superfici della figura, `form` le formule lessicali, `io` i segni della prima
persona. **Quando `io` è a zero, il testo parla come un manuale generato**, ed è
spesso il difetto vero.

## Cosa trova

Oltre all'epanortosi, il lessico italiano che nessuna lista inglese ha:

- **Verbi svuotati**: rappresenta, costituisce, si configura come, si traduce
  in, permette di, consente di, è in grado di, effettua un controllo.
- **Riempitivi**: fondamentale, cruciale, essenziale, strategico, prezioso,
  imprescindibile, significativo.
- **Aperture che non aprono**: nel mondo di oggi, nell'era digitale, nel
  panorama attuale, «Ecco» a inizio frase.
- **Meta-discorso**: in questa guida, vedremo, approfondiremo, In conclusione,
  come abbiamo visto.
- **Gerundio di commento**: «…, evidenziando l'attenzione all'innovazione». È il
  trailing `-ing` inglese, in italiano fatto col gerundio.
- **Gonfiaggio**: segna una svolta, una pietra miliare, consolida la sua
  posizione.
- **Attribuzione senza nome**: gli esperti concordano, gli studi dimostrano.
- **Punteggiatura**: trattini lunghi, due punti a effetto, chiuse profonde.

Ogni voce ha la sua cura **e le sue eccezioni**, perché una lista di divieti
senza eccezioni produce testi storti: «rappresentare» resta quando un vettore
rappresenta una parola, «significativo» quando dietro c'è un p-value,
«fondamentale» nei diritti fondamentali.

## Cosa c'è dentro

| File | Cosa fa |
| --- | --- |
| `skills/niente-sbobba/SKILL.md` | le regole e il flusso |
| `skills/niente-sbobba/eval.md` | le verifiche che la skill fa sul proprio lavoro |
| `skills/niente-sbobba/sbobba.py` | il rilevatore, senza dipendenze |
| `riferimenti/epanortosi.md` | la figura, le forme, i tassi per genere, i limiti della misura |
| `riferimenti/formule.md` | il lessico italiano, con le eccezioni |
| `riferimenti/voce.md` | il modello da riempire con la voce del proprio autore |

⚠️ **`riferimenti/voce.md` va riempito.** Senza, la skill toglie le formule e
restituisce una prosa corretta e di nessuno, che è il secondo modo di suonare
artificiale. Ci si scrive chi parla, cosa non usa mai, cosa usa e sembra un
difetto, e soprattutto **le frasi che l'autore ha scritto di suo pugno e non si
toccano**.

## Crediti

L'idea di impacchettare questo lavoro come skill viene da
**[no-ai-slop](https://github.com/petergyang/no-ai-slop)** di Peter Yang, che fa
la stessa cosa per l'inglese. Questa non è la sua traduzione: il lessico è
italiano, e il criterio con cui si decide quanto togliere viene dal paper.

La ricerca è **Federico Boggia, *Artificial Epanorthosis*, arXiv:2607.21498**.
I pattern del canale principale sono copiati verbatim dallo script di
valutazione del paper (§7.8), così la misura qui coincide con quella pubblicata.

## Licenza

MIT.
