# CloudVault — Cloud-Based File Storage Using AWS

A mini-project web application built with Flask and Amazon S3. It supports uploading, listing, downloading files using short-lived presigned URLs, and deleting files in a private S3 bucket.

## Project Overview

CloudVault is an AWS cloud-based file storage and management system developed using Python Flask and Amazon Web Services.

The application allows users to upload, view, download, and delete files through a web-based interface. Amazon S3 is used to store files securely, while Boto3 connects the Flask application with AWS services.

The project demonstrates cloud computing, object storage, web application development, and basic cloud security.

## Requirements

- Python 3.10+
- An AWS account and an S3 bucket
- AWS credentials configured locally, or an IAM role on an AWS-hosted machine

## 1. Create an S3 Bucket

1. Open the AWS Console and navigate to Amazon S3.
2. Create a bucket in your preferred region.
3. Use a globally unique bucket name.
4. Keep **Block Public Access enabled**.
5. Keep default encryption enabled.

The application also requests AES-256 server-side encryption for uploaded objects.

## 2. Configure AWS Credentials

For local development, install AWS CLI and run:

```bash
aws configure
```

Enter your IAM access key, secret key, and region.

Use an IAM user or role with only the required permissions. Never commit credentials or your `.env` file to GitHub.

For EC2 deployment, prefer an attached IAM role instead of access keys.

Required permissions:

- `s3:ListBucket` on the bucket ARN
- `s3:PutObject`, `s3:GetObject`, and `s3:DeleteObject` on the bucket's object ARN

Example resource patterns:

- Bucket: `arn:aws:s3:::YOUR_BUCKET_NAME`
- Objects: `arn:aws:s3:::YOUR_BUCKET_NAME/*`

## 3. Install and Configure

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and configure your bucket name and AWS region.

Example:

```env
AWS_REGION=eu-north-1
S3_BUCKET=cloudvault-tessa
MAX_FILE_MB=20
FLASK_SECRET_KEY=your-generated-secret
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

You can also run the virtual environment's Python directly without activation:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 4. Run Locally

```powershell
python app.py
```

Open the application:

```text
http://127.0.0.1:5000
```

Check the health endpoint:

```text
http://127.0.0.1:5000/health
```

## 5. Demo Checklist

1. Upload a PDF or image.
2. Confirm it appears in the dashboard.
3. Download the uploaded file using the temporary presigned URL.
4. Delete a test file.
5. Open the S3 bucket in AWS Console and verify the uploaded objects.
6. Try a blocked file extension and confirm that the application rejects it.

## System Architecture

The following diagram illustrates the architecture of CloudVault and the interaction between the user interface, Flask backend, AWS services, and Amazon S3 storage.

<p align="center">
  <img src="CloudVault%20System%20Architecture.png" alt="CloudVault System Architecture" width="800">
</p>

<p align="center">
  <b>Figure: System Architecture of CloudVault</b>
</p>

## Project Features

- Upload files to Amazon S3 cloud storage.
- View and list stored files.
- Download uploaded files using temporary presigned URLs.
- Delete unwanted files from cloud storage.
- Simple and user-friendly web dashboard.
- AWS integration using Boto3.
- IAM-based permissions for AWS operations.
- S3 Block Public Access configuration.
- Server-side encryption using SSE-S3.
- Environment-based configuration management.
- File type validation and 20 MB upload limit.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML | Frontend structure |
| CSS | Frontend styling |
| Amazon Web Services | Cloud platform |
| Amazon S3 | Cloud file storage |
| Boto3 | AWS integration |
| AWS IAM | Access management |
| AWS CLI | AWS configuration |
| Visual Studio Code | Development environment |

## Important Limitations and Security

- This mini-project does not implement user accounts or per-user permissions. Anyone who can access the application may be able to operate on the configured bucket. Do not expose it publicly as-is.
- Use a private S3 bucket. Do not add public read/write bucket policies.
- Download URLs are valid for five minutes. Anyone holding a generated URL can use it until it expires.
- The 20 MB upload limit is an application-level limit.
- `debug=True` is intended for local development only.
- For deployment, use a production WSGI server, HTTPS, a reverse proxy, and appropriate network and security controls.
- AWS may charge for storage, requests, and compute. Check current pricing and set a budget alert.
- Validate and test the application in your own AWS account. Credentials, account permissions, and region configuration affect results.

## Author

Developed as a Cloud Computing Mini Project using Flask and Amazon Web Services.
