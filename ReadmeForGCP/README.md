# README: How to Obtain Google Cloud Service Account JSON Key

This guide explains how to obtain your Google Cloud Service Account JSON key, which is required for programmatic access to GCP services such as Google Cloud Storage.

---

## Prerequisites
- An active **Google Cloud Platform (GCP)** account.
- IAM permissions to create or manage **Service Accounts**.
- Programmatic access to GCP services (e.g., using the Google Cloud SDK or Python libraries).

---

## Steps to Obtain Service Account JSON Key

### 1. Log in to Google Cloud Console
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Log in using your Google account credentials.

### 2. Navigate to the IAM & Admin Section
   - From the left-hand menu, go to **IAM & Admin** > **Service Accounts**.

### 3. Create or Select a Service Account
   - **Option A**: To create a new service account:
     1. Click on **Create Service Account**.
     2. Provide a **name** and **description** for the service account (e.g., `storage-access`).
     3. Click **Create and Continue**.

   - **Option B**: To use an existing service account:
     1. Find the desired service account in the list.
     2. Click on the service account name to open its details.

### 4. Assign Permissions to the Service Account
   - Assign the required permissions for the service account. For example, to list storage buckets:
     1. Click **Add Another Role**.
     2. Search for and select **Storage Viewer**.
     3. Click **Continue** to finish.

### 5. Generate the Service Account JSON Key
   - Navigate to the **Keys** tab of the service account.
   - Click **Add Key** > **Create New Key**.
   - Select **JSON** as the key type.
   - Download the JSON file containing the service account credentials. Save this file securely as it contains sensitive information.

---

## Security Best Practices
- **Do not share your JSON key publicly**: Avoid uploading the file to public repositories or sharing it in unsecured channels.
- **Use environment variables or secret management tools**: Store credentials securely in environment variables or tools like HashiCorp Vault or AWS Secrets Manager.
- **Rotate keys regularly**: Delete unused keys and generate new ones periodically for better security.
- **Restrict permissions**: Only assign roles that are necessary for the service account.

---

## References
- [Google Cloud IAM Documentation](https://cloud.google.com/iam/docs/)
- [Service Account Key Management](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
- [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs/)
