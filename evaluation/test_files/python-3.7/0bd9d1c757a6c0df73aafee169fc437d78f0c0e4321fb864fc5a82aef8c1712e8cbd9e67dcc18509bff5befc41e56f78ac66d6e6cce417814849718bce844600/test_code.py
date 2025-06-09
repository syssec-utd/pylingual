import unittest
from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_code_cell, new_output
from e2xgrader.graders import CodeGrader

class TestCodeGrader(unittest.TestCase):

    def create_autograded_code_cell(self, grade_id: str, points: int=5) -> NotebookNode:
        cell = new_code_cell()
        cell.metadata = {'nbgrader': {'grade': True, 'grade_id': grade_id, 'locked': False, 'points': points, 'schema_version': 3, 'solution': False, 'task': False}}
        return cell

    def test_errored_cell(self):
        cell = self.create_autograded_code_cell('mycell', 10)
        cell.outputs.append(new_output(output_type='error', ename='MyError', evalue='Something went wrong.'))
        grader = CodeGrader()
        (points, max_points) = grader.determine_grade(cell)
        assert points == 0
        assert max_points == 10

    def test_stderrored_cell(self):
        grader = CodeGrader()
        cell = self.create_autograded_code_cell('mycell', 10)
        cell.outputs.append(new_output(output_type='stream', name='stderr'))
        (points, max_points) = grader.determine_grade(cell)
        assert points == 0
        assert max_points == 10

    def test_correctly_formatted_execute_result(self):
        grader = CodeGrader()
        cell = self.create_autograded_code_cell('mycell', 10)
        cell.outputs.append(new_output(output_type='execute_result', data={'text/plain': '5.0'}))
        (points, max_points) = grader.determine_grade(cell)
        assert points == 5
        assert max_points == 10

    def test_incorrectly_formatted_execute_result(self):
        grader = CodeGrader()
        cell = self.create_autograded_code_cell('mycell', 10)
        cell.outputs.append(new_output(output_type='execute_result', data={'text/plain': 'five'}))
        (points, max_points) = grader.determine_grade(cell)
        assert points == max_points
        assert max_points == 10

    def test_correctly_formatted_partial_credit(self):
        grader = CodeGrader()
        cell = self.create_autograded_code_cell('mycell', 10)
        cell.outputs.append(new_output(output_type='stream', name='stdout', text='### BEGIN GRADE\n5.0\n### END GRADE\n'))
        (points, max_points) = grader.determine_grade(cell)
        assert points == 5
        assert max_points == 10

    def test_incorrectly_formatted_partial_credit(self):
        grader = CodeGrader()
        cell = self.create_autograded_code_cell('mycell', 10)
        cell.outputs.append(new_output(output_type='stream', name='stdout', text='### BEGIN GRADE\nfive\n### END GRADE\n'))
        (points, max_points) = grader.determine_grade(cell)
        assert points is max_points
        assert max_points == 10