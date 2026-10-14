# Portfolio Stan Hudepohl

Persoonlijke portfolio website als GitHub Page. Een statische site zonder build stap: `index.html`, `style.css` en `script.js`.

## Inhoud
De site laat mijn werk als Cloud Consultant zien, met de browserextensies [FlowKit](https://github.com/StanFV/FlowKit) en [AppKit](https://github.com/StanFV/AppKit), mijn werkervaring en een verwijzing naar de [referentieprojecten bij Bruinsma](https://bruinsmakantoor.nl/ict/projecten/).

## Lokaal bekijken
```
python3 -m http.server 8000
```
Open daarna http://localhost:8000.

## Publiceren
De site wordt gepubliceerd met de GitHub Action in `.github/workflows/pages.yml`. Zet daarvoor in de repository onder **Settings > Pages** de **Source** op "GitHub Actions".

De workflow draait bij elke push naar `main`, elke ochtend automatisch en handmatig via het tabblad **Actions**.

## Referentieprojecten
Bij elke publicatie haalt `scripts/fetch_projects.py` de [projecten-feed van Bruinsma](https://bruinsmakantoor.nl/ict/projecten/feed/) op en schrijft de laatste zes projecten naar `assets/data/projecten.json`. De site toont die als kaarten. Lukt het ophalen niet, dan blijft de vorige versie staan. Is er nog geen data, dan zie je alleen de link naar de projectenpagina.

Lokaal testen kan met `python3 scripts/fetch_projects.py`.
