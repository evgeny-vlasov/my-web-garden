import hashlib
import json
import sys
import unittest
import wave
import zipfile
from pathlib import Path
from xml.etree import ElementTree


SITE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SITE_ROOT.parents[1]
if str(SITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SITE_ROOT))

from app import app
from project_library import PROJECTS


SLUG = "escape-from-the-giant-pigeon"
PROJECT = PROJECTS[SLUG]
PACKAGE_ROOT = SITE_ROOT / "static" / "projects" / SLUG
STARTER = PACKAGE_ROOT / f"{SLUG}-starter.sb3"
FINISHED = PACKAGE_ROOT / f"{SLUG}-finished.sb3"
ASSET_PACK = PACKAGE_ROOT / f"{SLUG}-assets.zip"
CONTENT_SOURCE = SITE_ROOT / "scratch_projects" / f"{SLUG}.json"
VENDOR_ROOT = SITE_ROOT / "static" / "vendor" / "scratchblocks"


def load_project(path):
    with zipfile.ZipFile(path) as archive:
        project = json.loads(archive.read("project.json"))
        files = {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
    return project, files


def all_opcodes(project):
    return {
        block["opcode"]
        for target in project["targets"]
        for block in target["blocks"].values()
    }


class ScratchProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()
        cls.starter_project, cls.starter_files = load_project(STARTER)
        cls.finished_project, cls.finished_files = load_project(FINISHED)

    def test_project_page_and_structured_build_sections(self):
        response = self.client.get(f"/projects/{SLUG}")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Start Building", page)
        self.assertIn("Project system sketch", page)
        self.assertIn("scratchblocks-3.7.1.min.js", page)
        self.assertIn("scratch-project.js", page)
        self.assertEqual(page.count("scratch-code-section"), 10)
        for section in PROJECT["code_sections"]:
            self.assertIn(f'id="{section["anchor"]}"', page)
            self.assertIn(section["pseudocode"].splitlines()[0], page)
            self.assertIn(section["teacher_checkpoint"], page)
            for script in section["scripts"]:
                self.assertIn(f'data-script-id="{script["id"]}"', page)
                self.assertIn(script["source"].splitlines()[0], page)
        self.assertIn(PROJECT["trademark_note"], page)

    def test_renderer_is_self_hosted_pinned_and_only_loaded_for_script_page(self):
        page = self.client.get(f"/projects/{SLUG}").get_data(as_text=True)
        self.assertNotIn("cdnjs", page.lower())
        self.assertNotIn("unpkg", page.lower())
        self.assertNotIn("jsdelivr", page.lower())
        self.assertTrue((VENDOR_ROOT / "scratchblocks-3.7.1.min.js").is_file())
        self.assertGreater((VENDOR_ROOT / "scratchblocks-3.7.1.min.js").stat().st_size, 100_000)
        self.assertIn("Permission is hereby granted", (VENDOR_ROOT / "LICENSE.txt").read_text(encoding="utf-8"))
        ordinary_page = self.client.get("/projects/attack-of-the-angry-snowballs").get_data(as_text=True)
        self.assertNotIn("scratchblocks-3.7.1.min.js", ordinary_page)

    def test_download_links_routes_files_sizes_and_mime_types(self):
        page = self.client.get(f"/projects/{SLUG}").get_data(as_text=True)
        expected_mime = {".sb3": "application/x.scratch.sb3", ".zip": "application/zip"}
        for download in PROJECT["downloads"]:
            with self.subTest(filename=download["filename"]):
                path = PACKAGE_ROOT / download["filename"]
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)
                self.assertIn(download["url"], page)
                self.assertIn(download["label"], page)
                self.assertIn(download["file_type"], page)
                self.assertIn(download["purpose"], page)
                self.assertIn(f'{path.stat().st_size / 1024:.1f} KB', page)
                response = self.client.get(download["url"])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content_type, expected_mime[path.suffix])
                self.assertIn("attachment", response.headers["Content-Disposition"])
                self.assertEqual(len(response.data), path.stat().st_size)
                response.close()
        self.assertEqual(self.client.get(f"/projects/{SLUG}/downloads/not-a-file.sb3").status_code, 404)

    def test_sb3_archives_have_valid_json_and_hashed_assets(self):
        for package_path, project, files in (
            (STARTER, self.starter_project, self.starter_files),
            (FINISHED, self.finished_project, self.finished_files),
        ):
            with self.subTest(package=package_path.name):
                self.assertTrue(zipfile.is_zipfile(package_path))
                self.assertIn("project.json", files)
                self.assertEqual(project["meta"]["semver"], "3.0.0")
                for target in project["targets"]:
                    for asset in target["costumes"] + target["sounds"]:
                        filename = asset["md5ext"]
                        self.assertIn(filename, files)
                        self.assertEqual(filename.split(".", 1)[0], asset["assetId"])
                        self.assertEqual(hashlib.md5(files[filename]).hexdigest(), asset["assetId"])

    def test_starter_and_finished_are_intentionally_different(self):
        self.assertNotEqual(hashlib.sha256(STARTER.read_bytes()).digest(), hashlib.sha256(FINISHED.read_bytes()).digest())
        starter_opcodes = all_opcodes(self.starter_project)
        finished_opcodes = all_opcodes(self.finished_project)
        for completed_opcode in ("motion_changexby", "motion_pointtowards", "sensing_touchingobject", "event_whenkeypressed"):
            self.assertNotIn(completed_opcode, starter_opcodes)
            self.assertIn(completed_opcode, finished_opcodes)
        starter_blocks = sum(len(target["blocks"]) for target in self.starter_project["targets"])
        finished_blocks = sum(len(target["blocks"]) for target in self.finished_project["targets"])
        self.assertGreater(finished_blocks, starter_blocks * 2)
        comments = " ".join(comment["text"] for target in self.starter_project["targets"] for comment in target["comments"].values())
        self.assertIn("STARTER", comments)
        self.assertIn("Build movement", comments)

    def test_finished_targets_variables_costumes_sounds_and_opcodes(self):
        stage = self.finished_project["targets"][0]
        self.assertTrue(stage["isStage"])
        self.assertEqual([target["name"] for target in self.finished_project["targets"]], ["Stage", "Safe Zone", "Giant Pigeon", "Player"])
        self.assertEqual({value[0] for value in stage["variables"].values()}, {"Game State", "Panic", "Survival Time", "Pigeon Speed"})
        targets = {target["name"]: target for target in self.finished_project["targets"]}
        self.assertEqual([costume["name"] for costume in targets["Player"]["costumes"]], ["normal", "caught"])
        self.assertEqual([costume["name"] for costume in targets["Giant Pigeon"]["costumes"]], ["wings up", "wings down"])
        self.assertEqual([costume["name"] for costume in targets["Safe Zone"]["costumes"]], ["inactive", "active"])
        self.assertEqual({sound["name"] for target in targets.values() for sound in target["sounds"]}, {"start", "caught", "safe"})
        required_opcodes = {
            "event_whenflagclicked", "event_whenkeypressed", "event_broadcastandwait",
            "control_forever", "control_if", "motion_changexby", "motion_changeyby",
            "motion_setx", "motion_sety", "motion_pointtowards", "motion_movesteps",
            "sensing_keypressed", "sensing_touchingobject", "sensing_distanceto",
            "operator_equals", "operator_not", "data_setvariableto", "sound_playuntildone", "sound_stopallsounds",
        }
        self.assertEqual(required_opcodes - all_opcodes(self.finished_project), set())

    def test_content_source_covers_every_finished_top_level_script(self):
        content = json.loads(CONTENT_SOURCE.read_text(encoding="utf-8"))
        content_scripts = {script["id"] for script in content["scripts"]}
        section_scripts = {
            script_id
            for section in content["code_sections"]
            for script_id in section["script_ids"]
        }
        self.assertEqual(content_scripts, section_scripts)
        self.assertEqual(len(content["code_sections"]), 10)
        for script in content["scripts"]:
            self.assertTrue(script["source"])
            self.assertTrue(script["blocks"])

    def test_original_svg_sources_and_sketch_parse(self):
        required = ["player.svg", "giant-pigeon.svg", "safe-zone.svg", "stage-backdrop.svg"]
        svg_paths = list((PACKAGE_ROOT / "assets").glob("*.svg")) + [PACKAGE_ROOT / "project-sketch.svg"]
        for filename in required:
            self.assertTrue((PACKAGE_ROOT / "assets" / filename).is_file())
        for svg_path in svg_paths:
            with self.subTest(svg=svg_path.name):
                root = ElementTree.parse(svg_path).getroot()
                self.assertTrue(root.tag.endswith("svg"))
                self.assertTrue(any(child.tag.endswith("title") for child in root))
                self.assertTrue(any(child.tag.endswith("desc") for child in root))
        sketch = (PACKAGE_ROOT / "project-sketch.svg").read_text(encoding="utf-8")
        for label in ("A", "B", "C", "D", "E", "F", "CAUGHT", "SAFE"):
            self.assertIn(label, sketch)

    def test_original_wav_sources_parse(self):
        for filename in ("start.wav", "caught.wav", "safe.wav"):
            with self.subTest(wav=filename):
                with wave.open(str(PACKAGE_ROOT / "assets" / filename), "rb") as sound:
                    self.assertEqual(sound.getnchannels(), 1)
                    self.assertEqual(sound.getsampwidth(), 2)
                    self.assertEqual(sound.getframerate(), 22050)
                    self.assertGreater(sound.getnframes(), 1000)
                    self.assertLess(sound.getnframes(), 22050)

    def test_asset_pack_opens_and_contains_readable_sources(self):
        self.assertTrue(zipfile.is_zipfile(ASSET_PACK))
        with zipfile.ZipFile(ASSET_PACK) as archive:
            names = set(archive.namelist())
            for filename in (
                "README.txt", "LICENSES.txt", "project-sketch.svg",
                "assets/player.svg", "assets/giant-pigeon.svg", "assets/safe-zone.svg",
                "assets/stage-backdrop.svg", "assets/start.wav", "assets/caught.wav", "assets/safe.wav",
            ):
                self.assertIn(filename, names)
            self.assertIn("Students may redraw", archive.read("README.txt").decode("utf-8"))
            self.assertIn("not affiliated with or endorsed", archive.read("LICENSES.txt").decode("utf-8"))

    def test_art_slot_model_uses_existing_internal_assets(self):
        self.assertEqual(set(PROJECT["art_slots"]), {"cover", "project_sketch", "build", "debug", "boss_level"})
        for role, art in PROJECT["art_slots"].items():
            with self.subTest(role=role):
                self.assertTrue((SITE_ROOT / "static" / art["src"]).is_file())
                self.assertTrue(art["alt"])
                self.assertIn("artwork" if role in {"cover", "project_sketch"} else "slot", art["caption"].lower())


if __name__ == "__main__":
    unittest.main()
