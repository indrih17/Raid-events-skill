import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_route import generate, validate
from compare_results import compare, number
from extract_action import extract
from check_repository import check_skill

ASSETS = Path(__file__).resolve().parents[2] / "assets"


class SkillTests(unittest.TestCase):
    def test_real_skill_frontmatter(self):
        self.assertEqual(check_skill(ASSETS.parent / "SKILL.md"), [])


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((ASSETS / "guillotine-observations.json").read_text(encoding="utf-8"))

    def test_historical_ratios_and_damage_delta(self):
        result = compare(self.document)
        self.assertAlmostEqual(result["cases"][0]["direct_results_per_execution"], 1.996793550455774)
        self.assertAlmostEqual(result["cases"][1]["direct_results_per_execution"], 0.9982616253802694)
        self.assertAlmostEqual(result["deltas"][0]["damage"]["percent"], -50.63603569394341)
        self.assertAlmostEqual(result["deltas"][0]["num_direct_results"]["absolute"], -43.541)

    def test_zero_denominator_is_undefined(self):
        self.document["cases"][0].update(num_executes=0, num_direct_results=0, damage=0)
        result = compare(self.document)
        self.assertIsNone(result["cases"][0]["direct_results_per_execution"])
        self.assertIsNone(result["deltas"][0]["damage"]["percent"])

    def test_sample_mean_not_sum(self):
        self.assertEqual(number({"mean": 2, "sum": 200}, "x"), 2)
        with self.assertRaises(ValueError):
            number({"sum": 200}, "x")

    def test_reject_bad_numbers(self):
        for value in (-1, float("nan"), float("inf"), True, "43.662", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                number(value, "x")

    def test_missing_counter_not_zero(self):
        del self.document["cases"][0]["num_direct_results"]
        with self.assertRaises(ValueError):
            compare(self.document)

    def test_reject_incompatible_scopes(self):
        for field in ("owner", "action", "damage_scope"):
            doc = copy.deepcopy(self.document)
            doc["cases"][1][field] = "different"
            with self.subTest(field=field), self.assertRaises(ValueError):
                compare(doc)

    def test_duplicate_labels(self):
        self.document["cases"][1]["label"] = self.document["cases"][0]["label"]
        with self.assertRaises(ValueError):
            compare(self.document)


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((ASSETS / "example-timeline.json").read_text(encoding="utf-8"))

    def test_exact_windows_and_boss_classification(self):
        text = generate(self.document, exact=True)
        adds = [line for line in text.splitlines() if line.startswith("raid_events+=/adds")]
        self.assertEqual(len(adds), 5)
        self.assertEqual(sum("type=add_boss" in line for line in adds), 1)
        self.assertIn("name=TrashA_P01,timestamps=5", text)
        self.assertIn("duration=30,duration_min=30,duration_max=30", text)
        self.assertNotIn("duration_stddev=1", text)

    def test_default_retains_route_jitter(self):
        text = generate(self.document)
        self.assertEqual(text.count(",duration_stddev=1"), 5)

    def test_chain_pull_duplicate_guid_rejected(self):
        duplicate = copy.deepcopy(self.document["targets"][0])
        duplicate["pull"] = 2
        self.document["targets"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "duplicate GUID"):
            generate(self.document)

    def test_identical_names_collide(self):
        self.document["targets"][1]["name"] = self.document["targets"][0]["name"]
        with self.assertRaisesRegex(ValueError, "collision"):
            validate(self.document)

    def test_invalid_windows(self):
        for start, end in ((10, 10), (12, 5), (-1, 2), (200, 301)):
            doc = copy.deepcopy(self.document)
            doc["targets"][0].update(start=start, end=end)
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                generate(doc)

    def test_no_code_injection(self):
        self.document["targets"][0]["name"] = "Trash,raid_events=/stun"
        with self.assertRaises(ValueError):
            generate(self.document)
        self.document["targets"][0]["name"] = "Trash"
        self.document["targets"][0]["evidence"] = "line\nraid_events=/stun"
        with self.assertRaises(ValueError):
            generate(self.document)

    def test_bloodlust_order_and_bounds(self):
        for timestamps in ([60, 60], [80, 20], [300], [-1]):
            doc = copy.deepcopy(self.document)
            doc["bloodlust"] = timestamps
            with self.subTest(timestamps=timestamps), self.assertRaises(ValueError):
                generate(doc)

    def test_long_route_dummy_is_one_start(self):
        self.document["duration"] = 6000
        text = generate(self.document, exact=True)
        self.assertIn("timestamps=0,cooldown=6001,duration=6001", text)
        self.assertIn("duration_min=6001,duration_max=6001", text)

    def test_requires_provenance(self):
        del self.document["targets"][0]["evidence"]
        with self.assertRaises(ValueError):
            generate(self.document)


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.row = {"name": "perfected_guillotine", "id": 1306624,
                    "num_executes": {"mean": 43.662}, "num_direct_results": {"mean": 87.184},
                    "actual_amount": {"mean": 10000000}, "compound_amount": 10534000,
                    "children": [{"name": "venomfang", "num_executes": 87.184,
                                  "num_direct_results": 87.184, "actual_amount": 534000,
                                  "compound_amount": 534000}]}
        self.report = {"sim": {"players": [{"name": "Player", "stats": [self.row]}]}}

    def test_parent_damage_scope_is_explicit(self):
        result = extract(self.report, "Player", "perfected_guillotine", "baseline")
        self.assertEqual(result["cases"][0]["damage"], 10000000)
        self.assertEqual(result["cases"][0]["damage_scope"], "actual_amount")
        result = extract(self.report, "Player", "perfected_guillotine", "baseline", "compound_amount")
        self.assertEqual(result["cases"][0]["damage"], 10534000)

    def test_child_found_without_double_count(self):
        result = extract(self.report, "Player", "venomfang", "baseline")
        self.assertEqual(result["cases"][0]["damage"], 534000)
        self.assertIn(".children[0]", result["cases"][0]["source_json_path"])

    def test_ambiguous_action_rejected(self):
        self.report["sim"]["players"][0]["stats"].append(copy.deepcopy(self.row))
        with self.assertRaises(ValueError):
            extract(self.report, "Player", "perfected_guillotine", "x")

    def test_missing_action_and_player_rejected(self):
        for player, action in (("Other", "perfected_guillotine"), ("Player", "unknown")):
            with self.subTest(player=player, action=action), self.assertRaises(ValueError):
                extract(self.report, player, action, "x")

    def test_unsupported_schema_rejected(self):
        with self.assertRaises(ValueError):
            extract({"players": []}, "Player", "perfected_guillotine", "x")

    def test_omitted_zero_requires_explicit_choice(self):
        del self.row["num_direct_results"]
        with self.assertRaises(ValueError):
            extract(self.report, "Player", "perfected_guillotine", "x")
        result = extract(self.report, "Player", "perfected_guillotine", "x", missing_zero=True)
        self.assertEqual(result["cases"][0]["num_direct_results"], 0)
        self.assertEqual(result["cases"][0]["omitted_fields_assumed_zero"], ["num_direct_results"])

    def test_pet_owner_explicit(self):
        self.report["sim"]["players"][0]["stats_pets"] = {"Pet": [copy.deepcopy(self.row)]}
        result = extract(self.report, "Player", "perfected_guillotine", "x", pet="Pet")
        self.assertEqual(result["cases"][0]["owner"], "Player/pet:Pet")
        self.assertEqual(extract(self.report, "Player", "perfected_guillotine", "x")["cases"][0]["owner"], "Player")


if __name__ == "__main__":
    unittest.main()
