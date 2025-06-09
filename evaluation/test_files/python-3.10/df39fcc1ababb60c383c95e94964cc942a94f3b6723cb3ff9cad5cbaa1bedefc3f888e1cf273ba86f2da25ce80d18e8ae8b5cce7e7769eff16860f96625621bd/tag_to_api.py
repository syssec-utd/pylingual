import typing_extensions
from frontrunner_python_sdk.apis.tags import TagValues
from frontrunner_python_sdk.apis.tags.abbreviated_people_api import AbbreviatedPeopleApi
from frontrunner_python_sdk.apis.tags.api_api import ApiApi
from frontrunner_python_sdk.apis.tags.feed_api import FeedApi
from frontrunner_python_sdk.apis.tags.integrations_api import IntegrationsApi
from frontrunner_python_sdk.apis.tags.people_api import PeopleApi
from frontrunner_python_sdk.apis.tags.tags_api import TagsApi
from frontrunner_python_sdk.apis.tags.tasks_api import TasksApi
TagToApi = typing_extensions.TypedDict('TagToApi', {TagValues.ABBREVIATED_PEOPLE: AbbreviatedPeopleApi, TagValues.API: ApiApi, TagValues.FEED: FeedApi, TagValues.INTEGRATIONS: IntegrationsApi, TagValues.PEOPLE: PeopleApi, TagValues.TAGS: TagsApi, TagValues.TASKS: TasksApi})
tag_to_api = TagToApi({TagValues.ABBREVIATED_PEOPLE: AbbreviatedPeopleApi, TagValues.API: ApiApi, TagValues.FEED: FeedApi, TagValues.INTEGRATIONS: IntegrationsApi, TagValues.PEOPLE: PeopleApi, TagValues.TAGS: TagsApi, TagValues.TASKS: TasksApi})