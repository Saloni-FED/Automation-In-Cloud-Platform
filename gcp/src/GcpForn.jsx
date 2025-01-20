import { useState } from "react";

function GcpForm() {
  const [formData, setFormData] = useState({
    functionName: "",
    triggerName: "",
    serviceEmail: "",
    source: "Cloud Storage",
    bucketName: "",
    eventType: "google.cloud.storage.object.v1.finalized",
    collectionPath: "",
    documentPath: "",
    topicName: "",
    cronSchedule: "",
    timezone: "",
    endpointUrl: "",
  });

  const [responseMessage, setResponseMessage] = useState("");

  // Handle form field changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/deploy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      setResponseMessage(result.message);
      console.log(result);
    } catch (error) {
      setResponseMessage("Error deploying function.");
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white shadow-md rounded-lg p-8 max-w-md w-full">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">
          Cloud Function Deployment
        </h1>
        <form onSubmit={handleSubmit}>
          {/* Function Name */}
          <div className="mb-4">
            <label className="block text-gray-700 font-medium mb-2">
              Function Name
            </label>
            <input
              type="text"
              name="functionName"
              value={formData.functionName}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          {/* Trigger Name */}
          <div className="mb-4">
            <label className="block text-gray-700 font-medium mb-2">
              Trigger Name
            </label>
            <input
              type="text"
              name="triggerName"
              value={formData.triggerName}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          {/* Service Email */}
          <div className="mb-4">
            <label className="block text-gray-700 font-medium mb-2">
              Service Email
            </label>
            <input
              type="email"
              name="serviceEmail"
              value={formData.serviceEmail}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          {/* Source Dropdown */}
          <div className="mb-4">
            <label className="block text-gray-700 font-medium mb-2">
              Source
            </label>
            <select
              name="source"
              value={formData.source}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Cloud Storage">Cloud Storage</option>
              <option value="Cloud Firestore">Cloud Firestore</option>
              <option value="Pub/Sub">Pub/Sub</option>
              <option value="Cloud Scheduler">Cloud Scheduler</option>
              <option value="HTTP Trigger">HTTP Trigger</option>
            </select>
          </div>

          {/* Conditional Fields based on Source */}
          {formData.source === "Cloud Storage" && (
            <>
              <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">
                  Bucket Name
                </label>
                <input
                  type="text"
                  name="bucketName"
                  value={formData.bucketName}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">
                  Event Type
                </label>
                <select
                  name="eventType"
                  value={formData.eventType}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="google.cloud.storage.object.v1.finalized">
                    Object Finalized
                  </option>
                  <option value="google.cloud.storage.object.v1.deleted">
                    Object Deleted
                  </option>
                </select>
              </div>
            </>
          )}

          {formData.source === "Cloud Firestore" && (
            <>
              <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">
                  Collection Path
                </label>
                <input
                  type="text"
                  name="collectionPath"
                  value={formData.collectionPath}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">
                  Document Path (Optional)
                </label>
                <input
                  type="text"
                  name="documentPath"
                  value={formData.documentPath}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </>
          )}

          {formData.source === "Pub/Sub" && (
            <div className="mb-4">
              <label className="block text-gray-700 font-medium mb-2">
                Topic Name
              </label>
              <input
                type="text"
                name="topicName"
                value={formData.topicName}
                onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          )}

          {formData.source === "Cloud Scheduler" && (
            <>
              <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">
                  Cron Schedule
                </label>
                <input
                  type="text"
                  name="cronSchedule"
                  value={formData.cronSchedule}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-gray-700 font-medium mb-2">
                  Timezone
                </label>
                <input
                  type="text"
                  name="timezone"
                  value={formData.timezone}
                  onChange={handleChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </>
          )}

          {formData.source === "HTTP Trigger" && (
            <div className="mb-4">
              <label className="block text-gray-700 font-medium mb-2">
                Endpoint URL
              </label>
              <input
                type="text"
                name="endpointUrl"
                value={formData.endpointUrl}
                onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          )}

          <div>
            <button
              type="submit"
              className="w-full bg-blue-500 text-white font-bold py-3 rounded-lg hover:bg-blue-600 transition duration-300"
            >
              Deploy Function
            </button>
          </div>
        </form>
        {responseMessage && (
          <div className="mt-4 p-3 bg-green-100 text-green-700 rounded-lg">
            {responseMessage}
          </div>
        )}
      </div>
    </div>
  );
}

export default GcpForm;

