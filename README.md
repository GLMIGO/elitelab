# Elite Lab Pro — Plataforma de Análise de Apostas

Plataforma de análise estatística de futebol com modelos Poisson + Dixon-Coles.

## Como usar

Acede directamente em: **https://SEU-USERNAME.github.io/elitelab/**

## Actualização automática

As classificações actualizam-se **todos os dias às 08:00** (hora de Portugal) via GitHub Actions.
Podes também forçar uma actualização manual em: Actions → Actualizar Classificações → Run workflow

## Estrutura

- `index.html` — plataforma completa
- `actualizar.py` — script que vai buscar dados ao Sofascore
- `.github/workflows/actualizar.yml` — agenda de actualização automática
