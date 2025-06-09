import io
import logging
from typing import Set, Dict, Generator, Tuple, List, Optional
import docker
import docker.models.containers
import docker.models.networks
from requests.exceptions import ConnectionError as RequestsConnectionError
from .DockerImage import DockerImage
from .DockerLink import DockerLink
from .DockerMachine import DockerMachine
from .DockerPlugin import DockerPlugin
from .stats.DockerLinkStats import DockerLinkStats
from .stats.DockerMachineStats import DockerMachineStats
from ... import utils
from ...decorators import privileged
from ...exceptions import DockerDaemonConnectionError, LinkNotFoundError, MachineCollisionDomainError, InvocationError, LabNotFoundError
from ...exceptions import MachineNotFoundError
from ...foundation.manager.IManager import IManager
from ...model.Lab import Lab
from ...model.Link import Link
from ...model.Machine import Machine
from ...setting.Setting import Setting
from ...utils import pack_files_for_tar, import_pywintypes
pywintypes = import_pywintypes()

def check_docker_status(method):
    """Decorator function to check if Docker daemon is running properly."""

    @privileged
    def check_docker(*args, **kw):
        method(*args, **kw)
        client = args[0].client
        try:
            client.ping()
        except RequestsConnectionError as e:
            raise DockerDaemonConnectionError(str(e))
        except pywintypes.error as e:
            raise DockerDaemonConnectionError(str(e))
    return check_docker

class DockerManager(IManager):
    """The class responsible to interact between Kathara and the Docker APIs."""
    __slots__ = ['client', 'docker_image', 'docker_machine', 'docker_link']

    @check_docker_status
    def __init__(self) -> None:
        remote_url = Setting.get_instance().remote_url
        if remote_url is None:
            self.client: docker.DockerClient = docker.from_env(timeout=None, max_pool_size=utils.get_pool_size())
        else:
            tls_config = docker.tls.TLSConfig(ca_cert=Setting.get_instance().cert_path)
            self.client: docker.DockerClient = docker.DockerClient(base_url=remote_url, timeout=None, max_pool_size=utils.get_pool_size(), tls=tls_config)
        docker_plugin = DockerPlugin(self.client)
        docker_plugin.check_and_download_plugin()
        self.docker_image: DockerImage = DockerImage(self.client)
        self.docker_machine: DockerMachine = DockerMachine(self.client, self.docker_image)
        self.docker_link: DockerLink = DockerLink(self.client)

    @privileged
    def deploy_machine(self, machine: Machine) -> None:
        """Deploy a Kathara device.

        Args:
            machine (Kathara.model.Machine): A Kathara machine object.

        Returns:
            None

        Raises:
            LabNotFoundError: If the specified device is not associated to any network scenario.
        """
        if not machine.lab:
            raise LabNotFoundError('Device `%s` is not associated to a network scenario.' % machine.name)
        self.docker_link.deploy_links(machine.lab, selected_links={x.name for x in machine.interfaces.values()})
        self.docker_machine.deploy_machines(machine.lab, selected_machines={machine.name})

    @privileged
    def deploy_link(self, link: Link) -> None:
        """Deploy a Kathara collision domain.

        Args:
            link (Kathara.model.Link): A Kathara collision domain object.

        Returns:
            None

        Raises:
            LabNotFoundError: If the collision domain is not associated to any network scenario.
        """
        if not link.lab:
            raise LabNotFoundError('Collision domain `%s` is not associated to a network scenario.' % link.name)
        self.docker_link.deploy_links(link.lab, selected_links={link.name})

    @privileged
    def deploy_lab(self, lab: Lab, selected_machines: Set[str]=None) -> None:
        """Deploy a Kathara network scenario.

        Args:
            lab (Kathara.model.Lab): A Kathara network scenario.
            selected_machines (Set[str]): If not None, deploy only the specified devices.

        Returns:
            None

        Raises:
            MachineNotFoundError: If the specified devices are not in the network scenario.
        """
        if selected_machines and (not lab.find_machines(selected_machines)):
            machines_not_in_lab = selected_machines - set(lab.machines.keys())
            raise MachineNotFoundError(f'The following devices are not in the network scenario: {machines_not_in_lab}.')
        selected_links = None
        if selected_machines:
            selected_links = lab.get_links_from_machines(selected_machines)
        self.docker_link.deploy_links(lab, selected_links=selected_links)
        self.docker_machine.deploy_machines(lab, selected_machines=selected_machines)

    @privileged
    def connect_machine_to_link(self, machine: Machine, link: Link) -> None:
        """Connect a Kathara device to a collision domain.

        Args:
            machine (Kathara.model.Machine): A Kathara machine object.
            link (Kathara.model.Link): A Kathara collision domain object.

        Returns:
            None

        Raises:
            LabNotFoundError: If the device specified is not associated to any network scenario.
            LabNotFoundError: If the collision domain is not associated to any network scenario.
            MachineCollisionDomainConflictError: If the device is already connected to the collision domain.
        """
        if not machine.lab:
            raise LabNotFoundError('Device `%s` is not associated to a network scenario.' % machine.name)
        if not link.lab:
            raise LabNotFoundError(f'Collision domain `{link.name}` is not associated to a network scenario.')
        if machine.name in link.machines:
            raise MachineCollisionDomainError(f'Device `{machine.name}` is already connected to collision domain `{link.name}`.')
        machine.add_interface(link)
        self.deploy_link(link)
        self.docker_machine.connect_to_link(machine, link)

    @privileged
    def disconnect_machine_from_link(self, machine: Machine, link: Link) -> None:
        """Disconnect a Kathara device from a collision domain.

        Args:
            machine (Kathara.model.Machine): A Kathara machine object.
            link (Kathara.model.Link): The Kathara collision domain from which disconnect the device.

        Returns:
            None

        Raises:
            LabNotFoundError: If the device specified is not associated to any network scenario.
            LabNotFoundError: If the collision domain is not associated to any network scenario.
            MachineCollisionDomainConflictError: If the device is not connected to the collision domain.
        """
        if not machine.lab:
            raise LabNotFoundError(f'Device `{machine.name}` is not associated to a network scenario.')
        if not link.lab:
            raise LabNotFoundError(f'Collision domain `{link.name}` is not associated to a network scenario.')
        if machine.name not in link.machines:
            raise MachineCollisionDomainError(f'Device `{machine.name}` is not connected to collision domain `{link.name}`.')
        machine.remove_interface(link)
        self.docker_machine.disconnect_from_link(machine, link)
        self.undeploy_link(link)

    @privileged
    def undeploy_machine(self, machine: Machine) -> None:
        """Undeploy a Kathara device.

        Args:
            machine (Kathara.model.Machine): A Kathara machine object.

        Returns:
            None

        Raises:
            LabNotFoundError: If the device specified is not associated to any network scenario.
        """
        if not machine.lab:
            raise LabNotFoundError(f'Device `{machine.name}` is not associated to a network scenario.')
        self.docker_machine.undeploy(machine.lab.hash, selected_machines={machine.name})
        self.docker_link.undeploy(machine.lab.hash, selected_links={x.name for x in machine.interfaces.values()})

    @privileged
    def undeploy_link(self, link: Link) -> None:
        """Undeploy a Kathara collision domain.

        Args:
            link (Kathara.model.Link): A Kathara collision domain object.

        Returns:
            None

        Raises:
            LabNotFoundError: If the collision domain is not associated to any network scenario.
        """
        if not link.lab:
            raise LabNotFoundError(f'Collision domain `{link.name}` is not associated to a network scenario.')
        self.docker_link.undeploy(link.lab.hash, selected_links={link.name})

    @privileged
    def undeploy_lab(self, lab_hash: Optional[str]=None, lab_name: Optional[str]=None, selected_machines: Optional[Set[str]]=None) -> None:
        """Undeploy a Kathara network scenario.

        Args:
            lab_hash (Optional[str]): The hash of the network scenario. Can be used as an alternative to lab_name.
                If None, lab_name should be set.
            lab_name (Optional[str]): The name of the network scenario. Can be used as an alternative to lab_hash.
                If None, lab_hash should be set.
            selected_machines (Optional[Set[str]]): If not None, undeploy only the specified devices.

        Returns:
            None

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        self.docker_machine.undeploy(lab_hash, selected_machines=selected_machines)
        self.docker_link.undeploy(lab_hash)

    @privileged
    def wipe(self, all_users: bool=False) -> None:
        """Undeploy all the running network scenarios.

        If multiuser scenarios are active, undeploy only current user devices.

        Args:
            all_users (bool): If false, undeploy only the current user network scenarios. If true, undeploy the
                running network scenarios of all users.

        Returns:
            None
        """
        if Setting.get_instance().remote_url is not None and all_users:
            all_users = False
            logging.warning('Cannot wipe devices of other users with a remote Docker connection.')
        user_name = utils.get_current_user_name() if not all_users else None
        self.docker_machine.wipe(user=user_name)
        self.docker_link.wipe(user=user_name)

    @privileged
    def connect_tty(self, machine_name: str, lab_hash: Optional[str]=None, lab_name: Optional[str]=None, shell: str=None, logs: bool=False) -> None:
        """Connect to a device in a running network scenario, using the specified shell.

        Args:
            machine_name (str): The name of the device to connect.
            lab_hash (str): The hash of the network scenario where the device is deployed.
            lab_name (str): The name of the network scenario where the device is deployed.
            shell (str): The name of the shell to use for connecting.
            logs (bool): If True, print startup logs on stdout.

        Returns:
            None

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        user_name = utils.get_current_user_name()
        self.docker_machine.connect(lab_hash=lab_hash, machine_name=machine_name, user=user_name, shell=shell, logs=logs)

    @privileged
    def exec(self, machine_name: str, command: List[str], lab_hash: Optional[str]=None, lab_name: Optional[str]=None) -> Generator[Tuple[bytes, bytes], None, None]:
        """Exec a command on a device in a running network scenario.

        Args:
            machine_name (str): The name of the device to connect.
            command (List[str]): The command to exec on the device.
            lab_hash (Optional[str]): The hash of the network scenario where the device is deployed.
            lab_name (Optional[str]): The name of the network scenario where the device is deployed.

        Returns:
            Generator[Tuple[bytes, bytes]]: A generator of tuples containing the stdout and stderr in bytes.

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        user_name = utils.get_current_user_name()
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        return self.docker_machine.exec(lab_hash, machine_name, command, user=user_name, tty=False)

    @privileged
    def copy_files(self, machine: Machine, guest_to_host: Dict[str, io.IOBase]) -> None:
        """Copy files on a running device in the specified paths.

        Args:
            machine (Kathara.model.Machine): A running device object. It must have the api_object field populated.
            guest_to_host (Dict[str, io.IOBase]): A dict containing the device path as key and
                fileobj to copy in path as value.

        Returns:
            None
        """
        tar_data = pack_files_for_tar(guest_to_host)
        self.docker_machine.copy_files(machine.api_object, path='/', tar_data=tar_data)

    @privileged
    def get_machine_api_object(self, machine_name: str, lab_hash: str=None, lab_name: str=None, all_users: bool=False) -> docker.models.containers.Container:
        """Return the corresponding API object of a running device in a network scenario.

        Args:
            machine_name (str): The name of the device.
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
                If None, lab_name should be set.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_name.
                If None, lab_hash should be set.
            all_users (bool): If True, return information about devices of all users.

        Returns:
            docker.models.containers.Container: Docker API object of devices.

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
            MachineNotFoundError: If the specified device is not found.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        user_name = utils.get_current_user_name() if not all_users else None
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        containers = self.docker_machine.get_machines_api_objects_by_filters(lab_hash=lab_hash, machine_name=machine_name, user=user_name)
        if containers:
            return containers.pop()
        raise MachineNotFoundError(f'Device `{machine_name}` not found.')

    def get_machines_api_objects(self, lab_hash: str=None, lab_name: str=None, all_users: bool=False) -> List[docker.models.containers.Container]:
        """Return API objects of running devices.

        Args:
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_name.
            all_users (bool): If True, return information about devices of all users.

        Returns:
            List[docker.models.containers.Container]: Docker API objects of devices.
        """
        user_name = utils.get_current_user_name() if not all_users else None
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        return self.docker_machine.get_machines_api_objects_by_filters(lab_hash=lab_hash, user=user_name)

    def get_link_api_object(self, link_name: str, lab_hash: str=None, lab_name: str=None, all_users: bool=False) -> docker.models.networks.Network:
        """Return the corresponding API object of a collision domain in a network scenario.

        Args:
            link_name (str): The name of the collision domain.
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
                If None, lab_name should be set.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_name.
                If None, lab_hash should be set.
            all_users (bool): If True, return information about collision domains of all users.

        Returns:
            docker.models.networks.Network: Docker API object of the network.

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
            LinkNotFoundError: If the collision domain is not found.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        user_name = utils.get_current_user_name() if not all_users else None
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        networks = self.docker_link.get_links_api_objects_by_filters(lab_hash=lab_hash, link_name=link_name, user=user_name)
        if networks:
            return networks.pop()
        raise LinkNotFoundError(f'Collision Domain `{link_name}` not found.')

    def get_links_api_objects(self, lab_hash: str=None, lab_name: str=None, all_users: bool=False) -> List[docker.models.networks.Network]:
        """Return API objects of collision domains in a network scenario.

        Args:
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_name.
            all_users (bool): If True, return information about collision domains of all users.

        Returns:
            List[docker.models.networks.Network]: Docker API objects of networks.
        """
        user_name = utils.get_current_user_name() if not all_users else None
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        return self.docker_link.get_links_api_objects_by_filters(lab_hash=lab_hash, user=user_name)

    @privileged
    def get_lab_from_api(self, lab_hash: str=None, lab_name: str=None) -> Lab:
        """Return the network scenario (specified by the hash or name), building it from API objects.

        Args:
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_name.

        Returns:
            Lab: The built network scenario.

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        if lab_name:
            reconstructed_lab = Lab(lab_name)
        else:
            reconstructed_lab = Lab('reconstructed_lab')
            reconstructed_lab.hash = lab_hash
        lab_containers = self.get_machines_api_objects(lab_hash=reconstructed_lab.hash)
        lab_networks = dict(map(lambda x: (x.name, x), self.get_links_api_objects(lab_hash=reconstructed_lab.hash)))
        for container in lab_containers:
            container.reload()
            device = reconstructed_lab.get_or_new_machine(container.labels['name'])
            device.api_object = container
            device.add_meta('privileged', container.attrs['HostConfig']['Privileged'])
            device.add_meta('image', container.attrs['Config']['Image'])
            device.add_meta('shell', container.attrs['Config']['Labels']['shell'])
            if container.attrs['HostConfig']['Memory'] > 0:
                device.add_meta('mem', f"{int(container.attrs['HostConfig']['Memory'] / 1024 ** 2)}M")
            if container.attrs['HostConfig']['NanoCpus'] > 0:
                device.add_meta('cpu', container.attrs['HostConfig']['NanoCpus'] / 1000000000)
            for env in container.attrs['Config']['Env']:
                device.add_meta('env', env)
            if container.attrs['HostConfig']['PortBindings']:
                for (port_info, port_data) in container.attrs['HostConfig']['PortBindings'].items():
                    (guest_port, protocol) = port_info.split('/')
                    host_port = port_data[0]['HostPort']
                    device.meta['ports'][int(host_port), protocol] = int(guest_port)
            device.meta['sysctls'] = container.attrs['HostConfig']['Sysctls']
            if 'none' not in container.attrs['NetworkSettings']['Networks']:
                for network_name in container.attrs['NetworkSettings']['Networks']:
                    if network_name == 'bridge':
                        device.add_meta('bridged', True)
                        continue
                    network = lab_networks[network_name]
                    link = reconstructed_lab.get_or_new_link(network.attrs['Labels']['name'])
                    link.api_object = network
                    device.add_interface(link)
        return reconstructed_lab

    @privileged
    def update_lab_from_api(self, lab: Lab) -> None:
        """Update the passed network scenario from API objects.

        Args:
            lab (Lab): The network scenario to update.
        """
        running_containers = self.get_machines_api_objects(lab_hash=lab.hash)
        deployed_networks = dict(map(lambda x: (x.name, x), self.get_links_api_objects(lab_hash=lab.hash)))
        for network in deployed_networks.values():
            network.reload()
        deployed_networks_by_link_name = dict(map(lambda x: (x.attrs['Labels']['name'], x), self.get_links_api_objects(lab_hash=lab.hash)))
        for container in running_containers:
            container.reload()
            device = lab.get_or_new_machine(container.labels['name'])
            device.api_object = container
            static_links = set(device.interfaces.values())
            current_links = set(map(lambda x: lab.get_or_new_link(deployed_networks[x].attrs['Labels']['name']), filter(lambda x: x != 'bridge', container.attrs['NetworkSettings']['Networks'])))
            dynamic_links = current_links - static_links
            deleted_links = static_links - current_links
            for link in static_links:
                if link.name in deployed_networks_by_link_name:
                    link.api_object = deployed_networks_by_link_name[link.name]
            for link in dynamic_links:
                link.api_object = deployed_networks_by_link_name[link.name]
                device.add_interface(link)
            for link in deleted_links:
                device.remove_interface(link)

    @privileged
    def get_machines_stats(self, lab_hash: str=None, lab_name: str=None, machine_name: str=None, all_users: bool=False) -> Generator[Dict[str, DockerMachineStats], None, None]:
        """Return information about the running devices.

        Args:
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_hash.
            machine_name (str): If specified return all the devices with machine_name.
            all_users (bool): If True, return information about the device of all users.

        Returns:
              Generator[Dict[str, DockerMachineStats], None, None]: A generator containing dicts that has API Object
              identifier as keys and DockerMachineStats objects as values.
        """
        user_name = utils.get_current_user_name() if not all_users else None
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        return self.docker_machine.get_machines_stats(lab_hash=lab_hash, machine_name=machine_name, user=user_name)

    @privileged
    def get_machine_stats(self, machine_name: str, lab_hash: str=None, lab_name: str=None, all_users: bool=False) -> Generator[DockerMachineStats, None, None]:
        """Return information of the specified device in a specified network scenario.

        Args:
            machine_name (str): The device name.
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
                If None, lab_name should be set.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_hash.
                If None, lab_hash should be set.
            all_users (bool): If True, search the device among all the users devices.

        Returns:
            Generator[DockerMachineStats, None, None]: A generator containing DockerMachineStats objects with
            the device info.

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        machines_stats = self.get_machines_stats(lab_hash=lab_hash, machine_name=machine_name, all_users=all_users)
        (_, machine_stats) = next(machines_stats).popitem()
        yield machine_stats

    def get_links_stats(self, lab_hash: str=None, lab_name: str=None, link_name: str=None, all_users: bool=False) -> Generator[Dict[str, DockerLinkStats], None, None]:
        """Return information about deployed Docker networks.

        Args:
           lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
           lab_name (str): The name of the network scenario. Can be used as an alternative to lab_hash.
           link_name (str): If specified return all the networks with link_name.
           all_users (bool): If True, return information about the networks of all users.

        Returns:
             Generator[Dict[str, DockerLinkStats], None, None]: A generator containing dicts that has API Object
                identifier as keys and DockerLinksStats objects as values.
        """
        user_name = utils.get_current_user_name() if not all_users else None
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        return self.docker_link.get_links_stats(lab_hash=lab_hash, link_name=link_name, user=user_name)

    def get_link_stats(self, link_name: str, lab_hash: str=None, lab_name: str=None, all_users: bool=False) -> Generator[DockerLinkStats, None, None]:
        """Return information of the specified deployed network in a specified network scenario.

        Args:
            link_name (str): The link name.
            lab_hash (str): The hash of the network scenario. Can be used as an alternative to lab_name.
                If None, lab_name should be set.
            lab_name (str): The name of the network scenario. Can be used as an alternative to lab_hash.
                If None, lab_hash should be set.
            all_users (bool): If True, search the network among all the users networks.

        Returns:
            Generator[DockerLinkStats, None, None]: A generator containing DockerLinkStats objects with the network
                statistics.

        Raises:
            InvocationError: If a running network scenario hash or name is not specified.
        """
        if not lab_hash and (not lab_name):
            raise InvocationError('You must specify a running network scenario hash or name.')
        if lab_name:
            lab_hash = utils.generate_urlsafe_hash(lab_name)
        links_stats = self.get_links_stats(lab_hash=lab_hash, link_name=link_name, all_users=all_users)
        (_, link_stats) = next(links_stats).popitem()
        yield link_stats

    @privileged
    def check_image(self, image_name: str) -> None:
        """Check if the specified image is valid.

        Args:
            image_name (str): The name of the image

        Returns:
            None

        Raises:
            ConnectionError: If the image is not locally available and there is no connection to a remote image repository.
            DockerImageNotFoundError: If the image is not found.
        """
        self.docker_image.check(image_name)

    @privileged
    def get_release_version(self) -> str:
        """Return the current manager version.

        Returns:
            str: The current manager version.
        """
        return self.client.version()['Version']

    @staticmethod
    def get_formatted_manager_name() -> str:
        """Return a formatted string containing the current manager name.

        Returns:
            str: A formatted string containing the current manager name.
        """
        return 'Docker (Kathara)'