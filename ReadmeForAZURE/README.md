# README: How to Obtain Azure Credentials

This guide explains how to obtain your Azure credentials (`Tenant ID`, `Client ID`, `Client Secret`, and `Subscription ID`) required for programmatic access to Azure services.

---

## Prerequisites
- An active **Microsoft Azure** account.
- Permissions to create and manage Azure Active Directory (Azure AD) applications.
- Access to the Azure Portal.

---

## Steps to Obtain Azure Credentials

### 1. Log in to Azure Portal
   - Visit the [Azure Portal](https://portal.azure.com/).
   - Log in using your Azure account credentials.

---

### 2. Navigate to Azure Active Directory
   - From the left-hand menu, select **Azure Active Directory**.

---

### 3. Register an Application
   - Under **Manage**, click on **App registrations**.
   - Click on **New registration**.
   - Provide a **name** for your application (e.g., `ResourceManagementApp`).
   - Select **Accounts in this organizational directory only**.
   - Click **Register** to create the application.

---

### 4. Obtain Application (Client) ID and Tenant ID
   - After registering the application, go to the **Overview** page.
   - Copy the **Application (client) ID** and **Directory (tenant) ID**. These will be used as `CLIENT_ID` and `TENANT_ID`.

---

### 5. Create a Client Secret
   - Under **Manage**, go to **Certificates & secrets**.
   - Click on **New client secret**.
   - Add a description (e.g., `DefaultSecret`) and select an expiration period.
   - Click **Add**.
   - Copy the **Value** of the client secret. This will be used as `CLIENT_SECRET`.  
     **Note**: You won't be able to view the value again, so save it securely.

---

### 6. Assign a Role to the Application
   - Navigate to your **Subscription** in the Azure Portal:
     1. From the left-hand menu, go to **Subscriptions**.
     2. Select the subscription you want to manage.
   - Under **Access control (IAM)**, click **Add** > **Add role assignment**.
   - Select a role (e.g., `Contributor` or `Reader`) that grants the necessary permissions.
   - Assign the role to your registered application by searching for its name.
   - Save the changes.

---

### 7. Obtain the Subscription ID
   - In the **Subscriptions** page, select the subscription you want to use.
   - Copy the **Subscription ID**. This will be used as `SUBSCRIPTION_ID`.

---

## Security Best Practices
- **Do not share your credentials publicly**: Avoid uploading credentials to public repositories or sharing them insecurely.
- **Store secrets securely**: Use tools like Azure Key Vault or environment variables to store credentials securely.
- **Rotate secrets regularly**: Delete and regenerate client secrets periodically to enhance security.
- **Restrict permissions**: Assign only the necessary roles and permissions to your application.

---

## References
- [Azure Active Directory Documentation](https://learn.microsoft.com/en-us/azure/active-directory/)
- [App Registrations in Azure AD](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Azure Resource Management Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/)

