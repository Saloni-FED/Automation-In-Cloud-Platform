from flask import Flask, jsonify, request
from google.cloud import functions_v2, eventarc_v1
from google.oauth2 import service_account
from google.api_core import exceptions
from google.iam.v1 import policy_pb2, iam_policy_pb2
import json
from flask_cors import CORS
import os
from google.cloud import storage


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/deploy', methods=['POST'])
def deploy_function_and_create_trigger():
    # Get data from the frontend
    data = request.json
    
    # Configuration
    project_id = "able-stock-428615-n4"
    region = "us-central1"
    function_name = data['functionName']
    trigger_name = data['triggerName']
    bucket_name = data['bucketName'] if data['source'] == 'Cloud Storage' else None
    service_path = f"/{function_name}"
    
    zip_file_path = 'function-source.zip'

    # Service Account credentials
    credentials_json = """
    {
      "type": "service_account",
      "project_id": "able-stock-428615-n4",
      "private_key_id": "8b11902e6c08f9182d09f3cc668682b564c66995",
      "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDUd8YX+/aIjw1l\\nXZegQMOpMWwM4jb4gHIER2PTUF1b5XI83Ayr8rjeonT56A8Bz5xXT5UDZHhi2ByG\\n8HerJTpmihbRuS0rU7nimKP7PrJSoonl3nQiWxGoYuVi023avD15iPkGSFi5uBxr\\n55i+xfZs+7I93zZHTDo3ZW0xOCzFM6yEyiXes8QiULf3hIMliMdWhKboVHU39Zxn\\nMEUvKW6uZqZ0aWkKa0SeKFZvTcHhfDKIvvxbquKEe8B6TfxQrf0iczSEHybAzToz\\nQZo7YbQ1a9fkMroMUQFpvCMb/VQ0YtnFBXuURc2al3pMeY9rbtORhQqle0n6gH3K\\nYq9WTlnBAgMBAAECggEAItYen0kbQ4m9Bw1A8rAbxK6LSlN+8uDQkP4Jkpi/LfWh\\ndPQZicnq4OofJuiTKVdaiYBNbPh4urA3gTKFVITunehvVGS50LxSIqKnZGcDwwPO\\ne2etgAKRkxvgA4OqI+6wX7CDMDIFhjH3SwP2qfT4cicUswtZsXgApZuWOzc8M/r3\\n9b2T4UdsXNLHCtWy4WfO1FTNbbACmwPQ06RKzdlD547bTZmkGDcqYL46NEitS45k\\nHSzN7XK5z+8Dd+Doo8WYKgDIb6YbgXklIyUmLiOmTEPiQ/XLCQ/4X/ud5FOnF21U\\nO+IDfoK5Cl5+LBixFfcQpVtwOo+N6rKqfnY0mL0k3wKBgQDzlpSerejTi37zD7op\\nEpifu/c2NYD9UHR63ZXOnJWkUhgXJazk0kJ0nlaUoMeFmxbdWI3sOGKoTjXbAbzU\\nLOPd82H9OmmXdQpbt6XOq0/ChDu2mfQbln+GDttiTfrUDqko9m8GlkRoCALNwBbX\\nesqe3JGvLGTZwYVTvCgrZr4kmwKBgQDfS0Cmp0wxcaOKwq3OP7Xvcol9vgxvskWQ\\nJB9dwa/98Y67m/N5QHrM4Wri+CjU9Pwrfqtrl4PyoRRws1f0glE6lDyf5oFeqFBF\\n+p53tSTo0duygzG+BLnZmoMIZZ/Jv944ht8utgc4cqfpLZr5cK31iiAGbvrEdT3j\\n+XYV8Spq0wKBgEWC/RpjKoPj1PBr1oYOBnve2ecgUZT4NqUxQqTZTmK8Ap/oYnRS\\nBCDfZnm3f/iCj33O3YFBffXli7zZvBcYUFZwM9BdsPBFuBUATVKy1Gn/7kJnoJ+W\\nzQFmj/h3pFKLdH56BKjujMrbLmGkpWAMbHH1I6XHl2gEr5V7pkLsaOptAoGBAJpr\\nJjiZ9Z0z409wtlWtxZnj8aVdqqgL9wNpl6905MqPJJAll0jBCKtrMEnqKAKtsT47\\nCT0MuRkvwDz4KdlTzeze2tYRyGG3sFvUp4ZNZUsE5hQbmmi4R/ZuXjOOY+RXpcwd\\nqXZaN8AXunsNKOFbxVHKxb7tPMpj8fsYZ0thTl41AoGAB3uqZ55O6vo7srd77xsc\\nPtTz3rDWOnmZG0BwXaU5cpFtyzWmg32sOPvLseYMz22MUn4B2b/JN83q3HdG5nxM\\n2+I0pvzpwPj3HA6rDJzf2TxVEl3lAo+wqf5FjVz+cblqgfNCmu+nHyEp/uch9WaF\\nXqYi2V+AREqOyKq4i1vDC4Y=\\n-----END PRIVATE KEY-----\\n",
      "client_email": "test-2@able-stock-428615-n4.iam.gserviceaccount.com",
      "client_id": "112248088088723126178",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-2%40able-stock-428615-n4.iam.gserviceaccount.com"
    }
    """

    # Load credentials from JSON
    credentials_dict = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    storage_client = storage.Client(credentials=credentials, project=project_id)
    bucket_name_create = "workik-bucket"

    try:
        # Create the bucket if it does not exist
        bucket = storage_client.bucket(bucket_name_create)
        if not bucket.exists():
            bucket = storage_client.create_bucket(bucket_name_create, location="us-central1")
            app.logger.info(f"Bucket {bucket_name_create} created successfully in location us-central1")
        else:
            app.logger.info(f"Bucket {bucket_name_create} already exists")

        # Upload the file to the bucket
        blob = bucket.blob(f"{function_name}/function-source.zip")
        blob.upload_from_filename(zip_file_path)
        app.logger.info(f"File {zip_file_path} uploaded to bucket {bucket_name_create} under path {function_name}/function-source.zip")
    
    except exceptions.GoogleAPICallError as e:
        app.logger.error(f"Bucket creation or file upload error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Bucket creation or file upload failed: {str(e)}"
        }), 500
    except Exception as e:
        app.logger.error(f"Unexpected error during bucket creation or file upload: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred during bucket creation or file upload"
        }), 500
    
    try:
       
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
        function.build_config.source.storage_source.bucket = bucket_name_create
        function.build_config.source.storage_source.object_ = f"{function_name}/function-source.zip"

        # Set up service config
        function.service_config = functions_v2.ServiceConfig()
        function.service_config.available_memory = "256M"
        function.service_config.timeout_seconds = 120
        function.service_config.ingress_settings = functions_v2.ServiceConfig.IngressSettings.ALLOW_ALL
        function.service_config.all_traffic_on_latest_revision = True
        function.service_config.max_instance_count = 1

        # Deploy the Cloud Function
        operation = functions_client.create_function(
            request={"parent": function_parent, "function": function, "function_id": function_name}
        )

        # Wait for the operation to complete and get the result
        response = operation.result()
        app.logger.info(f"Function deployed: {response.name}")

        # Step 2: Make the function publicly accessible
        app.logger.info("Setting IAM policy...")
        
        # Get the current IAM policy
        get_iam_request = iam_policy_pb2.GetIamPolicyRequest(
            resource=response.name
        )
        policy = functions_client.get_iam_policy(request=get_iam_request)

        # Create a new binding
        binding = policy_pb2.Binding()
        binding.role = "roles/cloudfunctions.invoker"
        binding.members.append("allUsers")
        
        # Create a new policy
        new_policy = policy_pb2.Policy()
        new_policy.version = 3
        new_policy.bindings.append(binding)

        # Set the IAM policy
        set_iam_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=response.name,
            policy=new_policy
        )
        
        functions_client.set_iam_policy(request=set_iam_request)
        app.logger.info("Function is now publicly accessible")

        # Step 3: Create Eventarc trigger
        app.logger.info("Creating Eventarc trigger...")
        
        # Initialize Eventarc client
        eventarc_client = eventarc_v1.EventarcClient(credentials=credentials)

        # Define the Cloud Run destination
        destination = eventarc_v1.Destination(
            cloud_run=eventarc_v1.CloudRun(
                service=function_name,
                path=service_path,
                region=region
            )
        )

        # Define the trigger based on the source
        trigger = eventarc_v1.Trigger(
            name=f"{function_parent}/triggers/{trigger_name}",
            destination=destination,
            service_account=data['serviceEmail']
        )

        if data['source'] == 'Cloud Storage':
            trigger.event_filters = [
                eventarc_v1.EventFilter(
                    attribute="type",
                    value=data['eventType']
                ),
                eventarc_v1.EventFilter(
                    attribute="bucket",
                    value=data['bucketName']
                )
            ]
        elif data['source'] == 'Cloud Firestore':
            trigger.event_filters = [
                eventarc_v1.EventFilter(
                    attribute="type",
                    value="google.cloud.firestore.document.v1.written"
                ),
                eventarc_v1.EventFilter(
                    attribute="document",
                    value=f"projects/{project_id}/databases/(default)/documents/{data['collectionPath']}/{data['documentPath']}"
                )
            ]
        elif data['source'] == 'Pub/Sub':
            trigger.event_filters = [
                eventarc_v1.EventFilter(
                    attribute="type",
                    value="google.cloud.pubsub.topic.v1.messagePublished"
                ),
                eventarc_v1.EventFilter(
                    attribute="topic",
                    value=data['topicName']
                )
            ]
        elif data['source'] == 'Cloud Scheduler':
            # For Cloud Scheduler, you might need to create a Cloud Scheduler job separately
            # and then use its details to create an Eventarc trigger
            pass
        elif data['source'] == 'HTTP Trigger':
            # For HTTP Trigger, you might not need to create an Eventarc trigger
            # The function is already accessible via HTTP
            pass

        # Create the trigger (if not HTTP Trigger)
        if data['source'] != 'HTTP Trigger':
            trigger_operation = eventarc_client.create_trigger(
                request={
                    "parent": function_parent,
                    "trigger": trigger,
                    "trigger_id": trigger_name,
                }
            )
            trigger_result = trigger_operation.result()
            app.logger.info(f"Trigger created successfully: {trigger_result.name}")

        return jsonify({
            "status": "success",
            "message": "Function deployed and trigger created successfully",
            "function_name": response.name,
            "trigger_name": trigger_result.name if data['source'] != 'HTTP Trigger' else "N/A"
        }), 200

    except exceptions.GoogleAPICallError as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)

