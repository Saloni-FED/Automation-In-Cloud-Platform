from flask import Flask, request, jsonify
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.eventgrid import EventGridManagementClient
from azure.mgmt.eventgrid.models import EventSubscription, WebHookEventSubscriptionDestination
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Initialize Azure clients
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
eventgrid_client = EventGridManagementClient(credential, SUBSCRIPTION_ID)

# Helper function to create Event Subscription
def create_event_subscription(scope, subscription_name, event_types, webhook_url):
    try:
        response = eventgrid_client.event_subscriptions.begin_create_or_update(
            scope=scope,
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
        resource_group_name = data.get("resourceGroupName")  # Required for resource groups
        resource_name = data.get("resourceName")  # Optional for specific resources
        event_types = data.get("eventTypes")
        subscription_name = data.get("subscriptionName")
        webhook_url = "https://insect-uncommon-luckily.ngrok-free.app/webhook-eventarc"

        if not all([resource_type, resource_group_name, event_types, subscription_name]):
            return jsonify({"error": "Missing required fields"}), 400

        # Determine the scope
        if resource_type == "Resource Group":
            # Resource Group-level scope
            scope = f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{resource_group_name}"
        else:
            # Specific resource-level scope
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
            resource = resource_client.resources.get(
                resource_group_name=resource_group_name,
                resource_provider_namespace=provider_namespace,
                parent_resource_path="",
                resource_type=azure_resource_type,
                resource_name=resource_name,
                api_version="2021-08-01"
            )
            scope = resource.id

        # Create the event subscription
        subscription_id = create_event_subscription(scope, subscription_name, event_types, webhook_url)

        return jsonify({"message": "Event Subscription created successfully", "subscriptionId": subscription_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    print("[INFO] Starting Flask API server...")
    app.run(host="0.0.0.0", port=4800)
