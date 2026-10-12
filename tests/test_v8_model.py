import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import MODEL, VALID_PROJECTS, INVALID_PROJECTS, _is_generic_project_title, dashboard

class TestV8Model(unittest.TestCase):
    def test_project_counts_and_source_titles(self):
        self.assertEqual(len(MODEL["files"]), 26)
        self.assertEqual(len(VALID_PROJECTS), 154)
        self.assertEqual(len(INVALID_PROJECTS), 8)
        self.assertEqual(sum(1 for p in VALID_PROJECTS if _is_generic_project_title(p.get("title"))), 58)

    def test_dashboard_institutional_kpis(self):
        d = dashboard({"period":"","program":"","semester":"","section":"","group":"","teacher":"","subject":""})
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
        base = dashboard({"period":"","program":"","semester":"","section":"","group":"","teacher":"","subject":""})
        subject = base["subject_avg"][0]["name"]
        filtered = dashboard({"period":"","program":"","semester":"","section":"","group":"","teacher":"","subject":subject})
        self.assertEqual(filtered["kpis"]["subjects"], 1)
        self.assertLess(filtered["kpis"]["subjects"], base["kpis"]["subjects"])

if __name__ == "__main__":
    unittest.main()
