import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import MODEL, VALID_PROJECTS, INVALID_PROJECTS, _is_generic_project_title, _is_valid_project, dashboard

class TestV8Model(unittest.TestCase):
    def test_project_counts_and_source_titles(self):
        self.assertEqual(sum(1 for f in MODEL["files"] if f.get("period", "2026-1") == "2026-1"), 26)
        cohort_period = {c["id"]: c["period"] for c in MODEL["cohorts"]}
        valid_2026_1 = [p for p in MODEL["projects"] if cohort_period[p["cohort_id"]] == "2026-1" and _is_valid_project(p)]
        invalid_2026_1 = [p for p in MODEL["projects"] if cohort_period[p["cohort_id"]] == "2026-1" and not _is_valid_project(p)]
        self.assertEqual(len(valid_2026_1), 154)
        self.assertEqual(len(invalid_2026_1), 8)
        self.assertEqual(sum(1 for p in valid_2026_1 if _is_generic_project_title(p.get("title"))), 58)

    def test_dashboard_institutional_kpis(self):
        d = dashboard({"period":"2026-1","program":"","semester":"","section":"","group":"","teacher":"","subject":""})
        k = d["kpis"]
        self.assertEqual(k["projects"], 154)
        self.assertEqual(k["students"], 726)
        self.assertEqual(k["teachers"], 77)
        self.assertEqual(k["subjects"], 36)
        self.assertEqual(k["sections"], 26)
        self.assertEqual(round(k["avg_final"], 2), 4.08)
        self.assertEqual(round(k["avg_final_weighted"], 2), 4.11)
        self.assertEqual(k["coverage"], 100.0)

    def test_subject_filter_is_dynamic(self):
        base = dashboard({"period":"2026-1","program":"","semester":"","section":"","group":"","teacher":"","subject":""})
        subject = base["subject_avg"][0]["name"]
        filtered = dashboard({"period":"2026-1","program":"","semester":"","section":"","group":"","teacher":"","subject":subject})
        self.assertEqual(filtered["kpis"]["subjects"], 1)
        self.assertLess(filtered["kpis"]["subjects"], base["kpis"]["subjects"])

if __name__ == "__main__":
    unittest.main()
