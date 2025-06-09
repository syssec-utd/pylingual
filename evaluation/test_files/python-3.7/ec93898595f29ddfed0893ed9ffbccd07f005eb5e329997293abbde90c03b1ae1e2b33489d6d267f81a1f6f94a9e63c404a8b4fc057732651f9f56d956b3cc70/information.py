import sys
import os
import platform
import socket
import six
from rook.com_ws.linux_distribution import LinuxDistribution
from rook.config import VersionConfiguration, GitConfig
from rook import git
import rook.protobuf.agent_info_pb2 as agent_info_pb
from rook.logger import logger

class Information(object):
    _k8sNamespaceFileName_default = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
    _k8sNamespaceFileName = _k8sNamespaceFileName_default

    def __init__(self):
        self.debug = False

    def collect(self, debug=False, k8namespaceFile=None):
        if k8namespaceFile:
            self._k8sNamespaceFileName = k8namespaceFile
        for (name, collector) in six.iteritems(self._collectors):
            try:
                if callable(collector):
                    value = collector()
                else:
                    value = collector
                setattr(self, name, value)
            except Exception as exc:
                logger.debug('Failed to collect %s information: %s', name, exc)
                setattr(self, name, '')
        self.debug = debug
        return self

class SCMInformation(Information):

    def __init__(self):
        super(SCMInformation, self).__init__()
        self._collectors = {'commit': self._get_commit, 'origin': self._get_origin, 'sources': self._get_sources}

    def _get_commit(self):
        user_commit = GitConfig.GIT_COMMIT or os.environ.get('ROOKOUT_COMMIT', '')
        if user_commit:
            return user_commit
        else:
            git_root = self._get_git_root()
            if git_root:
                return git.get_revision(git_root)
        return ''

    def _get_origin(self):
        user_remote_origin = GitConfig.GIT_ORIGIN or os.environ.get('ROOKOUT_REMOTE_ORIGIN', '')
        if user_remote_origin:
            return user_remote_origin
        else:
            git_root = self._get_git_root()
            if git_root:
                return git.get_remote_url(git_root)
        return ''

    def _get_git_root(self):
        return os.environ.get('ROOKOUT_GIT') or git.find_root(os.path.dirname(os.path.abspath(sys.argv[0])))

    def _get_sources(self):
        return GitConfig.SOURCES

class NetworkInformation(Information):

    def __init__(self):
        super(NetworkInformation, self).__init__()
        self._collectors = {'ip_addr': self._get_ip_addr, 'network': platform.node()}

    @staticmethod
    def _get_ip_addr():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]

class SystemInformation(Information):

    def __init__(self):
        super(SystemInformation, self).__init__()
        self._collectors = {'hostname': socket.gethostname, 'os': platform.system, 'os_version': self._get_os_version, 'distro': lambda : platform.system() == 'Linux' and LinuxDistribution.get_name() or '', 'arch': platform.machine()}

    def _get_os_version(self):
        system = platform.system()
        if system == 'Darwin':
            version = platform.mac_ver()[0]
        elif system == 'Linux':
            version = LinuxDistribution.get_version()
        elif system == 'Windows':
            version = platform.win32_ver()[0]
        else:
            version = ''
        return version

class VersionInformation(Information):

    def __init__(self):
        super(VersionInformation, self).__init__()
        self._collectors = {'version': VersionConfiguration.VERSION, 'commit': VersionConfiguration.COMMIT}

class PlatformInformation(Information):

    def __init__(self):
        super(PlatformInformation, self).__init__()
        self._collectors = {'platform': 'python', 'version': sys.version, 'variant': platform.python_implementation}

class ClusterInformation(Information):

    def __init__(self):
        super(ClusterInformation, self).__init__()
        self._collectors = {'k8s_namespace': self._get_namespace_name}

    def _get_namespace_name(self):
        """
        Collect Kubernates cluster information
        """
        filename = self._k8sNamespaceFileName
        try:
            if not os.path.isfile(filename):
                return ''
        except:
            return ''
        try:
            with open(filename, 'r') as f:
                contents = f.read()
        except:
            logger.debug('Failed to read Kubernates information from: %s', filename)
            return ''
        return contents

class ServerlessInformation(Information):

    def __init__(self):
        super(ServerlessInformation, self).__init__()
        self._collectors = {'function_name': self._get_function_name, 'rookout_serverless': self._is_serverless, 'aws_region': self._get_aws_region, 'azure_region': self._get_azure_region}

    def __iter__(self):
        for (attr, value) in self.__dict__.items():
            if not attr.startswith('_') and (not callable(getattr(self, attr))):
                yield (attr, value)

    def _is_AWSlambda(self):
        return os.environ.get('AWS_LAMBDA_FUNCTION_NAME')

    def _is_google_cloudfunction(self):
        return os.environ.get('FUNCTION_TARGET') and os.environ.get('FUNCTION_SIGNATURE_TYPE')

    def _is_azurefunction(self):
        return os.environ.get('FUNCTIONS_WORKER_RUNTIME') and os.environ.get('WEBSITE_SITE_NAME')

    def _is_cloudrun_or_firbase(self):
        return os.environ.get('K_SERVICE') and os.environ.get('K_REVISION') and os.environ.get('K_CONFIGURATION') and os.environ.get('PORT')

    def _get_function_name(self):
        if self._is_AWSlambda():
            return os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
        elif self._is_google_cloudfunction() or self._is_cloudrun_or_firbase():
            return os.environ.get('FUNCTION_NAME') or os.environ.get('K_SERVICE')
        elif self._is_azurefunction():
            return os.environ.get('WEBSITE_SITE_NAME')
        return ''

    def _is_serverless(self):
        return 'true' if self._is_AWSlambda() or self._is_google_cloudfunction() or self._is_cloudrun_or_firbase() or self._is_azurefunction() else ''

    def _get_aws_region(self):
        if self._is_AWSlambda():
            return os.environ.get('AWS_REGION')
        return ''

    def _get_azure_region(self):
        if self._is_azurefunction():
            return os.environ.get('REGION_NAME')
        return ''

class AgentInformation(Information):

    def __init__(self):
        super(AgentInformation, self).__init__()
        self._collectors = {'version': lambda : VersionInformation().collect(), 'network': lambda : NetworkInformation().collect(), 'system': lambda : SystemInformation().collect(), 'platform': lambda : PlatformInformation().collect(), 'scm': lambda : SCMInformation().collect(), 'cluster': lambda : ClusterInformation().collect(k8namespaceFile=self._k8sNamespaceFileName), 'serverless_info': lambda : ServerlessInformation().collect(), 'executable': lambda : sys.argv[0], 'command_arguments': lambda : sys.argv[1:], 'process_id': os.getpid}

def collect(debug, k8namespaceFile=None):
    return AgentInformation().collect(debug, k8namespaceFile)

def pack_agent_info(info):
    packed_info = agent_info_pb.AgentInformation()
    packed_info.agent_id = info.agent_id
    packed_info.version.CopyFrom(agent_info_pb.VersionInformation())
    packed_info.version.version = info.version.version
    packed_info.version.commit = info.version.commit
    packed_info.network.CopyFrom(agent_info_pb.NetworkInformation())
    packed_info.network.ip_addr = info.network.ip_addr
    packed_info.network.network = info.network.network
    packed_info.system.CopyFrom(agent_info_pb.SystemInformation())
    packed_info.system.hostname = info.system.hostname
    packed_info.system.os = info.system.os
    packed_info.system.os_version = info.system.os_version
    packed_info.system.distro = info.system.distro
    packed_info.system.arch = info.system.arch
    packed_info.platform.CopyFrom(agent_info_pb.PlatformInformation())
    packed_info.platform.platform = info.platform.platform
    packed_info.platform.version = info.platform.version
    packed_info.platform.variant = info.platform.variant
    packed_info.scm.CopyFrom(agent_info_pb.SCMInformation())
    packed_info.scm.commit = info.scm.commit
    packed_info.scm.origin = info.scm.origin
    if info.scm.sources:
        for (origin, commit) in six.iteritems(info.scm.sources):
            source_info = agent_info_pb.SCMInformation.SourceInfo()
            source_info.remoteOriginUrl = origin
            source_info.commit = commit
            packed_info.scm.sources.append(source_info)
    have_user_defined_git_info = info.scm.commit and info.scm.origin
    if have_user_defined_git_info and info.scm.origin not in info.scm.sources:
        source_info = agent_info_pb.SCMInformation.SourceInfo()
        source_info.remoteOriginUrl = info.scm.origin
        source_info.commit = info.scm.commit
        packed_info.scm.sources.append(source_info)
    packed_info.executable = info.executable
    packed_info.command_arguments.extend(info.command_arguments)
    packed_info.process_id = info.process_id
    for (label_key, label_value) in six.iteritems(info.labels):
        packed_info.labels[label_key] = label_value
    if info.debug:
        packed_info.labels['rookout_debug'] = 'on'
    if info.cluster and info.cluster.k8s_namespace != '' and ('k8s_namespace' not in packed_info.labels):
        packed_info.labels['k8s_namespace'] = info.cluster.k8s_namespace
    for (label_key, label_value) in info.serverless_info:
        if label_key not in packed_info.labels and label_value:
            packed_info.labels[label_key] = label_value
    packed_info.tags.extend(info.tags)
    return packed_info