from sonarqube.utils.rest_client import RestClient
from sonarqube.utils.config import API_PROJECTS_BULK_DELETE_ENDPOINT, API_PROJECTS_SEARCH_ENDPOINT, API_PROJECTS_CREATE_ENDPOINT, API_PROJECTS_DELETE_ENDPOINT, API_PROJECTS_UPDATE_VISIBILITY_ENDPOINT, API_PROJECTS_UPDATE_KEY_ENDPOINT, API_PROJECTS_UPDATE_DEFAULT_VISIBILITY_ENDPOINT, API_PROJECTS_EXPORT_FINDINGS_ENDPOINT, API_PROJECTS_LICENSE_USAGE_ENDPOINT
from sonarqube.utils.common import GET, POST

class SonarQubeProjects(RestClient):
    """
    SonarQube projects Operations
    """
    special_attributes_map = {'previous_project_key': 'from', 'new_project_key': 'to'}

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        super(SonarQubeProjects, self).__init__(**kwargs)

    def get(self, key):
        result = self.search_projects(projects=key)
        projects = result.get('components', [])
        for project in projects:
            if project['key'] == key:
                return project

    @GET(API_PROJECTS_SEARCH_ENDPOINT)
    def search_projects(self, organization=None, analyzedBefore=None, onProvisionedOnly='false', projects=None, p=None, ps=None, q=None, qualifiers='TRK'):
        """
        SINCE 6.3
        Search for projects or views to administrate them.

        :param organization: The key of the organization
        :param analyzedBefore: Filter the projects for which last analysis is older than the given date (exclusive).
          Either a date (server timezone) or datetime can be provided.
        :param onProvisionedOnly: Filter the projects that are provisioned.
          Possible values are for: true or false. default value is false.
        :param projects: Comma-separated list of project keys
        :param p: page number.
        :param ps: Page size. Must be greater than 0 and less or equal than 500
        :param q:
          Limit search to:
            * component names that contain the supplied string
            * component keys that contain the supplied string
        :param qualifiers: Comma-separated list of component qualifiers. Filter the results with the specified
          qualifiers. Possible values are for:
            * TRK
            * VW
            * APP
          default value is TRK.

        :return:
        """

    @POST(API_PROJECTS_CREATE_ENDPOINT)
    def create_project(self, project, name, organization=None, visibility=None):
        """
        SINCE 4.0
        Create a project.

        :param project: Key of the project
        :param name: Name of the project. If name is longer than 500, it is abbreviated.
        :param organization: The key of the organization
        :param visibility: Whether the created project should be visible to everyone, or only specific user/groups.
          If no visibility is specified, the default project visibility of the organization will be used.
          Possible values are for:
            * private
            * public
        :return: request response
        """

    @POST(API_PROJECTS_DELETE_ENDPOINT)
    def delete_project(self, project):
        """
        SINCE 5.2
        Delete a project.

        :param project: Project key
        :return:
        """

    @POST(API_PROJECTS_BULK_DELETE_ENDPOINT)
    def bulk_delete_projects(self, organization=None, analyzedBefore=None, onProvisionedOnly='false', projects=None, q=None, qualifiers='TRK'):
        """
        SINCE 5.2
        Delete one or several projects.
        At least one parameter is required among analyzedBefore, projects, projectIds (deprecated since 6.4) and q

        :param organization: The key of the organization
        :param analyzedBefore: Filter the projects for which last analysis is older than the given date (exclusive).
          Either a date (server timezone) or datetime can be provided.
        :param onProvisionedOnly: Filter the projects that are provisioned.
          Possible values are for: true or false. default value is false.
        :param projects: Comma-separated list of project keys
        :param q:
          Limit to:
            * component names that contain the supplied string
            * component keys that contain the supplied string
        :param qualifiers: Comma-separated list of component qualifiers. Filter the results with the specified
          qualifiers. Possible values are for:
            * TRK
            * VW
            * APP
          default value is TRK.
        :return:
        """

    @POST(API_PROJECTS_UPDATE_KEY_ENDPOINT)
    def update_project_key(self, previous_project_key, new_project_key):
        """
        SINCE 6.1
        Update a project or module key and all its sub-components keys.

        :param previous_project_key: Project or module key
        :param new_project_key: New component key
        :return:
        """

    @POST(API_PROJECTS_UPDATE_VISIBILITY_ENDPOINT)
    def update_project_visibility(self, project, visibility):
        """
        SINCE 6.4
        Updates visibility of a project.

        :param project: Project key
        :param visibility: New visibility
        :return:
        """

    @POST(API_PROJECTS_UPDATE_DEFAULT_VISIBILITY_ENDPOINT)
    def update_project_default_visibility(self, projectVisibility):
        """
        SINCE 6.4
        Update the default visibility for new projects.

        :param projectVisibility: Default visibility for projects
        :return:
        """

    @GET(API_PROJECTS_EXPORT_FINDINGS_ENDPOINT)
    def export_findings_for_project(self, project, branch=None, pullRequest=None):
        """
        SINCE 9.1
        Export all findings (issues and hotspots) of a specific project branch.

        :param project: Project key
        :param branch: Branch key. When not specified, if no Pull Request key is defined either,
        it will default to the main branch
        :param pullRequest: Pull Request key. When not specified, the branch data will be returned instead
        :return:
        """

    @GET(API_PROJECTS_LICENSE_USAGE_ENDPOINT)
    def get_license_usage_for_project(self):
        """
        SINCE 9.4
        Help admins to understand how the number of lines of code (used for licensing) is distributed between projects,
        i.e. how much each project affects the total number of lines of code. Returns the list of projects together with
        information about their usage, sorted by lines of code descending.
        Requires Administer System permission.

        :return:
        """