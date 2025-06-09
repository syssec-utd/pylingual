from unittest import TestCase
import responses
from requests import Session
from ...controllers import TextsController
from ...models import Project, ProjectTypes
from ...utils.response import DoccanoAPIError
from .mock_api_responses import bad
from .mock_api_responses import texts as mocks

class TextsControllerTest(TestCase):

    def setUp(self) -> None:
        self.project = Project(name='my_project', description='Project description', project_type=ProjectTypes.SEQ2SEQ)
        self.texts_controller = TextsController(example_id=123, project=self.project, example_url='http://api/v1/projects/123/examples/123', client_session=Session())

    @responses.activate
    def test_all(self) -> None:
        responses.add(mocks.texts_get_response)
        text_controllers = list(self.texts_controller.all())
        expected_texts_id_map = {text_json['id']: text_json for text_json in mocks.texts_get_json}
        for text_controller in text_controllers:
            text_id = text_controller.id
            text = text_controller.text
            self.assertIn(text_id, expected_texts_id_map)
            self.assertEqual(text.text, expected_texts_id_map[text_id]['text'])
            self.assertEqual(text.prob, expected_texts_id_map[text_id]['prob'])
        self.assertEqual(len(text_controllers), len(mocks.texts_get_json))

    @responses.activate
    def test_all_with_bad_response(self) -> None:
        responses.add(bad.bad_get_response)
        with self.assertRaises(DoccanoAPIError):
            list(self.texts_controller.all())