from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def test_data():
    return jsonify({"status": "success"}), 200

@app.route("/eventgrid", methods=["POST"])
def handle_eventgrid():
    try:
        # Parse the JSON payload
        event_data = request.get_json()

        # Log the incoming request
        print("[INFO] Received Event Grid data:", event_data)

        # Handle Event Grid Subscription Validation
        if event_data and isinstance(event_data, list):
            first_event = event_data[0]
            if first_event.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
                print("[INFO] Validation event received.")
                validation_code = first_event["data"]["validationCode"]
                validation_response = {"validationResponse": validation_code}
                print(f"[INFO] Returning validation response: {validation_response}")
                return jsonify(validation_response), 200

        # Handle other Event Grid events
        if event_data:
            print("[INFO] Event processed successfully:", event_data)
            return jsonify({"status": "processed"}), 200

        # Default response for unexpected payloads
        return jsonify({"status": "unexpected payload"}), 400

    except Exception as e:
        print(f"[ERROR] Failed to process request: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("[INFO] Starting webhook server...")
    app.run(host="0.0.0.0", port=4000)
