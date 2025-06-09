from __future__ import annotations
import pathlib
from typing import Any, Dict, Iterator, List, Literal, Optional
from doccano_client.models.comment import Comment
from doccano_client.models.data_download import Option as DataExportOption
from doccano_client.models.data_upload import Option as DataImportOption
from doccano_client.models.data_upload import Task
from doccano_client.models.example import Example
from doccano_client.models.label import BoundingBox, Category, Relation, Segment, Span, Text
from doccano_client.models.label_type import PREFIX_KEY, SUFFIX_KEY, LabelType
from doccano_client.models.member import Member
from doccano_client.models.metrics import LabelDistribution, MemberProgress, Progress
from doccano_client.models.project import Project
from doccano_client.models.role import Role
from doccano_client.models.task_status import TaskStatus
from doccano_client.models.user import User
from doccano_client.repositories.base import BaseRepository
from doccano_client.repositories.comment import CommentRepository
from doccano_client.repositories.data_download import DataDownloadRepository
from doccano_client.repositories.data_upload import DataUploadRepository
from doccano_client.repositories.example import ExampleRepository
from doccano_client.repositories.label import BoundingBoxRepository, CategoryRepository, RelationRepository, SegmentRepository, SpanRepository, TextRepository
from doccano_client.repositories.label_type import CategoryTypeRepository, RelationTypeRepository, SpanTypeRepository
from doccano_client.repositories.member import MemberRepository
from doccano_client.repositories.metrics import MetricsRepository
from doccano_client.repositories.project import ProjectRepository
from doccano_client.repositories.role import RoleRepository
from doccano_client.repositories.task_status import TaskStatusRepository
from doccano_client.repositories.user import UserRepository
from doccano_client.services.label_type import LabelTypeService
from doccano_client.usecase.comment import CommentUseCase
from doccano_client.usecase.data_download import DataDownloadUseCase
from doccano_client.usecase.data_upload import DataUploadUseCase
from doccano_client.usecase.example import ExampleUseCase
from doccano_client.usecase.label import BoundingBoxUseCase, CategoryUseCase, RelationUseCase, SegmentUseCase, SpanUseCase, TextUseCase
from doccano_client.usecase.label_type import LabelTypeUseCase
from doccano_client.usecase.member import MemberUseCase
from doccano_client.usecase.project import ProjectType, ProjectUseCase

class DoccanoClient:

    def __init__(self, base_url: str, verify: Optional[str | bool]=None):
        """Initialize the client.

        Args:
            base_url (str): The base url of the Doccano instance
            verify (str | bool): Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``. When set to
                ``False``, requests will accept any TLS certificate presented by
                the server, and will ignore hostname mismatches and/or expired
                certificates, which will make your application vulnerable to
                man-in-the-middle (MitM) attacks. Setting verify to ``False``
                may be useful during local development or testing.
        """
        self._base_repository = BaseRepository(base_url, verify=verify)
        self._user_repository = UserRepository(self._base_repository)
        self._role_repository = RoleRepository(self._base_repository)
        self._project_repository = ProjectRepository(self._base_repository)
        self._metrics_repository = MetricsRepository(self._base_repository)
        self._example_repository = ExampleRepository(self._base_repository)
        self._comment_repository = CommentRepository(self._base_repository)
        self._member_repository = MemberRepository(self._base_repository)
        self._category_type_repository = CategoryTypeRepository(self._base_repository)
        self._span_type_repository = SpanTypeRepository(self._base_repository)
        self._relation_type_repository = RelationTypeRepository(self._base_repository)
        self._category_repository = CategoryRepository(self._base_repository)
        self._span_repository = SpanRepository(self._base_repository)
        self._relation_repository = RelationRepository(self._base_repository)
        self._segment_repository = SegmentRepository(self._base_repository)
        self._bounding_box_repository = BoundingBoxRepository(self._base_repository)
        self._text_repository = TextRepository(self._base_repository)
        self._task_status_repository = TaskStatusRepository(self._base_repository)
        self._data_import_repository = DataUploadRepository(self._base_repository)
        self._data_export_repository = DataDownloadRepository(self._base_repository)

    def login(self, username: str, password: str) -> None:
        """Login to a session with the Doccano instance related to the base url.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self._base_repository.login(username, password)

    def logout(self) -> None:
        """Logout from the session."""
        self._base_repository.logout()

    @property
    def project(self) -> ProjectUseCase:
        return ProjectUseCase(self._project_repository)

    @property
    def example(self) -> ExampleUseCase:
        return ExampleUseCase(self._example_repository)

    @property
    def comment(self) -> CommentUseCase:
        return CommentUseCase(self._comment_repository)

    @property
    def category_type(self) -> LabelTypeUseCase:
        service = LabelTypeService(self._category_type_repository)
        return LabelTypeUseCase(self._category_type_repository, service)

    @property
    def span_type(self) -> LabelTypeUseCase:
        service = LabelTypeService(self._span_type_repository)
        return LabelTypeUseCase(self._span_type_repository, service)

    @property
    def relation_type(self) -> LabelTypeUseCase:
        service = LabelTypeService(self._relation_type_repository)
        return LabelTypeUseCase(self._relation_type_repository, service)

    @property
    def data_import(self) -> DataUploadUseCase:
        return DataUploadUseCase(self._data_import_repository, self._task_status_repository)

    @property
    def data_export(self) -> DataDownloadUseCase:
        return DataDownloadUseCase(self._data_export_repository, self._task_status_repository)

    @property
    def member(self) -> MemberUseCase:
        return MemberUseCase(self._member_repository, self._user_repository, self._role_repository)

    @property
    def category(self) -> CategoryUseCase:
        return CategoryUseCase(self._category_repository, self._category_type_repository)

    @property
    def span(self) -> SpanUseCase:
        return SpanUseCase(self._span_repository, self._span_type_repository)

    @property
    def relation(self) -> RelationUseCase:
        return RelationUseCase(self._relation_repository, self._relation_type_repository)

    @property
    def segment(self) -> SegmentUseCase:
        return SegmentUseCase(self._segment_repository, self._category_type_repository)

    @property
    def bounding_box(self) -> BoundingBoxUseCase:
        return BoundingBoxUseCase(self._bounding_box_repository, self._category_type_repository)

    @property
    def text(self) -> TextUseCase:
        return TextUseCase(self._text_repository)

    def _get_label_type_usecase(self, type: Literal['category', 'span', 'relation']) -> LabelTypeUseCase:
        if type == 'category':
            return self.category_type
        elif type == 'span':
            return self.span_type
        elif type == 'relation':
            return self.relation_type
        else:
            raise ValueError(f'Invalid type: {type}')

    def list_roles(self) -> List[Role]:
        """Return all roles.

        Returns:
            List[Role]: The list of roles.
        """
        return self._role_repository.list()

    def get_profile(self) -> User:
        """Return the profile of the logged in user.

        Returns:
            User: The profile of the logged in user.
        """
        return self._user_repository.get_profile()

    def search_users(self, name: str='') -> List[User]:
        """Search users by name.

        Args:
            name (str): The name of the user to search for.

        Returns:
            List[User]: The list of the users.
        """
        return self._user_repository.list(name=name)

    def find_user_by_name(self, name: str) -> User:
        """Find a user by name.

        Args:
            name (str): The name of the user.

        Returns:
            User: The found user.
        """
        return self._user_repository.find_by_name(name)

    def list_projects(self) -> Iterator[Project]:
        """Return all projects in which you are a member.

        Yields:
            Project: The next project.
        """
        yield from self.project.list()

    def find_project_by_id(self, project_id: int) -> Project:
        """Find a project by id.

        Args:
            project_id (int): The id of the project to find.

        Returns:
            Project: The found project.
        """
        return self.project.find_by_id(project_id)

    def get_progress(self, project_id: int) -> Progress:
        """Get the authenticated user's progress.

        Args:
            project_id (int): The id of the project.

        Returns:
            Progress: The user's progress.
        """
        return self._metrics_repository.get_progress(project_id)

    def get_members_progress(self, project_id: int) -> List[MemberProgress]:
        """Return all metricss in which you are a member.

        Args:
            project_id (int): The id of the project.

        Returns:
            List[MemberProgress]: The list of the member progress.
        """
        return self._metrics_repository.get_members_progress(project_id)

    def get_label_distribution(self, project_id: int, type: Literal['category', 'span', 'relation']) -> List[LabelDistribution]:
        """Return label distribution.

        Args:
            project_id (int): The id of the project.
            type (Literal["category", "span", "relation"]): The type of the label.

        Returns:
            LabelDistribution: The label distribution.

        Raises:
            ValueError: If the type is invalid.
        """
        if type == 'category':
            return self._metrics_repository.get_category_distribution(project_id)
        elif type == 'span':
            return self._metrics_repository.get_span_distribution(project_id)
        elif type == 'relation':
            return self._metrics_repository.get_relation_distribution(project_id)
        else:
            raise ValueError(f'Invalid type: {type}')

    def create_project(self, name: str, project_type: ProjectType, description: str, guideline: str='', random_order: bool=False, collaborative_annotation: bool=False, single_class_classification: bool=False, allow_overlapping: bool=False, grapheme_mode: bool=False, use_relation: bool=False, tags: Optional[List[str]]=None) -> Project:
        """Create a new project. `ProjectType` is one of the
        `DocumentClassification`, `SequenceLabeling`, `Seq2seq`, `Speech2text`,
        `ImageClassification`, `BoundingBox`, `Segmentation`, `ImageCaptioning`,
        and `IntentDetectionAndSlotFilling`.

        Args:
            name (str): The name of the project.
            project_type (ProjectType): The type of the project.
            description (str): The description of the project.
            guideline (str): The annotation guideline. Defaults to "".
            random_order (bool): Whether to shuffle the uploaded data. Defaults to False.
            collaborative_annotation (bool): If True, a data can be annotated by multiple users. Defaults to False.
            single_class_classification (bool): If True, only one label can apply a data. Defaults to False.
            allow_overlapping (bool): If True, span overlapping is allowed. Defaults to False.
            grapheme_mode (bool): If True, count multi-byte characters as one character. Defaults to False.
            use_relation (bool): If True, relation labeling is allowed. Defaults to False.
            tags (Optional[List[str]], optional): The tags of the project. Defaults to None.

        Returns:
            Project: The created project.
        """
        return self.project.create(name=name, project_type=project_type, description=description, guideline=guideline, random_order=random_order, collaborative_annotation=collaborative_annotation, single_class_classification=single_class_classification, allow_overlapping=allow_overlapping, grapheme_mode=grapheme_mode, use_relation=use_relation, tags=tags)

    def update_project(self, project_id: int, name: str=None, project_type: ProjectType=None, description: str=None, guideline: str=None, random_order: bool=None, collaborative_annotation: bool=None, single_class_classification: bool=None, allow_overlapping: bool=None, grapheme_mode: bool=None, use_relation: bool=None, tags: Optional[List[str]]=None) -> Project:
        """Update a project. `ProjectType` is one of the
        `DocumentClassification`, `SequenceLabeling`, `Seq2seq`, `Speech2text`,
        `ImageClassification`, `BoundingBox`, `Segmentation`, `ImageCaptioning`,
        and `IntentDetectionAndSlotFilling`.

        Args:
            project_id (int): The project id.
            name (str): The name of the project.
            project_type (ProjectType): The type of the project.
            description (str): The description of the project. Defaults to None.
            guideline (str): The annotation guideline. Defaults to None.
            random_order (bool): Whether to shuffle the uploaded data. Defaults to None.
            collaborative_annotation (bool): If True, a data can be annotated by multiple users. Defaults to None.
            single_class_classification (bool): If True, only one label can apply a data. Defaults to None.
            allow_overlapping (bool): If True, span overlapping is allowed. Defaults to None.
            grapheme_mode (bool): If True, count multi-byte characters as one character. Defaults to None.
            use_relation (bool): If True, relation labeling is allowed. Defaults to None.
            tags (Optional[List[str]], optional): The tags of the project. Defaults to None.

        Returns:
            Project: The updated project.
        """
        return self.project.update(project_id=project_id, name=name, project_type=project_type, description=description, guideline=guideline, random_order=random_order, collaborative_annotation=collaborative_annotation, single_class_classification=single_class_classification, allow_overlapping=allow_overlapping, grapheme_mode=grapheme_mode, use_relation=use_relation, tags=tags)

    def delete_project(self, project_id: int):
        """Delete a project.

        Args:
            project_id (int): The project id.
        """
        self.project.delete(project_id)

    def list_label_types(self, project_id: int, type: Literal['category', 'span', 'relation']) -> List[LabelType]:
        """Return all label types in a project.

        Args:
            project_id (int): The project id.
            type (Literal["category", "span", "relation"]): The type of the label type.

        Returns:
            List[LabelType]: The list of label types.
        """
        return self._get_label_type_usecase(type).list(project_id)

    def find_label_type_by_id(self, project_id: int, label_type_id: int, type: Literal['category', 'span', 'relation']) -> LabelType:
        """Find a label type by id.

        Args:
            project_id (int): The project id.
            label_type_id (int): The label type id.
            type (Literal["category", "span", "relation"]): The type of the label type.

        Returns:
            LabelType: The found label type.
        """
        return self._get_label_type_usecase(type).find_by_id(project_id, label_type_id)

    def create_label_type(self, project_id: int, type: Literal['category', 'span', 'relation'], text: str, prefix_key: PREFIX_KEY=None, suffix_key: SUFFIX_KEY=None, color: Optional[str]=None) -> LabelType:
        """Create a new label type.

        Args:
            project_id (int): The project id.
            type (Literal["category", "span", "relation"]): The type of the label type.
            text (str): The name of the label type.
            prefix_key (PREFIX_KEY): The prefix key of the label type.
            suffix_key (SUFFIX_KEY): The suffix key of the label type.
            color (str): The color of the label type. Defaults to None.

        Returns:
            LabelType: The created label type.
        """
        return self._get_label_type_usecase(type).create(project_id=project_id, text=text, prefix_key=prefix_key, suffix_key=suffix_key, color=color)

    def update_label_type(self, project_id: int, label_type_id: int, type: Literal['category', 'span', 'relation'], text: str=None, prefix_key: PREFIX_KEY | int=-1, suffix_key: SUFFIX_KEY | int=-1, color: str=None) -> LabelType:
        """Update a label type.

        Args:
            project_id (int): The project id.
            label_type_id (int): The label type id.
            type (Literal["category", "span", "relation"]): The type of the label type.
            text (str): The name of the label type.
            prefix_key (PREFIX_KEY): The prefix key of the label type.
            suffix_key (SUFFIX_KEY): The suffix key of the label type.
            color (str): The color of the label type. Defaults to None.

        Returns:
            LabelType: The updated label type.
        """
        return self._get_label_type_usecase(type).update(project_id=project_id, label_type_id=label_type_id, text=text, prefix_key=prefix_key, suffix_key=suffix_key, color=color)

    def delete_label_type(self, project_id: int, label_type_id: int, type: Literal['category', 'span', 'relation']):
        """Delete a label type.

        Args:
            project_id (int): The project id.
            label_type_id (int): The label type id.
            type (Literal["category", "span", "relation"]): The type of the label type.
        """
        self._get_label_type_usecase(type).delete(project_id, label_type_id)

    def bulk_delete_label_types(self, project_id: int, label_type_ids: List[int], type: Literal['category', 'span', 'relation']):
        """Delete multiple label types.

        Args:
            project_id (int): The project id.
            label_type_ids (List[int]): The label type ids.
            type (Literal["category", "span", "relation"]): The type of the label type.
        """
        self._get_label_type_usecase(type).bulk_delete(project_id, label_type_ids)

    def upload_label_type(self, project_id: int, file_path: str, type: Literal['category', 'span', 'relation']):
        """Upload a label type.

        Args:
            project_id (int): The id of the project.
            file_path (str): The path to the file to upload.
            type (Literal["category", "span", "relation"]): The type of the label type.
        """
        self._get_label_type_usecase(type).upload(project_id, file_path)

    def list_examples(self, project_id: int) -> Iterator[Example]:
        """Return all examples.

        Args:
            project_id (int): The id of the project.

        Yields:
            Example: The examples in the project.
        """
        yield from self.example.list(project_id)

    def find_example_by_id(self, project_id: int, example_id: int) -> Example:
        """Find an example by id.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.

        Returns:
            Example: The found example.
        """
        return self.example.find_by_id(project_id, example_id)

    def count_examples(self, project_id: int) -> int:
        """Count the number of examples.

        Args:
            project_id (int): The id of the project.

        Returns:
            int: The number of examples.
        """
        return self.example.count(project_id)

    def create_example(self, project_id: int, text: str, meta: Dict[str, Any]=None) -> Example:
        """Create a new example.

        Args:
            project_id (int): The id of the project.
            text (str): The text of the example.
            meta (Dict[str, Any]): The meta data of the example.

        Returns:
            Example: The created example.
        """
        return self.example.create(project_id, text, meta)

    def update_example(self, project_id: int, example_id: int, text: str=None, meta: Dict[str, Any]=None) -> Example:
        """Update an example.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            text (str): The text of the example.
            meta (Dict[str, Any]): The meta data of the example.

        Returns:
            Example: The updated example.
        """
        return self.example.update(project_id, example_id, text, meta)

    def delete_example(self, project_id: int, example_id: int):
        """Delete an example.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.example.delete(project_id, example_id)

    def bulk_delete_examples(self, project_id: int, example_ids: List[int]):
        """Delete multiple examples.

        Args:
            project_id (int): The id of the project.
            example_ids (List[int]): The ids of the examples.
        """
        self.example.bulk_delete(project_id, example_ids)

    def delete_all_examples(self, project_id: int):
        """Delete all examples.

        Args:
            project_id (int): The id of the project.
        """
        self.example.delete_all(project_id)

    def update_example_state(self, project_id: int, example_id: int):
        """Update the state of an example.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.example.update_state(project_id, example_id)

    def find_comment_by_id(self, project_id: int, comment_id: int) -> Comment:
        """Find a comment by id.

        Args:
            project_id (int): The id of the project.
            comment_id (int): The id of the comment.

        Returns:
            Comment: The found comment.
        """
        return self.comment.find_by_id(project_id, comment_id)

    def list_comments(self, project_id: int, example_id: int, query: str='') -> Iterator[Comment]:
        """Return all comments.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            query (str): The query string to filter comments.

        Yields:
            Comment: The comments in the project.
        """
        yield from self.comment.list(project_id, example_id, query)

    def create_comment(self, project_id: int, example_id: int, text: str) -> Comment:
        """Create a new comment.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            text (str): The text of the comment.

        Returns:
            Comment: The created comment.
        """
        return self.comment.create(project_id, example_id, text)

    def update_comment(self, project_id: int, comment_id: int, text: str) -> Comment:
        """Update a comment.

        Args:
            project_id (int): The id of the project.
            comment_id (int): The id of the comment.
            text (str): The text of the comment.

        Returns:
            Comment: The updated comment.
        """
        return self.comment.update(project_id, comment_id, text)

    def delete_comment(self, project_id: int, comment_id: int):
        """Delete a comment.

        Args:
            project_id (int): The id of the project.
            comment_id (int): The id of the comment.
        """
        self.comment.delete(project_id, comment_id)

    def bulk_delete_comments(self, project_id: int, comment_ids: List[int]):
        """Delete multiple comments.

        Args:
            project_id (int): The id of the project.
            comment_ids (List[int]): The ids of the comments.
        """
        self.comment.bulk_delete(project_id, comment_ids)

    def list_upload_options(self, project_id: int) -> List[DataImportOption]:
        """Return all upload options.

        Args:
            project_id (int): The id of the project.

        Returns:
            List[Option]: The list of the upload options.
        """
        return self.data_import.list_options(project_id)

    def list_download_options(self, project_id: int) -> List[DataExportOption]:
        """Return all download options.

        Args:
            project_id (int): The id of the project.

        Returns:
            List[Option]: The list of the download options.
        """
        return self.data_export.list_options(project_id)

    def upload(self, project_id: int, file_paths: List[str], task: Task, format: str, column_data: str='text', column_label: str='label') -> TaskStatus:
        """Upload a file. `task` is one of the
        `DocumentClassification`, `SequenceLabeling`, `Seq2seq`, `Speech2text`,
        `ImageClassification`, `BoundingBox`, `Segmentation`, `ImageCaptioning`,
        , `IntentDetectionAndSlotFilling`, and `RelationExtraction`.

        Args:
            project_id (int): The id of the project.
            file_paths (List[str]): The list of the file paths.
            task (Task): The task of the upload.
            format (str): The format of the upload.
            column_data (str): The column name of the data.
            column_label (str): The column name of the label.

        Returns:
            TaskStatus: The status of the upload task.
        """
        return self.data_import.upload(project_id, file_paths, task, format, column_data, column_label)

    def download(self, project_id: int, format: str, only_approved=False, dir_name='.') -> pathlib.Path:
        """Download a file.

        Args:
            project_id (int): The id of the project.
            format (str): The format of the download.
            only_approved (bool): Whether to export approved data only.
            dir_name (str): The directory to save the file.

        Returns:
            pathlib.Path: The path to the downloaded file.
        """
        return self.data_export.download(project_id, format, only_approved, dir_name)

    def find_member_by_id(self, project_id: int, member_id: int) -> Member:
        """Find a member by id.

        Args:
            project_id (int): The id of the project to find.
            member_id (int): The id of the member to find.

        Returns:
            Member: The found member.
        """
        return self.member.find_by_id(project_id, member_id)

    def list_members(self, project_id: int) -> List[Member]:
        """Return all members.

        Args:
            project_id (int): The id of the project.

        Returns:
            List[Member]: The members in the project.
        """
        return self.member.list(project_id)

    def add_member(self, project_id: int, username: str, role_name: str) -> Member:
        """Create a new member.

        Args:
            project_id (int): The id of the project.
            username (str): The username of the future member.
            role_name (str): The role of the future member.

        Returns:
            Member: The created member.
        """
        return self.member.add(project_id, username, role_name)

    def update_member(self, project_id: int, member_id: int, role_name: str) -> Member:
        """Update a member role.

        Args:
            project_id (int): The id of the project.
            member_id (int): The id of the member.
            role_name (str): The role of the member.

        Returns:
            Member: The updated member.
        """
        return self.member.update(project_id, member_id, role_name)

    def delete_member(self, project_id: int, member_id: int):
        """Delete a member.

        Args:
            project_id (int): The id of the project.
            member_id (int): The id of the member.
        """
        self.member.delete(project_id, member_id)

    def bulk_delete_members(self, project_id: int, member_ids: List[int]):
        """Delete multiple members.

        Args:
            project_id (int): The id of the project.
            member_ids (List[int]): The ids of the members.
        """
        self.member.bulk_delete(project_id, member_ids)

    def find_category_by_id(self, project_id: int, example_id: int, label_id: int) -> Category:
        """Find a category by id.

        Args:
            project_id (int): The id of the project to find.
            example_id (int): The id of the example.
            label_id (int): The id of the label to find.

        Returns:
            Category: The found category.
        """
        return self.category.find_by_id(project_id, example_id, label_id)

    def find_span_by_id(self, project_id: int, example_id: int, label_id: int) -> Span:
        """Find a span by id.

        Args:
            project_id (int): The id of the project to find.
            example_id (int): The id of the example.
            label_id (int): The id of the label.

        Returns:
            Span: The found span.
        """
        return self.span.find_by_id(project_id, example_id, label_id)

    def find_relation_by_id(self, project_id: int, example_id: int, label_id: int) -> Relation:
        """Find a relation by id.

        Args:
            project_id (int): The id of the project to find.
            example_id (int): The id of the example.
            label_id (int): The id of the label.

        Returns:
            Relation: The found relation.
        """
        return self.relation.find_by_id(project_id, example_id, label_id)

    def find_text_by_id(self, project_id: int, example_id: int, label_id: int) -> Text:
        """Find a text by id.

        Args:
            project_id (int): The id of the project to find.
            example_id (int): The id of the example.
            label_id (int): The id of the label.

        Returns:
            Text: The found text.
        """
        return self.text.find_by_id(project_id, example_id, label_id)

    def find_segment_by_id(self, project_id: int, example_id: int, label_id: int) -> Segment:
        """Find a segment by id.

        Args:
            project_id (int): The id of the project to find.
            example_id (int): The id of the example.
            label_id (int): The id of the label.

        Returns:
            Segment: The found segment.
        """
        return self.segment.find_by_id(project_id, example_id, label_id)

    def find_bounding_box_by_id(self, project_id: int, example_id: int, label_id: int) -> BoundingBox:
        """Find a bounding box by id.

        Args:
            project_id (int): The id of the project to find.
            example_id (int): The id of the example.
            label_id (int): The id of the label.

        Returns:
            BoundingBox: The found bounding box.
        """
        return self.bounding_box.find_by_id(project_id, example_id, label_id)

    def list_categories(self, project_id: int, example_id: int) -> List[Category]:
        """Return all categories.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.

        Returns:
            List[Category]: The categories in the project.
        """
        return self.category.list(project_id, example_id)

    def list_spans(self, project_id: int, example_id: int) -> List[Span]:
        """Return all spans.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.

        Returns:
            List[Span]: The spans in the project.
        """
        return self.span.list(project_id, example_id)

    def list_relations(self, project_id: int, example_id: int) -> List[Relation]:
        """Return all relations.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.

        Returns:
            List[Relation]: The relations in the project.
        """
        return self.relation.list(project_id, example_id)

    def list_texts(self, project_id: int, example_id: int) -> List[Text]:
        """Return all texts.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.

        Returns:
            List[Text]: The texts in the project.
        """
        return self.text.list(project_id, example_id)

    def list_segments(self, project_id: int, example_id: int) -> List[Segment]:
        """Return all segments.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.

        Returns:
            List[Segment]: The segments in the project.
        """
        return self.segment.list(project_id, example_id)

    def list_bounding_boxes(self, project_id: int, example_id: int) -> List[BoundingBox]:
        """Return all bounding boxes.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.

        Returns:
            List[BoundingBox]: The bounding boxes in the project.
        """
        return self.bounding_box.list(project_id, example_id)

    def delete_category(self, project_id: int, example_id: int, label_id: int):
        """Delete a category.

        Args:
            project_id (int): The project id.
            example_id (int): The id of the example.
            label_id (int): The label id.
        """
        self.category.delete(project_id, example_id, label_id)

    def delete_span(self, project_id: int, example_id: int, label_id: int):
        """Delete a span.

        Args:
            project_id (int): The project id.
            example_id (int): The id of the example.
            label_id (int): The label id.
        """
        self.span.delete(project_id, example_id, label_id)

    def delete_relation(self, project_id: int, example_id: int, label_id: int):
        """Delete a relation.

        Args:
            project_id (int): The project id.
            example_id (int): The id of the example.
            label_id (int): The label id.
        """
        self.relation.delete(project_id, example_id, label_id)

    def delete_text(self, project_id: int, example_id: int, label_id: int):
        """Delete a text.

        Args:
            project_id (int): The project id.
            example_id (int): The id of the example.
            label_id (int): The label id.
        """
        self.text.delete(project_id, example_id, label_id)

    def delete_segment(self, project_id: int, example_id: int, label_id: int):
        """Delete a segment.

        Args:
            project_id (int): The project id.
            example_id (int): The id of the example.
            label_id (int): The label id.
        """
        self.segment.delete(project_id, example_id, label_id)

    def delete_bounding_box(self, project_id: int, example_id: int, label_id: int):
        """Delete a bounding box.

        Args:
            project_id (int): The project id.
            example_id (int): The id of the example.
            label_id (int): The label id.
        """
        self.bounding_box.delete(project_id, example_id, label_id)

    def delete_all_categories(self, project_id: int, example_id: int):
        """Delete all categories.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.category.delete_all(project_id, example_id)

    def delete_all_spans(self, project_id: int, example_id: int):
        """Delete all spans.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.span.delete_all(project_id, example_id)

    def delete_all_relations(self, project_id: int, example_id: int):
        """Delete all relations.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.relation.delete_all(project_id, example_id)

    def delete_all_texts(self, project_id: int, example_id: int):
        """Delete all texts.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.text.delete_all(project_id, example_id)

    def delete_all_segments(self, project_id: int, example_id: int):
        """Delete all segments.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.segment.delete_all(project_id, example_id)

    def delete_all_bounding_boxes(self, project_id: int, example_id: int):
        """Delete all bounding boxes.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
        """
        self.bounding_box.delete_all(project_id, example_id)

    def create_category(self, project_id: int, example_id: int, label: int | str, human_annotated=False, confidence=0.0) -> Category:
        """Create a new category label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Category: The created category label.
        """
        return self.category.create(project_id, example_id, label, human_annotated, confidence)

    def create_span(self, project_id: int, example_id: int, start_offset: int, end_offset: int, label: int | str, human_annotated: bool=False, confidence: float=0.0) -> Span:
        """Create a new span label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            start_offset (int): The start offset of the span.
            end_offset (int): The end offset of the span.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Span: The created span label.
        """
        return self.span.create(project_id, example_id, start_offset, end_offset, label, human_annotated, confidence)

    def create_relation(self, project_id: int, example_id: int, from_id: int, to_id: int, label: int | str, human_annotated: bool=False, confidence: float=0.0) -> Relation:
        """Create a new relation label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            from_id (int): The id of the from span.
            to_id (int): The id of the to span.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Relation: The created relation label.
        """
        return self.relation.create(project_id, example_id, from_id, to_id, label, human_annotated, confidence)

    def create_text(self, project_id: int, example_id: int, text: str, human_annotated: bool=False, confidence: float=0.0) -> Text:
        """Create a new text label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            text (str): The text to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Text: The created text label.
        """
        return self.text.create(project_id, example_id, text, human_annotated, confidence)

    def create_bounding_box(self, project_id: int, example_id: int, x: float, y: float, width: float, height: float, label: int | str, human_annotated: bool=False, confidence: float=0.0) -> BoundingBox:
        """Create a new bounding box label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            x (float): The x coordinate of the bounding box.
            y (float): The y coordinate of the bounding box.
            width (float): The width of the bounding box.
            height (float): The height of the bounding box.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            BoundingBox: The created bounding box label.
        """
        return self.bounding_box.create(project_id, example_id, x, y, width, height, label, human_annotated, confidence)

    def create_segment(self, project_id: int, example_id: int, points: List[float], label: int | str, human_annotated: bool=False, confidence: float=0.0) -> Segment:
        """Create a new segment label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            points (List[float]): The points of the segment.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Segment: The created segment label.
        """
        return self.segment.create(project_id, example_id, points, label, human_annotated, confidence)

    def update_category(self, project_id: int, example_id: int, label_id: int, label: Optional[int | str]=None, human_annotated: bool=None, confidence: float=None) -> Category:
        """Update a category label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            label_id (int): The id of the label.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to None.
            confidence (float): The confidence of the label. Defaults to None.

        Returns:
            Category: The updated category label.
        """
        return self.category.update(project_id, example_id, label_id, label, human_annotated, confidence)

    def update_span(self, project_id: int, example_id: int, label_id: int, start_offset: Optional[int]=None, end_offset: Optional[int]=None, label: Optional[int | str]=None, human_annotated: bool=None, confidence: float=None) -> Span:
        """Update a span label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            label_id (int): The id of the label.
            start_offset (int): The start offset of the span.
            end_offset (int): The end offset of the span.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to None.
            confidence (float): The confidence of the label. Defaults to None.

        Returns:
            Span: The updated span label.
        """
        return self.span.update(project_id, example_id, label_id, start_offset, end_offset, label, human_annotated, confidence)

    def update_relation(self, project_id: int, example_id: int, label_id: int, from_id: Optional[int]=None, to_id: Optional[int]=None, label: Optional[int | str]=None, human_annotated: bool=None, confidence: float=None) -> Relation:
        """Update a relation label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            label_id (int): The id of the label.
            from_id (int): The id of the from span.
            to_id (int): The id of the to span.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to None.
            confidence (float): The confidence of the label. Defaults to None.

        Returns:
            Relation: The updated relation label.
        """
        return self.relation.update(project_id, example_id, label_id, from_id, to_id, label, human_annotated, confidence)

    def update_text(self, project_id: int, example_id: int, label_id: int, text: Optional[str]=None, human_annotated: bool=None, confidence: float=None) -> Text:
        """Update a text label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            label_id (int): The id of the label.
            text (str): The text to update.
            human_annotated (bool): Whether the label is human annotated. Defaults to None.
            confidence (float): The confidence of the label. Defaults to None.

        Returns:
            Text: The updated text label.
        """
        return self.text.update(project_id, example_id, label_id, text, human_annotated, confidence)

    def update_bounding_box(self, project_id: int, example_id: int, label_id: int, x: Optional[float]=None, y: Optional[float]=None, width: Optional[float]=None, height: Optional[float]=None, label: Optional[int | str]=None, human_annotated: bool=None, confidence: float=None) -> BoundingBox:
        """Update a bounding box label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            label_id (int): The id of the label.
            x (float): The x coordinate of the bounding box.
            y (float): The y coordinate of the bounding box.
            width (float): The width of the bounding box.
            height (float): The height of the bounding box.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to None.
            confidence (float): The confidence of the label. Defaults to None.

        Returns:
            BoundingBox: The updated bounding box label.
        """
        return self.bounding_box.update(project_id, example_id, label_id, x, y, width, height, label, human_annotated, confidence)

    def update_segment(self, project_id: int, example_id: int, label_id: int, points: Optional[List[float]]=None, label: Optional[int | str]=None, human_annotated: bool=None, confidence: float=None) -> Segment:
        """Update a segment label.

        Args:
            project_id (int): The id of the project.
            example_id (int): The id of the example.
            label_id (int): The id of the label.
            points (List[float]): The points of the segment.
            label (int | str): The label to create.
            human_annotated (bool): Whether the label is human annotated. Defaults to None.
            confidence (float): The confidence of the label. Defaults to None.

        Returns:
            Segment: The updated segment label.
        """
        return self.segment.update(project_id, example_id, label_id, points, label, human_annotated, confidence)