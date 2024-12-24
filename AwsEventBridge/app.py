from flask import Flask, request, jsonify

app = Flask(__name__)
import logging

logging.basicConfig(level=logging.DEBUG)



@app.route('/eventbridge', methods=['POST'])
def handle_event():
    # Parse the incoming EventBridge event
    event = request.json
    api_key = request.headers.get('x-api-key')
    print("Received Event:", event)

    # Process the event (e.g., log, store, or trigger automation)
    if event.get("detail-type") == "Object Created":
        bucket_name = event["detail"]["bucket"]["name"]
        object_key = event["detail"]["object"]["key"]
        print(f"Object Created in Bucket: {bucket_name}, Key: {object_key}")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(debug=True)  
