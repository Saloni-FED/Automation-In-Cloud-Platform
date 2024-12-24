import boto3
import json
from flask import Flask, request, jsonify
from flask_cors import CORS 

# ------------------- Flask App Setup -------------------
app = Flask(__name__)
CORS(app)

# ------------------- Configuration Parameters -------------------
connection_name = "external-api-connection"  # EventBridge Connection Name
api_destination_name = "send-s3-events-api"  # API Destination Name
external_api_endpoint = "https://insect-uncommon-luckily.ngrok-free.app/eventbridge"  # External API URL
api_key_name = "x-api-key"  # API Key Header
api_key_value = "saloni"  # API Key Value
role_arn = "arn:aws:iam::054037123559:role/EventBridgeInvokeRole"  # IAM Role ARN


# ------------------- Step 1: Create EventBridge Connection -------------------
def create_eventbridge_connection():
    event_client = boto3.client('events')

    try:
        response = event_client.create_connection(
            Name=connection_name,
            AuthorizationType='API_KEY',
            AuthParameters={
                'ApiKeyAuthParameters': {
                    'ApiKeyName': api_key_name,
                    'ApiKeyValue': api_key_value
                }
            }
        )
        print(f"[SUCCESS] EventBridge Connection Created: {response['ConnectionArn']}")
        return response['ConnectionArn']

    except event_client.exceptions.ResourceAlreadyExistsException:
        # If connection already exists, fetch its details
        response = event_client.describe_connection(Name=connection_name)
        print(f"[INFO] Connection '{connection_name}' already exists. Using existing Connection ARN.")
        return response['ConnectionArn']


# ------------------- Step 2: Create API Destination -------------------
def create_api_destination(connection_arn):
    event_client = boto3.client('events')

    try:
        response = event_client.create_api_destination(
            Name=api_destination_name,
            ConnectionArn=connection_arn,
            InvocationEndpoint=external_api_endpoint,
            HttpMethod='POST'
        )
        print(f"[SUCCESS] API Destination Created: {response['ApiDestinationArn']}")
        return response['ApiDestinationArn']

    except event_client.exceptions.ResourceAlreadyExistsException:
        print(f"[INFO] API Destination '{api_destination_name}' already exists. Skipping creation.")
        response = event_client.describe_api_destination(Name=api_destination_name)
        return response['ApiDestinationArn']


# ------------------- Step 3: Create EventBridge Rule -------------------
def create_eventbridge_rule(rule_name, event_pattern, api_destination_arn):
    event_client = boto3.client('events')

    # Create EventBridge rule with dynamic input
    response = event_client.put_rule(
        Name=rule_name,
        EventPattern=json.dumps(event_pattern),
        State='ENABLED'
    )
    print(f"[SUCCESS] EventBridge Rule Created: {response['RuleArn']}")

    # Attach API Destination as a target with Role ARN
    event_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': 'api-destination-target',
                'Arn': api_destination_arn,
                'RoleArn': role_arn
            }
        ]
    )
    print(f"[SUCCESS] API Destination attached as target to the rule.")


# ------------------- POST Method Endpoint -------------------
@app.route("/create-eventbridge-rule", methods=["POST"])
def create_rule():
    try:
        # Get user input from frontend request
        data = request.json
        print(f"Received data: {data}")

        # Extract rule_name and event_pattern
        rule_name = data.get("rule_name")
        event_pattern = data.get("event_pattern", {})

        # Extract fields dynamically
        source = event_pattern.get("source", [None])[0]  # First element of source array
        detail_type = event_pattern.get("detail-type", [])  # List of detail types
        bucket_name = None

        # Check for 'detail' and bucket name
        if "detail" in event_pattern and "bucket" in event_pattern["detail"]:
            bucket = event_pattern["detail"]["bucket"]
            if isinstance(bucket, str):  # Handle case where bucket is a string
                bucket_name = bucket
            elif isinstance(bucket, dict):  # Handle dictionary with 'name'
                bucket_name = bucket.get("name", [None])[0]

        # Validate required fields
        if not rule_name or not source or not detail_type:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Log the extracted data
        print(f"Rule Name: {rule_name}")
        print(f"Source: {source}")
        print(f"Detail-Type: {detail_type}")
        print(f"Bucket Name: {bucket_name}")

        # Construct final event pattern
        final_event_pattern = {
            "source": [source],
            "detail-type": detail_type
        }
        if bucket_name:  # Add bucket name only if provided
            final_event_pattern["detail"] = {"bucket": {"name": [bucket_name]}}

        print(f"Constructed Final Event Pattern: {final_event_pattern}")

        # Step-by-step execution
        connection_arn = create_eventbridge_connection()
        api_destination_arn = create_api_destination(connection_arn)
        create_eventbridge_rule(rule_name, final_event_pattern, api_destination_arn)

        return jsonify({
            "status": "success",
            "message": f"EventBridge rule '{rule_name}' created successfully!",
            "rule_name": rule_name,
            "event_pattern": final_event_pattern
        }), 200

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500




# ------------------- Main Function -------------------
if __name__ == "__main__":
    print("Starting Flask server for dynamic EventBridge rule creation...")
    app.run(debug=True, host="0.0.0.0", port=5500)
