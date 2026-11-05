# Vehicles.

App web self-hosted per tenere sotto controllo assicurazione, bollo, manutenzioni (meccanico, carrozziere, gommista) e relative scadenze di uno o più veicoli. Niente carburante né pedaggi.

## Funzioni

- Più veicoli, ognuno con nome, targa e note
- Scadenze (assicurazione, bollo, revisione, tagliando, gomme…) con giorni rimanenti e ripetizione automatica
- «Rinnova» registra il pagamento nello storico e sposta la scadenza avanti
- Allegati facoltativi (PDF o foto) su interventi e scadenze, es. fatture del meccanico
- Elenco di officine e carrozzerie (si popola da solo, gestibile dalle Impostazioni)
- Dettaglio spese dell'anno in corso
- Colore d'accento personalizzabile
- Data di acquisto e di vendita del veicolo
- Storico interventi con data, costo e km, e totale speso
- Tema chiaro/scuro automatico

## Avvio

```bash
docker compose up -d --build
```

L'app risponde su http://localhost:38189. Database (SQLite) e allegati restano in `./data` (`vehicles.db` e `files/`): per il backup basta copiare quella cartella.

## Stack

Flask + SQLite, frontend in un unico `static/index.html` senza dipendenze.
