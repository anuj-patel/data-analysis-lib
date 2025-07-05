import unittest
import pandas as pd
from stack_survey.survey import Survey
import os

test_xlsx = "test_survey.xlsx"

def make_test_xlsx():
    data = {
        'Q1': ['A', 'B', 'A', 'C', 'A;B', 'B;C'],
        'Q2': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No'],
    }
    df = pd.DataFrame(data)
    df.to_excel(test_xlsx, index=False)

class TestSurvey(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        make_test_xlsx()
        cls.survey = Survey(test_xlsx)

    @classmethod
    def tearDownClass(cls):
        os.remove(test_xlsx)

    def test_display_structure(self):
        self.assertEqual(self.survey.questions, ['Q1', 'Q2'])

    def test_search_question(self):
        self.assertIn('Q1', self.survey.search_question('Q1'))
        self.assertIn('Q2', self.survey.search_question('Q2'))
        self.assertEqual(self.survey.search_question('notfound'), [])

    def test_search_option(self):
        idxs = self.survey.search_option('Q1', 'A')
        self.assertTrue(all(i in idxs for i in [0,2,4]))

    def test_subset_respondents(self):
        df = self.survey.subset_respondents('Q2', 'Yes')
        self.assertEqual(len(df), 3)

    def test_answer_distribution_sc(self):
        dist = self.survey.answer_distribution('Q2')
        self.assertAlmostEqual(dist['Yes'], 0.5)
        self.assertAlmostEqual(dist['No'], 0.5)

    def test_answer_distribution_mc(self):
        dist = self.survey.answer_distribution('Q1', multiple_choice=True)
        self.assertAlmostEqual(dist['A'], 3/8)
        self.assertAlmostEqual(dist['B'], 3/8)
        self.assertAlmostEqual(dist['C'], 2/8)

if __name__ == "__main__":
    unittest.main()
