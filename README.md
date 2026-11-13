<p align="center">
  <img src="https://img.shields.io/badge/LOCALIZATION-GAME_TRANSLATOR-101010?style=for-the-badge&labelColor=050805&color=00FF41" alt="Game Translator"/>
  <img src="https://img.shields.io/badge/PYTHON-DESKTOP_%2F_CLI-101010?style=for-the-badge&logo=python&logoColor=00FF41" alt="Python"/>
</p>

# Game Translator

Python desktop and CLI toolkit for localising supported game text files. It can create separate language files or apply in-place changes with backups and a restoration manifest.

<p align="center">
  <a href="https://tzayadet.github.io/GameTranslator/"><strong>LIVE DEMO ↗</strong></a> ·
  <a href="https://github.com/tzayadet/GameTranslator"><strong>SOURCE CODE</strong></a>
</p>

[![GitHub Pages](https://github.com/tzayadet/GameTranslator/actions/workflows/pages.yml/badge.svg)](https://github.com/tzayadet/GameTranslator/actions/workflows/pages.yml) · [![Python checks](https://github.com/tzayadet/GameTranslator/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/GameTranslator/actions/workflows/python-syntax.yml)

## Features

- Scans directories and recognises supported localisation formats.
- Performs local translation through Argos Translate.
- Supports a configurable HTTP engine and a no-op mode for tests.
- Provides `--dry-run` previews.
- Creates backups and supports restoration through `--restore`.
- Caches translations to reduce repeated work.
- Preserves original files when a game supports separate language files.

## Install

```bash
python -m venv .venv
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Linux**
```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
sudo apt install python3-tk
```

## Run

Desktop interface:

```bash
python game_translator.py
```

Preview changes without modifying files:

```bash
python game_translator.py --game-dir "/path/to/game" --dry-run
```

Restore an in-place patch:

```bash
python game_translator.py --game-dir "/path/to/game" --restore
```

The first Argos model download requires an Internet connection. Once installed, local translation can work offline.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Scope and precautions

Compatibility depends on the supported file formats and game structures. The tool does not directly process proprietary binary packages or encrypted files. Keep an external backup of the game directory and start with `--dry-run`.

## Showcase and deployment

The [GitHub Pages showcase](https://tzayadet.github.io/GameTranslator/) is a static project page. It does not execute translations or host game files. Pages deployment is defined in `.github/workflows/pages.yml`.

## License

See [LICENSE](LICENSE).
