# Tre prima e dopo

Sono tre dei dodici testi della prova descritta nel README, uno per genere.
Li ha scritti un modello a cui non era stato detto cosa si stava misurando, e
li ha rivisti un modello che seguiva le istruzioni della skill.

| Prima | Dopo | Cosa è successo |
| --- | --- | --- |
| `prima-oratorio-1.txt` | `dopo-oratorio-1.txt` | tolta «Una biblioteca non si misura dal numero dei libri. Si misura da…», che la regex non vedeva |
| `prima-promozionale-1.txt` | `dopo-promozionale-1.txt` | due epanortosi e sette formule; è anche il più accorciato dei dodici, −15% |
| `prima-argomentativo-3.txt` | `dopo-argomentativo-3.txt` | epanortosi **tenuta** apposta: «Quei soldi non sono spariti: si sono spostati nelle periferie» |

L'ultima riga è il punto della skill. In un argomentativo la base umana è circa
12 occorrenze ogni 10.000 parole, e quella correzione porta un fatto nuovo:
toglierla sarebbe stato l'errore opposto.

Per vedere la differenza con lo strumento:

    python3 skills/niente-sbobba/sbobba.py --frasi esempi/prima-*.txt
    python3 skills/niente-sbobba/sbobba.py --frasi esempi/dopo-*.txt

⚠️ Sul canale principale li vedrai uguali, tutti e due a zero: quelle epanortosi
sono fra le quattro che la regex non prende. È il motivo per cui la skill la
legge un modello.
