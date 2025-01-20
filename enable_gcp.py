from google.cloud import compute_v1
from google.oauth2 import service_account
import json

# Project configuration
PROJECT_ID = "able-stock-428615-n4"  # Replace with your project ID
REGION = "us-central1"
NETWORK_NAME = "test-2-network"
ATTACHMENT_NAME = "test-2"
TARGET_SERVICE = f"projects/{PROJECT_ID}/regions/{REGION}/serviceAttachments/<service-attachment-id>"  # Replace with your service attachment ID



credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))

def create_network_attachment(project_id, region, network_name, attachment_name, target_service):
    client = compute_v1.NetworkAttachmentsClient(credentials=credentials)

    attachment = compute_v1.NetworkAttachment(
        name=attachment_name,
        network=f"projects/{project_id}/global/networks/{network_name}",
        target_service=target_service,
        connection_preference=compute_v1.NetworkAttachment.ConnectionPreference.ACCEPT_AUTOMATIC,
    )

    request = compute_v1.InsertNetworkAttachmentRequest(
        project=project_id, region=region, network_attachment_resource=attachment
    )

    operation = client.insert(request=request)
    print(f"Creating network attachment '{attachment_name}'...")
    wait_for_operation(project_id, region, operation.name)
    print(f"Network attachment '{attachment_name}' created successfully!")

def wait_for_operation(project_id, region, operation_name):
    client = compute_v1.RegionOperationsClient(credentials=credentials)
    while True:
        operation = client.get(project=project_id, region=region, operation=operation_name)
        if operation.status == compute_v1.Operation.Status.DONE:
            if operation.error:
                raise Exception(f"Operation failed: {operation.error}")
            print("Operation completed successfully.")
            break
        print("Waiting for operation...")

if __name__ == "__main__":
    create_network_attachment(PROJECT_ID, REGION, NETWORK_NAME, ATTACHMENT_NAME, TARGET_SERVICE)
