"use client";

import { useState } from "react";
import { XIcon, ChevronDownIcon } from "lucide-react";

const sources = [
  {
    name: "aws.s3",
    types: [
      { type: "Amazon S3 Event Notification", detailFields: ["bucket"] },
      { type: "Object-Level API Call via CloudTrail", detailFields: ["bucket", "object"] },
    ],
    events: ["Object Created", "Object Deleted", "Object Restore Completed"],
  },
  {
    name: "aws.ec2",
    types: [{ type: "EC2 Instance State-change", detailFields: ["instance-id"] }],
    events: ["Instance Started", "Instance Stopped", "Instance Terminated"],
  },
  {
    name: "aws.lambda",
    types: [{ type: "Function Invocation", detailFields: ["function-name"] }],
    events: ["Function Error", "Function Invocation"],
  },
];

const EnhancedEventRuleForm = () => {
  const [selectedSource, setSelectedSource] = useState("");
  const [selectedType, setSelectedType] = useState("");
  const [selectedEvents, setSelectedEvents] = useState([]);
  const [ruleName, setRuleName] = useState("");
  const [details, setDetails] = useState({});
  const [showDropdown, setShowDropdown] = useState(false);

  const handleEventSelect = (event) => {
    if (!selectedEvents.includes(event)) {
      setSelectedEvents([...selectedEvents, event]);
    }
  };

  const removeEvent = (event) => {
    setSelectedEvents(selectedEvents.filter((e) => e !== event));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create dynamic event_pattern
    const eventPattern = {
      source: [selectedSource],
      "detail-type": selectedEvents,
      ...(Object.keys(details).length > 0 && {
        detail: Object.fromEntries(
          Object.entries(details).filter(([_, value]) => value.trim())
        ),
      }),
    };

    const payload = {
      rule_name: ruleName,
      event_pattern: eventPattern,
    };

    console.log("Payload to submit:", payload);

    try {
      const response = await fetch("http://localhost:5500/create-eventbridge-rule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        alert(`Success: ${data.message}`);
      } else {
        alert(`Error: ${data.message}`);
      }

      // Clear form fields
      setRuleName("");
      setSelectedSource("");
      setSelectedType("");
      setSelectedEvents([]);
      setDetails({});
    } catch (error) {
      console.error("Error while sending data:", error);
      alert("An error occurred while creating the EventBridge rule.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg rounded-lg p-8 w-full max-w-lg space-y-6"
      >
        <h2 className="text-2xl font-bold text-gray-800 text-center">Create Event Rule</h2>

        {/* Rule Name */}
        <div>
          <label className="block text-sm font-medium mb-1">Rule Name</label>
          <input
            type="text"
            placeholder="Enter Rule Name"
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
            value={ruleName}
            onChange={(e) => setRuleName(e.target.value)}
            required
          />
        </div>

        {/* Source Dropdown */}
        <div>
          <label className="block text-sm font-medium mb-1">Source</label>
          <select
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
            value={selectedSource}
            onChange={(e) => {
              setSelectedSource(e.target.value);
              setSelectedType("");
              setSelectedEvents([]);
              setDetails({});
            }}
            required
          >
            <option value="">Select Source</option>
            {sources.map((src) => (
              <option key={src.name} value={src.name}>
                {src.name}
              </option>
            ))}
          </select>
        </div>

        {/* Event Type Dropdown */}
        {selectedSource && (
          <div>
            <label className="block text-sm font-medium mb-1">Event Type</label>
            <select
              className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
              value={selectedType}
              onChange={(e) => {
                setSelectedType(e.target.value);
                setDetails({});
              }}
              required
            >
              <option value="">Select Event Type</option>
              {sources
                .find((src) => src.name === selectedSource)
                ?.types.map((type) => (
                  <option key={type.type} value={type.type}>
                    {type.type}
                  </option>
                ))}
            </select>
          </div>
        )}

        {/* Detail Fields */}
        {selectedType &&
          sources
            .find((src) => src.name === selectedSource)
            ?.types.find((type) => type.type === selectedType)
            ?.detailFields.map((field) => (
              <div key={field}>
                <label className="block text-sm font-medium mb-1 capitalize">
                  {field} <span className="text-gray-400">(Optional)</span>
                </label>
                <input
                  type="text"
                  placeholder={`Enter ${field}`}
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  value={details[field] || ""}
                  onChange={(e) => setDetails({ ...details, [field]: e.target.value })}
                />
              </div>
            ))}

        {/* Events Selection */}
        {selectedType && (
          <div>
            <label className="block text-sm font-medium mb-1">Events</label>
            <div
              className="flex items-center justify-between w-full p-3 border rounded-lg cursor-pointer"
              onClick={() => setShowDropdown(!showDropdown)}
            >
              <span>{selectedEvents.length > 0 ? "Selected Events" : "Select Events"}</span>
              <ChevronDownIcon className="w-5 h-5" />
            </div>

            {showDropdown && (
              <div className="absolute z-10 w-full mt-2 bg-white border rounded-lg shadow-lg max-h-48 overflow-y-auto">
                {sources
                  .find((src) => src.name === selectedSource)
                  ?.events.map((event) => (
                    <div
                      key={event}
                      className="p-3 hover:bg-blue-100 cursor-pointer"
                      onClick={() => handleEventSelect(event)}
                    >
                      {event}
                    </div>
                  ))}
              </div>
            )}

            {/* Display Selected Events */}
            <div className="flex flex-wrap gap-2 mt-2">
              {selectedEvents.map((event) => (
                <div
                  key={event}
                  className="flex items-center bg-blue-100 text-blue-700 px-3 py-1 rounded-full"
                >
                  <span>{event}</span>
                  <button
                    type="button"
                    onClick={() => removeEvent(event)}
                    className="ml-2 hover:text-red-500"
                  >
                    <XIcon className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full p-3 text-white bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg hover:from-blue-600 hover:to-purple-700 focus:ring-2 focus:ring-purple-500"
        >
          Create Rule
        </button>
      </form>
    </div>
  );
};

export default EnhancedEventRuleForm;
