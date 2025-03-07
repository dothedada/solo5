import unittest
from app.task import Task


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task(
            {
                "id": 1,
                "task": "Finish report",
                "done": False,
                "important": True,
                "invalid_key": "should be ignored",
            }
        )

    def test_init_assigns_allowed_keys(self):
        self.assertTrue(hasattr(self.task, "task"))
        self.assertEqual(self.task.task, "Finish report")

    def test_init_ignores_invalid_keys(self):
        self.assertFalse(hasattr(self.task, "invalid_key"))

    def test_update_properties_updates_allowed_keys(self):
        self.task.update_properties(task="Updated task", important=False)
        self.assertEqual(self.task.task, "Updated task")
        self.assertFalse(self.task.important)

    def test_update_properties_ommit_the_id_update(self):
        self.task.update_properties(id=2)
        self.assertEqual(1, self.task.id)

    def test_mark_done_sets_done_to_true(self):
        self.task.mark_done()
        self.assertTrue(self.task.done)

    def test_mark_done_returns_self(self):
        self.assertIs(self.task.mark_done(), self.task)

    def test_mark_not_done_sets_done_to_false(self):
        self.task.mark_done()
        self.task.mark_not_done()
        self.assertFalse(self.task.done)

    def test_mark_not_done_returns_self(self):
        self.assertIs(self.task.mark_not_done(), self.task)

    def test_repr_includes_all_attributes(self):
        repr_output = repr(self.task)
        self.assertIn("task: Finish report", repr_output)
        self.assertIn("done: False", repr_output)
        self.assertIn("important: True", repr_output)  # Verifica más atributos

    def test_repr_starts_with_task_class_name(self):
        repr_output = repr(self.task)
        self.assertTrue(repr_output.startswith("Task {"))

    def test_update_properties_ignores_invalid_keys(self):  # Corrige el nombre
        self.task.update_properties(invalid_key="new value")
        self.assertFalse(hasattr(self.task, "invalid_key"))

    def test_init_raise_error_if_no_id_or_task_keys_are_passed(self):
        task_a = {"id": 1, "invalid_key": "value"}
        task_b = {"task": "some shit", "invalid_key": "value"}
        task_c = {"invalid_key": "value"}

        with self.assertRaises(TypeError):
            Task(task_a)
        with self.assertRaises(TypeError):
            Task(task_b)
        with self.assertRaises(TypeError):
            Task(task_c)

    def test_init_empty_task_raises_type_error(self):
        with self.assertRaises(TypeError):
            Task({})

    def test_update_properties_with_empty_dict_does_nothing(self):
        self.task.update_properties()
        self.assertEqual(self.task.task, "Finish report")

    def test_update_properties_with_empty_dict_returns_self(self):
        self.assertIs(self.task.update_properties(), self.task)

    def test_multiple_operations_maintain_consistency(self):
        self.task.update_properties(task="Updated task").mark_done()
        self.assertTrue(self.task.done)
        self.assertEqual(self.task.task, "Updated task")
        self.assertTrue(self.task.important)

    def test_multiple_operations_do_not_corrupt_state(self):
        self.task.mark_not_done().update_properties(important=False)
        self.assertFalse(self.task.done)
        self.assertFalse(self.task.important)
        self.assertEqual(self.task.task, "Finish report")


if __name__ == "__main__":
    unittest.main()
