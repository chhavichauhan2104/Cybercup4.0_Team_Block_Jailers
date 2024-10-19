from kubernetes import client, config
from kubernetes.client import V1Deployment, V1DeploymentSpec, V1PodTemplateSpec, V1PodSpec
from kubernetes.client import V1Container, V1ContainerPort, V1Service, V1ServiceSpec, V1ServicePort
from kubernetes.client import V1ObjectMeta, V1LabelSelector

# Load the Kubernetes configuration
config.load_kube_config()

# Create the API client instances
apps_v1_api = client.AppsV1Api()
core_v1_api = client.CoreV1Api()

# Define metadata for Deployment
metadata = V1ObjectMeta(name="hwid-ban-service", labels={"app": "hwid-ban-service"})

# Define the container with the application
container = V1Container(
    name="hwid-ban-service",
    image="hwid-ban-service:latest",  # Image already built in Docker
    ports=[V1ContainerPort(container_port=5000)]
)

# Define the pod template specification
pod_template = V1PodTemplateSpec(
    metadata=V1ObjectMeta(labels={"app": "hwid-ban-service"}),
    spec=V1PodSpec(containers=[container])
)

# Define the deployment spec
deployment_spec = V1DeploymentSpec(
    replicas=1,
    selector=V1LabelSelector(match_labels={"app": "hwid-ban-service"}),
    template=pod_template
)

# Create the deployment object
deployment = V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=metadata,
    spec=deployment_spec
)

# Create the deployment in Kubernetes
apps_v1_api.create_namespaced_deployment(namespace="default", body=deployment)

print("Deployment created.")

# Now, let's define the Service
service_metadata = V1ObjectMeta(name="hwid-ban-service")

service_spec = V1ServiceSpec(
    selector={"app": "hwid-ban-service"},
    ports=[V1ServicePort(protocol="TCP", port=5000, target_port=5000)],
    type="NodePort"
)

service = V1Service(
    api_version="v1",
    kind="Service",
    metadata=service_metadata,
    spec=service_spec
)

# Create the service in Kubernetes
core_v1_api.create_namespaced_service(namespace="default", body=service)

print("Service created.")