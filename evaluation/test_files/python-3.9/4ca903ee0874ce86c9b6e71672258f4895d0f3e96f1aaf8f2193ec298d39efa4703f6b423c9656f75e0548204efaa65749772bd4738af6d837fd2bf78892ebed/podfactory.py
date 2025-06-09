import logging
from kubernetes import client
from kubernetes.client import V1ResourceRequirements, V1EnvVarSource, V1EnvVar, V1ObjectFieldSelector
from galileofaas.context.platform.pod.factory import PodFactory
from galileofaas.system.core import KubernetesFunctionReplica
logger = logging.getLogger(__name__)

class BasicExamplePodFactory(PodFactory):

    def create_mobilenet_container(self, replica: KubernetesFunctionReplica) -> client.V1Container:
        return client.V1Container(image=replica.image, name=replica.replica_id, ports=[client.V1ContainerPort(name='function-port', container_port=8080)], resources=V1ResourceRequirements(requests=replica.container.get_resource_requirements()), env=[V1EnvVar('NODE_NAME', value_from=V1EnvVarSource(field_ref=V1ObjectFieldSelector(field_path='spec.nodeName'))), V1EnvVar('MODEL_STORAGE', 'local'), V1EnvVar('MODEL_FILE', '/home/app/function/data/mobilenet.tflite'), V1EnvVar('LABELS_FILE', '/home/app/function/data/labels.txt'), V1EnvVar('IMAGE_STORAGE', 'request')])

    def create_container(self, replica: KubernetesFunctionReplica) -> client.V1Container:
        if 'mobilenet' in replica.image:
            return self.create_mobilenet_container(replica)
        else:
            raise ValueError(f'Can not create Container for replica. Unknown image "{replica.image}"')