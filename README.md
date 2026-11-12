# Game Translator

[![GitHub Pages](https://github.com/tzayadet/GameTranslator/actions/workflows/pages.yml/badge.svg)](https://github.com/tzayadet/GameTranslator/actions/workflows/pages.yml)
[![Python checks](https://github.com/tzayadet/GameTranslator/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/GameTranslator/actions/workflows/python-syntax.yml)

**Project showcase:** [Open the project page](https://tzayadet.github.io/GameTranslator/) · [Showcase source](docs/index.html)

Herramienta Python de escritorio y CLI para localizar diálogos de videojuegos a partir de archivos de texto reconocibles. Puede crear archivos de idioma nuevos o aplicar cambios in-place con copias de seguridad y manifiesto de restauración.

## Características

- Escaneo de directorios y reconocimiento de formatos de localización.
- Traducción local mediante Argos Translate.
- Motor HTTP configurable y modo noop para pruebas.
- Simulación mediante `--dry-run`.
- Creación de copias de seguridad y restauración mediante `--restore`.
- Caché de traducciones para reducir trabajo repetido.
- Conservación de originales cuando la estructura del juego permite añadir un idioma separado.

## Instalación

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
sudo apt install python3-tk
```

## Uso

Interfaz:

```bash
python game_translator.py
```

Simulación sin modificar archivos:

```bash
python game_translator.py --game-dir "/ruta/al/juego" --dry-run
```

Restaurar un parcheo in-place:

```bash
python game_translator.py --game-dir "/ruta/al/juego" --restore
```

La primera descarga del modelo de Argos requiere conexión a Internet. Después, la traducción local puede funcionar sin conexión.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

## Límites y precauciones

La compatibilidad depende de los formatos y estructuras reconocidos. No procesa directamente paquetes binarios propietarios ni archivos cifrados. Conserva una copia externa del directorio del juego y empieza siempre con `--dry-run`.

La página de GitHub Pages es una presentación estática; no ejecuta traducciones ni aloja archivos de juegos. Para publicarla, activa GitHub Pages en **Settings → Pages → Build and deployment → Source → GitHub Actions** y ejecuta el workflow correspondiente.

## Licencia

Consulta [LICENSE](LICENSE).
