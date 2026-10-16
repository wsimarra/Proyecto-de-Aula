import unittest
from app.main import STUDENT_CUT_NOTES, students

class TestV91StudentCuts(unittest.TestCase):
    def test_source_cuts_are_loaded(self):
        self.assertGreaterEqual(len(STUDENT_CUT_NOTES), 700)

    def test_student_definitive_is_average_of_two_cuts(self):
        data = students(period='2026-1', semester='SEM-01', section='1')
        row = next(r for r in data['rows'] if r['student'] == 'LUIS JOSE AGUILAR RAMOS' and r['group'] == 'G01')
        self.assertEqual(row['followup2'], 4.2)
        self.assertEqual(row['followup3'], 4.6)
        self.assertEqual(row['definitive'], 4.4)

    def test_all_current_project_participations_have_both_cuts(self):
        rows = students(period='2026-1')['rows']
        self.assertEqual(len(rows), 726)
        self.assertTrue(all(r['followup2'] is not None and r['followup3'] is not None for r in rows))
        self.assertTrue(all(r['definitive'] is not None for r in rows))

if __name__ == '__main__':
    unittest.main()
