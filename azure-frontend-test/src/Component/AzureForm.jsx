import { useState } from "react";

function AzureResourceForm() {
  const [eventTypes, setEventTypes] = useState([]); // Updated to handle multiple event types
  const [resourceType, setResourceType] = useState("");
  const [resourceGroupName, setResourceGroupName] = useState(""); // Updated field
  const [blobName, setBlobName] = useState("");
  const [vmName, setVmName] = useState("");
  const [subscriptionName, setSubscriptionName] = useState(""); // New state for subscription name

  // Resource Types and Event Types Mapping
  const resourceTypes = {
    "Blob Storage": [
      "Microsoft.Storage.BlobCreated",
      "Microsoft.Storage.BlobDeleted",
      "Microsoft.Storage.BlobRenamed",
      "Microsoft.Storage.DirectoryCreated",
      "Microsoft.Storage.DirectoryDeleted"
    ],
    "Virtual Machine": [
      "Microsoft.Compute.VirtualMachineCreated",
      "Microsoft.Compute.VirtualMachineDeleted",
      "Microsoft.Compute.VirtualMachineUpdated",
      "Microsoft.Compute.VirtualMachinePowerOn",
      "Microsoft.Compute.VirtualMachinePowerOff",
      "Microsoft.Compute.VirtualMachineRestarted"
    ],
    "Azure Kubernetes": [
      "Microsoft.ContainerService.ClusterCreated",
      "Microsoft.ContainerService.ClusterDeleted",
      "Microsoft.ContainerService.NodePoolAdded",
      "Microsoft.ContainerService.NodePoolDeleted"
    ],
    "Azure App Service": [
      "Microsoft.Web.AppCreated",
      "Microsoft.Web.AppDeleted",
      "Microsoft.Web.AppUpdated",
      "Microsoft.Web.SlotSwapped",
      "Microsoft.Web.AppServicePlanCreated",
      "Microsoft.Web.AppServicePlanDeleted"
    ],
    "Azure SQL": [
      "Microsoft.Sql.DatabaseCreated",
      "Microsoft.Sql.DatabaseDeleted",
      "Microsoft.Sql.DatabaseUpdated",
      "Microsoft.Sql.DatabasePaused",
      "Microsoft.Sql.DatabaseResumed"
    ],
    "Azure Key Vault": [
      "Microsoft.KeyVault.VaultCreated",
      "Microsoft.KeyVault.VaultDeleted",
      "Microsoft.KeyVault.SecretCreated",
      "Microsoft.KeyVault.SecretDeleted",
      "Microsoft.KeyVault.VaultAccessPolicyChanged",
      "Microsoft.KeyVault.SecretNewVersionCreated",
      "Microsoft.KeyVault.KeyNewVersionCreated"
    ],
    "Azure Event Hubs": [
      "Microsoft.EventHub.CaptureFileCreated",
      "Microsoft.EventHub.CaptureFileDeleted"
    ],
    "Azure IoT Hub": [
      "Microsoft.Devices.DeviceConnected",
      "Microsoft.Devices.DeviceDisconnected",
      "Microsoft.Devices.DeviceCreated",
      "Microsoft.Devices.DeviceDeleted"
    ],
    "Azure Cosmos DB": [
      "Microsoft.DocumentDB.DatabaseCreated",
      "Microsoft.DocumentDB.DatabaseDeleted",
      "Microsoft.DocumentDB.CollectionCreated",
      "Microsoft.DocumentDB.CollectionDeleted"
    ],
    "Azure Functions": [
      "Microsoft.Web.FunctionExecutionStarted",
      "Microsoft.Web.FunctionExecutionCompleted",
      "Microsoft.Web.FunctionExecutionFailed"
    ],
    "Azure Backup": [
      "Microsoft.RecoveryServices.BackupStarted",
      "Microsoft.RecoveryServices.BackupCompleted",
      "Microsoft.RecoveryServices.BackupFailed"
    ],
    "Azure Resource Manager": [
      "Microsoft.Resources.ResourceWriteSuccess",
      "Microsoft.Resources.ResourceWriteFailure",
      "Microsoft.Resources.ResourceDeleteSuccess",
      "Microsoft.Resources.ResourceDeleteFailure"
    ],
    "Azure Logic Apps": [
      "Microsoft.Logic.WorkflowRunStarted",
      "Microsoft.Logic.WorkflowRunCompleted",
      "Microsoft.Logic.WorkflowRunFailed"
    ],
    "Azure Machine Learning": [
      "Microsoft.MachineLearningServices.ModelRegistered",
      "Microsoft.MachineLearningServices.RunCompleted",
      "Microsoft.MachineLearningServices.RunFailed"
    ],
    "Azure Service Bus": [
      "Microsoft.ServiceBus.ActiveMessages",
      "Microsoft.ServiceBus.DeadLetterMessages"
    ],
    "Azure Network Resources": [
      "Microsoft.Network.LoadBalancerCreated",
      "Microsoft.Network.LoadBalancerDeleted",
      "Microsoft.Network.ApplicationGatewayCreated",
      "Microsoft.Network.ApplicationGatewayDeleted"
    ],
    "Azure DevOps": [
      "Microsoft.DevOps.PipelineRunStarted",
      "Microsoft.DevOps.PipelineRunCompleted"
    ],
    "Azure Event Grid": [
      "Microsoft.EventGrid.SubscriptionDeleted",
      "Microsoft.EventGrid.SubscriptionUpdated"
    ]
  };

  const handleResourceChange = (e) => {
    const selectedResource = e.target.value;
    setResourceType(selectedResource);
    setEventTypes([]); // Reset event types when resource type changes
    setBlobName(""); // Reset conditional inputs
    setVmName("");
  };

  const handleEventTypeChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions, (option) => option.value);
    setEventTypes(selectedOptions);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = {
      eventTypes,
      resourceType,
      resourceGroupName, // Updated field
      blobName: resourceType === "Blob Storage" ? blobName : undefined,
      vmName: resourceType === "Virtual Machine" ? vmName : undefined,
      subscriptionName, // Use the dynamic subscription name
    };

    try {
      const response = await fetch("http://127.0.0.1:4800/create_event_subscription", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        alert("Event Subscription created successfully:\n" + JSON.stringify(result, null, 2));
      } else {
        alert("Error creating Event Subscription:\n" + JSON.stringify(result, null, 2));
      }
    } catch (error) {
      alert("An error occurred:\n" + error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <form
        className="bg-white p-6 rounded shadow-md w-full max-w-lg"
        onSubmit={handleSubmit}
      >
        <h1 className="text-2xl font-bold mb-4">Azure Resource Form</h1>

        {/* Subscription Name */}
        <div className="mb-4">
          <label htmlFor="subscriptionName" className="block text-gray-700 font-bold mb-2">
            Event Subscription Name
          </label>
          <input
            type="text"
            id="subscriptionName"
            value={subscriptionName}
            onChange={(e) => setSubscriptionName(e.target.value)}
            className="w-full border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter subscription name"
            required
          />
        </div>

        {/* Resource Type */}
        <div className="mb-4">
          <label htmlFor="resourceType" className="block text-gray-700 font-bold mb-2">
            Resource Type
          </label>
          <select
            id="resourceType"
            value={resourceType}
            onChange={handleResourceChange}
            className="w-full border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select a resource type</option>
            {Object.keys(resourceTypes).map((resource) => (
              <option key={resource} value={resource}>
                {resource}
              </option>
            ))}
          </select>
        </div>

        {/* Event Types (Multi-Select) */}
        {resourceType && (
          <div className="mb-4">
            <label htmlFor="eventTypes" className="block text-gray-700 font-bold mb-2">
              Event Types
            </label>
            <select
              id="eventTypes"
              multiple
              value={eventTypes}
              onChange={handleEventTypeChange}
              className="w-full border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {resourceTypes[resourceType]?.map((event) => (
                <option key={event} value={event}>
                  {event}
                </option>
              ))}
            </select>
            <p className="text-gray-600 text-sm mt-1">
              Hold <b>Ctrl</b> (Windows) or <b>Cmd</b> (Mac) to select multiple options.
            </p>
          </div>
        )}

        {/* Resource Group Name */}
        <div className="mb-4">
          <label htmlFor="resourceGroupName" className="block text-gray-700 font-bold mb-2">
            Resource Group Name
          </label>
          <input
            type="text"
            id="resourceGroupName"
            value={resourceGroupName}
            onChange={(e) => setResourceGroupName(e.target.value)}
            className="w-full border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter resource group name"
            required
          />
        </div>

        {/* Conditional Inputs */}
        {resourceType === "Blob Storage" && (
          <div className="mb-4">
            <label htmlFor="blobName" className="block text-gray-700 font-bold mb-2">
              Blob Name
            </label>
            <input
              type="text"
              id="blobName"
              value={blobName}
              onChange={(e) => setBlobName(e.target.value)}
              className="w-full border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter blob name"
            />
          </div>
        )}

        {resourceType === "Virtual Machine" && (
          <div className="mb-4">
            <label htmlFor="vmName" className="block text-gray-700 font-bold mb-2">
              VM Name
            </label>
            <input
              type="text"
              id="vmName"
              value={vmName}
              onChange={(e) => setVmName(e.target.value)}
              className="w-full border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter virtual machine name"
            />
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Submit
        </button>
      </form>
    </div>
  );
}

export default AzureResourceForm;
