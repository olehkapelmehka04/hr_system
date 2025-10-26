import unittest

from app.models import Candidate, HrBase, Menu


class TestCandidate(unittest.TestCase):
    def setUp(self):
        self.candidate = Candidate("Дударь Олег Николаевич", 21, "ol@mail.ru")

    def test_edit_candidate(self):
        self.assertEqual(
            self.candidate.edit_candidate("Дударь Максим Николаевич", 1), "ФИО изменено"
        )
        self.assertEqual(self.candidate.full_name, "Дударь Максим Николаевич")
        self.assertEqual(self.candidate.edit_candidate(35, 2), "Возраст изменен")
        self.assertEqual(self.candidate.age, 35)
        self.assertEqual(
            self.candidate.edit_candidate("new_email@mail.ru", 3), "Почта изменена"
        )
        self.assertEqual(self.candidate.email, "new_email@mail.ru")
        self.assertEqual(self.candidate.edit_candidate("hired", 4), "Статус изменен")
        self.assertEqual(self.candidate.status, "hired")
        with self.assertRaises(ValueError):
            self.candidate.edit_candidate("test", 5)

    def test_str(self):
        s = str(self.candidate)
        self.assertIn("Дударь Олег Николаевич", s)
        self.assertIn("21", s)
        self.assertIn("ol@mail.ru", s)


class TestHrBase(unittest.TestCase):
    def setUp(self):
        self.base = HrBase()
        self.candidate = Candidate("Дударь Олег Николаевич", 21, "ol@mail.ru")
        self.base.add_condidate(self.candidate)

    def test_add_and_find(self):
        self.assertEqual(len(self.base.local_base), 1)
        found = self.base.find_candidate_by_id(self.candidate.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.full_name, "Дударь Олег Николаевич")

    def test_get_all_candidates(self):
        all_candidates = self.base.get_all_candidates()
        self.assertIn("Дударь Олег Николаевич", all_candidates)

    def test_filter_candidate(self):
        result = self.base.filter_candidate("new")
        self.assertIn("Дударь Олег Николаевич", result)
        self.assertIsNone(self.base.filter_candidate("nonexistent_status"))

    def test_del_candidate(self):
        self.base.del_candidate(self.candidate)
        self.assertEqual(len(self.base.local_base), 0)


if __name__ == "__main__":
    unittest.main()
