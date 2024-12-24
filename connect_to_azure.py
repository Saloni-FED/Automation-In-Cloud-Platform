from flask import Flask, request, jsonify
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.eventgrid import EventGridManagementClient
from azure.mgmt.eventgrid.models import EventSubscription, WebHookEventSubscriptionDestination
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Azure AD application details
# TENANT_ID = "ce0dc187-5e20-4403-8c23-f4a815dc7b0d"
# CLIENT_ID = "0eb9bfc6-30f7-4ef4-aea8-03e3b6afb6ed"
# CLIENT_SECRET = "se18Q~LyCEFUh-aNqEIxH1IEuaIc9lYD_SCjpc.T"
# SUBSCRIPTION_ID = "dac89436-7e11-4b69-9873-b2d2daf6c299"

# # Authenticate using ClientSecretCredential
# credential = ClientSecretCredential(
#     tenant_id=TENANT_ID,
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET
# )

# Initialize Azure clients
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
eventgrid_client = EventGridManagementClient(credential, SUBSCRIPTION_ID)

# Helper function to get resource ID
def get_resource_id(resource_group, provider_namespace, resource_type, resource_name="gridblob"):
    try:
        print(f"[DEBUG] Fetching resource ID for: resource_group={resource_group}, provider_namespace={provider_namespace}, resource_type={resource_type}, resource_name={resource_name}")
        
        # Adjust API call if resource_name is not required
        if resource_name:
            resource = resource_client.resources.get(
                resource_group_name=resource_group,
                resource_provider_namespace=provider_namespace,
                parent_resource_path="",
                resource_type=resource_type,
                resource_name=resource_name,
                api_version="2021-08-01"
            )
        else:
            resource = resource_client.resources.get_by_id(
                resource_group_name=resource_group,
                provider_namespace=provider_namespace,
                resource_type=resource_type,
                api_version="2021-08-01"
            )

        print(f"[DEBUG] Resource ID: {resource.id}")
        return resource.id
    except Exception as e:
        print(f"[ERROR] Failed to fetch resource ID: {e}")
        raise Exception(f"Failed to fetch resource ID: {e}")


# Helper function to create Event Subscription
def create_event_subscription(resource_id, subscription_name, event_types, webhook_url):
    try:
        response = eventgrid_client.event_subscriptions.begin_create_or_update(
            scope=resource_id,
            event_subscription_name=subscription_name,
            event_subscription_info=EventSubscription(
                destination=WebHookEventSubscriptionDestination(endpoint_url=webhook_url),
                filter={
                    "is_subject_case_sensitive": False,
                    "included_event_types": event_types,
                },
                event_delivery_schema="EventGridSchema",
            ),
        ).result()
        return response.id
    except Exception as e:
        raise Exception(f"Failed to create Event Subscription: {e}")
@app.route("/create_event_subscription", methods=["POST"])
def create_subscription():
    try:
        data = request.get_json()
        resource_type = data.get("resourceType")
       
        resource_group_name = data.get("resourceGroupName")  # Default to "AI"
        resource_name = data.get("blobName")      # Default to "gridblob"
        print(resource_group_name, resource_name)

        event_types = data.get("eventTypes")
        subscription_name = data.get("subscriptionName")
        webhook_url = "https://insect-uncommon-luckily.ngrok-free.app/eventgrid"

        if not all([resource_type, resource_group_name, event_types, subscription_name]):
            return jsonify({"error": "Missing required fields"}), 400

        # Map resource type to provider namespace and resource type
        resource_mapping = {
            "Blob Storage": ("Microsoft.Storage", "storageAccounts"),
            "Virtual Machine": ("Microsoft.Compute", "virtualMachines"),
            "Azure Kubernetes": ("Microsoft.ContainerService", "managedClusters"),
            "Azure App Service": ("Microsoft.Web", "sites"),
            "Azure SQL": ("Microsoft.Sql", "servers"),
            "Azure Key Vault": ("Microsoft.KeyVault", "vaults"),
        }

        if resource_type not in resource_mapping:
            return jsonify({"error": "Unsupported resource type"}), 400

        provider_namespace, azure_resource_type = resource_mapping[resource_type]

        # Get the resource ID
        resource_id = get_resource_id(resource_group_name, provider_namespace, azure_resource_type, resource_name)

        # Create the event subscription
        subscription_id = create_event_subscription(resource_id, subscription_name, event_types, webhook_url)

        return jsonify({"message": "Event Subscription created successfully", "subscriptionId": subscription_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("[INFO] Starting Flask API server...")
    app.run(host="0.0.0.0", port=4800)
