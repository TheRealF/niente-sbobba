# niente-sbobba

Toglie da un testo italiano le formule che lo fanno percepire come generato da
una AI, senza togliere la voce di chi l'ha scritto.

**Le istruzioni stanno in [`skills/niente-sbobba/SKILL.md`](skills/niente-sbobba/SKILL.md).
Leggilo per intero prima di rivedere un testo**, insieme ai tre file in
`skills/niente-sbobba/riferimenti/`:

- `formule.md` — il lessico italiano da togliere, con le eccezioni;
- `epanortosi.md` — la figura, le sue forme, i tassi umani per genere e i limiti
  della misura;
- `voce.md` — da riempire con la voce dell'autore, sennò il testo esce corretto e
  di nessuno.

Dopo la revisione, controlla il risultato contro
[`skills/niente-sbobba/eval.md`](skills/niente-sbobba/eval.md).

Il rilevatore è Python 3 senza dipendenze:

    python3 skills/niente-sbobba/sbobba.py --frasi testo.md

⚠️ È un indizio, non un giudice: la sua recall misurata è 0,52 e copre la
famiglia «non… ma». Le altre forme le devi vedere leggendo. Se dà zero, vuol
dire solo che non ha trovato la forma che sa cercare.
