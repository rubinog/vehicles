<div align="center">
Vehicles.
All your vehicles. All in one place.
Una web app self-hosted, leggera e reattiva per gestire scadenze (bollo, assicurazione, revisione), storico manutenzioni (meccanico, carrozziere, gommista) e spese dei tuoi veicoli. Senza tracciamento di carburante o pedaggi: solo ciò che conta davvero.
![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL_3.0-blue.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)
![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?logo=docker&logoColor=white)
![PWA Ready](https://img.shields.io/badge/PWA-Ready-f08c00?logo=pwa&logoColor=white)
</div>
---
✨ Funzionalità
🚗 Gestione multi-veicolo: Supporto a più mezzi (auto, moto, scooter), ciascuno con nome, targa, note, data di acquisto e data di vendita.
⏱️ Scadenze intelligenti: Conto alla rovescia per assicurazione, bollo, revisione, tagliandi e cambio gomme. Evidenziazione visiva prioritaria delle scadenze in ritardo e della prossima scadenza attiva.
🔁 Rinnovo istantaneo: Il tasto «Rinnova» archivia il pagamento nello storico delle spese e sposta automaticamente in avanti la data di scadenza (es. +12 mesi).
🧾 Fatture e allegati: Caricamento di ricevute, fatture o foto (PDF, PNG, JPG, WebP) associate a interventi e scadenze.
🛠️ Rubrica officine e compagnie: Auto-popolamento di officine, carrozzerie e assicurazioni durante l'inserimento, gestibili e modificabili dalla sezione Impostazioni.
📊 Statistiche e grafici: Panoramica delle spese dell'anno in corso con grafico a barre mensile e diagramma a ciambella suddiviso per categoria di costo.
📱 Progressive Web App (PWA): Installabile direttamente come applicazione autonoma su smartphone e desktop.
💾 Backup & Restore integrato: Esportazione con un clic dell'intero archivio (database SQLite + tutti i file allegati) in formato `.zip` e ripristino istantaneo via interfaccia.
🎨 Personalizzazione: Scelta rapida o libera del colore d'accento con adattamento automatico del contrasto e tema scuro/chiaro di sistema.
---
🚀 Avvio rapido con Docker Compose
Il modo più rapido e consigliato per eseguire l'applicazione è tramite `docker-compose`.
1. Clonazione del repository
```bash
git clone https://github.com/rubinog/vehicles.git
cd vehicles
```
2. Avvio del container
```bash
docker compose up -d --build
```
L'applicazione sarà subito accessibile all'indirizzo:
```
http://localhost:38189
```
---
📂 Persistenza e Backup
Tutti i dati permanenti (database SQLite e cartella degli allegati caricati) vengono conservati nella cartella locale `./data`:
```text
vehicles/
├── data/
│   ├── vehicles.db       # Database SQLite
│   └── files/            # Fatture, ricevute e allegati
├── static/               # Frontend PWA (HTML, CSS, JS, manifest)
├── app.py                # Backend Flask
├── Dockerfile
└── docker-compose.yml
```
Metodi di backup
Dall'interfaccia web: Vai su Impostazioni > Dati e Backup e clicca Scarica Backup (.zip) per ottenere uno snapshot completo di database e file. Puoi usare lo stesso menu per effettuare il ripristino.
Da filesystem: È sufficiente copiare o sincronizzare la cartella `./data`.
---
🛠️ Stack tecnologico
Backend: Python 3.12 con Flask e server di produzione Gunicorn.
Database: SQLite3 con modalità WAL (`Write-Ahead Logging`) abilitata per garantire integrità e performance.
Frontend: Single-Page Application pura in Vanilla JavaScript / HTML5 / CSS moderno (zero dipendenze npm, build step o librerie esterne).
---
📄 Licenza
Distribuito con licenza GNU Affero General Public License v3.0 (AGPL-3.0).  
Consulta il file `LICENSE` per maggiori informazioni.
Realizzato da rubinog.