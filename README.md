# README: How to Obtain AWS Access Key ID and Secret Access Key

This guide explains how to obtain your AWS `Access Key ID` and `Secret Access Key`, which are required for programmatic access to AWS services such as S3.

---

## Prerequisites
- An active AWS account.
- IAM permissions to create or manage users.
- Programmatic access to AWS services (e.g., using the AWS CLI or SDKs).

---

## Steps to Obtain Access Key ID and Secret Access Key

### 1. Log in to AWS Management Console
   - Visit the [AWS Management Console](https://aws.amazon.com/console/).
   - Sign in using your AWS account credentials.

### 2. Navigate to the IAM Management Page
   - In the AWS Management Console, search for **IAM** in the search bar.
   - Click on **IAM (Identity and Access Management)**.

### 3. Create or Select a User
   - **Option A**: If you already have an IAM user:
     1. Click on **Users** from the left sidebar.
     2. Select the user for whom you want to generate the access keys.

   - **Option B**: To create a new user:
     1. Click on **Users** > **Add users**.
     2. Enter a **User name** (e.g., `s3-access-user`).
     3. Check the box for **Access key - Programmatic access**.
     4. Click **Next** to set permissions.

### 4. Assign Permissions
   - Attach the appropriate policy to the user:
     - If the user requires access to all S3 buckets, attach the **AmazonS3FullAccess** policy.
     - Alternatively, create a custom policy with the specific S3 permissions needed (e.g., `s3:ListBucket` and `s3:GetObject`).
   - Complete the user creation process by clicking **Next** > **Create user**.

### 5. Generate Access Keys
   - Once the user is created (or selected), navigate to the **Security credentials** tab.
   - Scroll down to the **Access keys** section and click **Create access key**.
   - Note the **Access Key ID** and **Secret Access Key**. These credentials will only be shown once, so save them securely.
     - You can download the key pair as a `.csv` file for safekeeping.

---

## Security Best Practices
- **Do not share your keys publicly**: Avoid committing them to repositories or sharing them in insecure channels.
- **Use environment variables or credential files**: Store credentials securely in `.env` files or AWS credential files.
- **Rotate keys regularly**: Delete and regenerate access keys periodically for better security.
- **Use IAM roles when possible**: Prefer IAM roles over access keys for secure access in AWS environments.

---

## References
- [AWS IAM Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
