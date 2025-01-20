from flask import Flask, request, jsonify
from google.cloud import storage

app = Flask(__name__)



@app.route("/webhook-eventarc", methods=["POST"])
def handle_storage_event():
    try:
        # Parse the incoming JSON request body
        event = request.get_json()
        print(event)

        # Extract relevant information from the event
        

        # Create a Storage client
        return jsonify({
            "message": "Event received successfully",
            "event": event
        }), 200  # Changed from 200 to 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8900)
