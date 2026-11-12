import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game_translator import (RunConfig, RunStats, ScannedFile, process_file, restore_from_backup, run, scan_game_dir)


class FakeTranslator:
    def translate(self, text, source_lang):
        return "ES: " + text

    def detect_language(self, sample_text):
        return "en"


class GameTranslatorSafetyTests(unittest.TestCase):
    def test_dry_run_does_not_modify_game_or_create_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            game_dir = Path(tmp)
            source = game_dir / "localization.json"
            original = {f"dialogue_{i}": f"Hello there, this is dialogue number {i}." for i in range(30)}
            source.write_text(json.dumps(original), encoding="utf-8")

            config = RunConfig(
                game_dir=game_dir,
                source_lang="en",
                mode="patch-inplace",
                dry_run=True,
                engine="noop",
            )

            with patch("game_translator.build_translator", return_value=FakeTranslator()):
                with contextlib.redirect_stdout(io.StringIO()):
                    stats = run(config)

            self.assertGreater(stats.files_translated, 0)
            self.assertEqual(json.loads(source.read_text(encoding="utf-8")), original)
            self.assertFalse((game_dir / ".game_translator_cache.json").exists())
            self.assertFalse((game_dir / ".game_translator_manifest.json").exists())
            self.assertFalse((game_dir / "localization.json.bak").exists())

    def test_restore_rejects_backup_outside_game_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            root.mkdir()
            outside = Path(tmp) / "outside.txt"
            outside.write_text("do not overwrite", encoding="utf-8")
            manifest = {"backups": {"safe.txt": "../outside.txt"}}
            (root / ".game_translator_manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )

            with contextlib.redirect_stdout(io.StringIO()):
                restore_from_backup(RunConfig(game_dir=root))

            self.assertEqual(outside.read_text(encoding="utf-8"), "do not overwrite")
            self.assertFalse((root / "safe.txt").exists())

    def test_add_language_does_not_overwrite_existing_translation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            source_dir = root / "tl" / "english"
            target_dir = root / "tl" / "spanish"
            source_dir.mkdir(parents=True)
            target_dir.mkdir(parents=True)
            source = source_dir / "dialogue.json"
            target = target_dir / "dialogue.json"
            source.write_text(json.dumps({"line": "Hello there"}), encoding="utf-8")
            target.write_text(json.dumps({"line": "Traducción humana"}), encoding="utf-8")

            config = RunConfig(game_dir=root, mode="add-language")
            scanned = ScannedFile(
                path=source,
                kind="json",
                lang_hint="en",
                lang_hint_folder="english",
            )
            stats = RunStats()

            with contextlib.redirect_stdout(io.StringIO()):
                process_file(
                    scanned,
                    config,
                    lambda text: "Traducción automática",
                    {"backups": {}},
                    stats,
                    target_path=target,
                )

            self.assertEqual(
                json.loads(target.read_text(encoding="utf-8")),
                {"line": "Traducción humana"},
            )
            self.assertEqual(stats.files_skipped, 1)

    def test_scanner_skips_symbolic_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            root.mkdir()
            outside = Path(tmp) / "outside.txt"
            outside.write_text("Hello dialogue", encoding="utf-8")
            link = root / "dialogue.txt"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("Symbolic links are not available in this environment")

            results = scan_game_dir(root)
            self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
