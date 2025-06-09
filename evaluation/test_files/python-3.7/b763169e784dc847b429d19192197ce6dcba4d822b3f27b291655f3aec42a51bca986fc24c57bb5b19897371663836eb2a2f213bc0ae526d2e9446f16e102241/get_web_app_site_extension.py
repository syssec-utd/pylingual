import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetWebAppSiteExtensionResult', 'AwaitableGetWebAppSiteExtensionResult', 'get_web_app_site_extension', 'get_web_app_site_extension_output']

@pulumi.output_type
class GetWebAppSiteExtensionResult:
    """
    Site Extension Information.
    """

    def __init__(__self__, authors=None, comment=None, description=None, download_count=None, extension_id=None, extension_type=None, extension_url=None, feed_url=None, icon_url=None, id=None, installed_date_time=None, installer_command_line_params=None, kind=None, license_url=None, local_is_latest_version=None, local_path=None, name=None, project_url=None, provisioning_state=None, published_date_time=None, summary=None, title=None, type=None, version=None):
        if authors and (not isinstance(authors, list)):
            raise TypeError("Expected argument 'authors' to be a list")
        pulumi.set(__self__, 'authors', authors)
        if comment and (not isinstance(comment, str)):
            raise TypeError("Expected argument 'comment' to be a str")
        pulumi.set(__self__, 'comment', comment)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if download_count and (not isinstance(download_count, int)):
            raise TypeError("Expected argument 'download_count' to be a int")
        pulumi.set(__self__, 'download_count', download_count)
        if extension_id and (not isinstance(extension_id, str)):
            raise TypeError("Expected argument 'extension_id' to be a str")
        pulumi.set(__self__, 'extension_id', extension_id)
        if extension_type and (not isinstance(extension_type, str)):
            raise TypeError("Expected argument 'extension_type' to be a str")
        pulumi.set(__self__, 'extension_type', extension_type)
        if extension_url and (not isinstance(extension_url, str)):
            raise TypeError("Expected argument 'extension_url' to be a str")
        pulumi.set(__self__, 'extension_url', extension_url)
        if feed_url and (not isinstance(feed_url, str)):
            raise TypeError("Expected argument 'feed_url' to be a str")
        pulumi.set(__self__, 'feed_url', feed_url)
        if icon_url and (not isinstance(icon_url, str)):
            raise TypeError("Expected argument 'icon_url' to be a str")
        pulumi.set(__self__, 'icon_url', icon_url)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if installed_date_time and (not isinstance(installed_date_time, str)):
            raise TypeError("Expected argument 'installed_date_time' to be a str")
        pulumi.set(__self__, 'installed_date_time', installed_date_time)
        if installer_command_line_params and (not isinstance(installer_command_line_params, str)):
            raise TypeError("Expected argument 'installer_command_line_params' to be a str")
        pulumi.set(__self__, 'installer_command_line_params', installer_command_line_params)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if license_url and (not isinstance(license_url, str)):
            raise TypeError("Expected argument 'license_url' to be a str")
        pulumi.set(__self__, 'license_url', license_url)
        if local_is_latest_version and (not isinstance(local_is_latest_version, bool)):
            raise TypeError("Expected argument 'local_is_latest_version' to be a bool")
        pulumi.set(__self__, 'local_is_latest_version', local_is_latest_version)
        if local_path and (not isinstance(local_path, str)):
            raise TypeError("Expected argument 'local_path' to be a str")
        pulumi.set(__self__, 'local_path', local_path)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if project_url and (not isinstance(project_url, str)):
            raise TypeError("Expected argument 'project_url' to be a str")
        pulumi.set(__self__, 'project_url', project_url)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if published_date_time and (not isinstance(published_date_time, str)):
            raise TypeError("Expected argument 'published_date_time' to be a str")
        pulumi.set(__self__, 'published_date_time', published_date_time)
        if summary and (not isinstance(summary, str)):
            raise TypeError("Expected argument 'summary' to be a str")
        pulumi.set(__self__, 'summary', summary)
        if title and (not isinstance(title, str)):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, 'title', title)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if version and (not isinstance(version, str)):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def authors(self) -> Optional[Sequence[str]]:
        """
        List of authors.
        """
        return pulumi.get(self, 'authors')

    @property
    @pulumi.getter
    def comment(self) -> Optional[str]:
        """
        Site Extension comment.
        """
        return pulumi.get(self, 'comment')

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Detailed description.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='downloadCount')
    def download_count(self) -> Optional[int]:
        """
        Count of downloads.
        """
        return pulumi.get(self, 'download_count')

    @property
    @pulumi.getter(name='extensionId')
    def extension_id(self) -> Optional[str]:
        """
        Site extension ID.
        """
        return pulumi.get(self, 'extension_id')

    @property
    @pulumi.getter(name='extensionType')
    def extension_type(self) -> Optional[str]:
        """
        Site extension type.
        """
        return pulumi.get(self, 'extension_type')

    @property
    @pulumi.getter(name='extensionUrl')
    def extension_url(self) -> Optional[str]:
        """
        Extension URL.
        """
        return pulumi.get(self, 'extension_url')

    @property
    @pulumi.getter(name='feedUrl')
    def feed_url(self) -> Optional[str]:
        """
        Feed URL.
        """
        return pulumi.get(self, 'feed_url')

    @property
    @pulumi.getter(name='iconUrl')
    def icon_url(self) -> Optional[str]:
        """
        Icon URL.
        """
        return pulumi.get(self, 'icon_url')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='installedDateTime')
    def installed_date_time(self) -> Optional[str]:
        """
        Installed timestamp.
        """
        return pulumi.get(self, 'installed_date_time')

    @property
    @pulumi.getter(name='installerCommandLineParams')
    def installer_command_line_params(self) -> Optional[str]:
        """
        Installer command line parameters.
        """
        return pulumi.get(self, 'installer_command_line_params')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='licenseUrl')
    def license_url(self) -> Optional[str]:
        """
        License URL.
        """
        return pulumi.get(self, 'license_url')

    @property
    @pulumi.getter(name='localIsLatestVersion')
    def local_is_latest_version(self) -> Optional[bool]:
        """
        <code>true</code> if the local version is the latest version; <code>false</code> otherwise.
        """
        return pulumi.get(self, 'local_is_latest_version')

    @property
    @pulumi.getter(name='localPath')
    def local_path(self) -> Optional[str]:
        """
        Local path.
        """
        return pulumi.get(self, 'local_path')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='projectUrl')
    def project_url(self) -> Optional[str]:
        """
        Project URL.
        """
        return pulumi.get(self, 'project_url')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning state.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publishedDateTime')
    def published_date_time(self) -> Optional[str]:
        """
        Published timestamp.
        """
        return pulumi.get(self, 'published_date_time')

    @property
    @pulumi.getter
    def summary(self) -> Optional[str]:
        """
        Summary description.
        """
        return pulumi.get(self, 'summary')

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        return pulumi.get(self, 'title')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version information.
        """
        return pulumi.get(self, 'version')

class AwaitableGetWebAppSiteExtensionResult(GetWebAppSiteExtensionResult):

    def __await__(self):
        if False:
            yield self
        return GetWebAppSiteExtensionResult(authors=self.authors, comment=self.comment, description=self.description, download_count=self.download_count, extension_id=self.extension_id, extension_type=self.extension_type, extension_url=self.extension_url, feed_url=self.feed_url, icon_url=self.icon_url, id=self.id, installed_date_time=self.installed_date_time, installer_command_line_params=self.installer_command_line_params, kind=self.kind, license_url=self.license_url, local_is_latest_version=self.local_is_latest_version, local_path=self.local_path, name=self.name, project_url=self.project_url, provisioning_state=self.provisioning_state, published_date_time=self.published_date_time, summary=self.summary, title=self.title, type=self.type, version=self.version)

def get_web_app_site_extension(name: Optional[str]=None, resource_group_name: Optional[str]=None, site_extension_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetWebAppSiteExtensionResult:
    """
    Site Extension Information.


    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str site_extension_id: Site extension name.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['siteExtensionId'] = site_extension_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20210301:getWebAppSiteExtension', __args__, opts=opts, typ=GetWebAppSiteExtensionResult).value
    return AwaitableGetWebAppSiteExtensionResult(authors=__ret__.authors, comment=__ret__.comment, description=__ret__.description, download_count=__ret__.download_count, extension_id=__ret__.extension_id, extension_type=__ret__.extension_type, extension_url=__ret__.extension_url, feed_url=__ret__.feed_url, icon_url=__ret__.icon_url, id=__ret__.id, installed_date_time=__ret__.installed_date_time, installer_command_line_params=__ret__.installer_command_line_params, kind=__ret__.kind, license_url=__ret__.license_url, local_is_latest_version=__ret__.local_is_latest_version, local_path=__ret__.local_path, name=__ret__.name, project_url=__ret__.project_url, provisioning_state=__ret__.provisioning_state, published_date_time=__ret__.published_date_time, summary=__ret__.summary, title=__ret__.title, type=__ret__.type, version=__ret__.version)

@_utilities.lift_output_func(get_web_app_site_extension)
def get_web_app_site_extension_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, site_extension_id: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetWebAppSiteExtensionResult]:
    """
    Site Extension Information.


    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str site_extension_id: Site extension name.
    """
    ...