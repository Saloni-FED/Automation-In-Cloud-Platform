from google.cloud import functions_v2
from google.oauth2 import service_account
from google.api_core import exceptions
import json
from google.iam.v1 import policy_pb2, iam_policy_pb2
import os

def deploy_python_function():
    # Previous credentials and setup code remains the same...
    project_id = "able-stock-428615-n4"
    region = "us-central1"
    function_name = "function-7"

    

    # Load credentials from JSON
    credentials_dict = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    # Initialize the Functions client
    functions_client = functions_v2.FunctionServiceClient(credentials=credentials)

    # Define the Cloud Function's parent path
    function_parent = f"projects/{project_id}/locations/{region}"

    # Create the function resource
    function = functions_v2.Function()
    function.name = f"{function_parent}/functions/{function_name}"
    function.description = "HTTP-triggered Cloud Function"
    
    # Set up build config
    function.build_config = functions_v2.BuildConfig()
    function.build_config.runtime = "nodejs20"
    function.build_config.entry_point = "helloHttp"
    function.build_config.source = functions_v2.Source()
    function.build_config.source.storage_source = functions_v2.StorageSource()
    function.build_config.source.storage_source.bucket = "test--2-for-event-arc"
    function.build_config.source.storage_source.object_ = "function-source.zip"

    # Set up service config
    function.service_config = functions_v2.ServiceConfig()
    function.service_config.available_memory = "256M"
    function.service_config.timeout_seconds = 120
    function.service_config.ingress_settings = functions_v2.ServiceConfig.IngressSettings.ALLOW_ALL
    function.service_config.all_traffic_on_latest_revision = True
    function.service_config.max_instance_count = 1

    # Set up HTTP trigger
    function.service_config.uri = f"https://{region}-{project_id}.cloudfunctions.net/{function_name}"

    try:
        # Deploy the Cloud Function
        operation = functions_client.create_function(
            request={"parent": function_parent, "function": function, "function_id": function_name}
        )

        # Wait for the operation to complete and get the result
        response = operation.result()
        print(f"Function deployed: {response.name}")

        # Get the current IAM policy
        get_iam_request = iam_policy_pb2.GetIamPolicyRequest(
            resource=response.name
        )
        policy = functions_client.get_iam_policy(request=get_iam_request)

        # Create a new binding
        binding = policy_pb2.Binding()
        binding.role = "roles/cloudfunctions.invoker"  # Use cloudfunctions.invoker instead of run.invoker
        binding.members.append("allUsers")
        
        # Create a new policy
        new_policy = policy_pb2.Policy()
        new_policy.version = 3  # Use IAM Policy version 3
        new_policy.bindings.append(binding)

        # Set the IAM policy
        set_iam_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=response.name,
            policy=new_policy
        )
        
        functions_client.set_iam_policy(request=set_iam_request)
        print("Function is now publicly accessible (unauthenticated)")
    except exceptions.GoogleAPICallError as e:
        print(f"Error deploying function: {str(e)}")

# Call the deploy function
if __name__ == "__main__":
    deploy_python_function()