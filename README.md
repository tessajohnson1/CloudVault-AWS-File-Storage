# CloudVault — Cloud-Based File Storage Using AWS

A mini-project web app built with Flask and Amazon S3. It supports uploading, listing, downloading with short-lived presigned URLs, and deleting files in a private S3 bucket.

## Project Overview

CloudVault is an AWS cloud-based file storage and management
system developed using Python Flask and Amazon Web Services.

The application allows users to upload, view, download, and
delete files through a web-based interface. Amazon S3 is used
to store files securely, while Boto3 connects the Flask
application with AWS services.

The project demonstrates cloud computing, object storage,
web application development, and basic cloud security.

## Requirements
- Python 3.10+
- An AWS account and an S3 bucket
- AWS credentials configured locally, or an IAM role on an AWS-hosted machine

## 1. Create an S3 bucket
1. Open the AWS Console and navigate to Amazon S3.
2. Create a bucket in your preferred region (default in this project: `ap-south-1`).
3. Use a globally unique bucket name.
4. Keep **Block Public Access enabled** and do not enable public website access.
5. Keep default encryption enabled. The app also requests AES256 server-side encryption for uploaded objects.

## 2. Configure AWS credentials
For local development, install AWS CLI and run:
```bash
aws configure
```
Enter your IAM access key, secret key, and region. Use an IAM user/role with only the required permissions. Never commit credentials or `.env` to GitHub. For EC2 deployment, prefer an attached IAM role instead of access keys.

The role/user needs permissions scoped to your bucket for:
- `s3:ListBucket` on the bucket ARN
- `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject` on the bucket's object ARN

Example resource pattern:
- Bucket: `arn:aws:s3:::YOUR_BUCKET_NAME`
- Objects: `arn:aws:s3:::YOUR_BUCKET_NAME/*`

## 3. Install and configure
Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and set `S3_BUCKET` to your exact bucket name and `AWS_REGION` to the bucket's region.

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```
You can also run the virtual environment's Python directly without activation:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 4. Run locally
```powershell
python app.py
```
Open `http://127.0.0.1:5000`.

Check `http://127.0.0.1:5000/health` for the health endpoint.

## 5. Demo checklist
1. Upload a PDF or image.
2. Confirm it appears in the dashboard.
3. Download it; a temporary presigned URL should be generated.
4. Delete a test file.
5. Open the S3 bucket in AWS Console and show the uploaded objects.
6. Try a blocked file extension and confirm the app rejects it.

## Important limitations
- This mini-project version does not implement user accounts or per-user permissions. Anyone who can access the app can operate on the bucket. Do not expose it publicly as-is.
- Use a private bucket. Do not add public read/write bucket policies.
- The download URL is valid for five minutes; anyone holding it can use it until expiry.
- The 20 MB upload limit is an application-level limit.
- `debug=True` is for local development only. For deployment, use a production WSGI server such as Gunicorn, HTTPS, a reverse proxy, and appropriate network/security controls.
- AWS may charge for storage, requests, and compute. Check current pricing and set a budget alert. Delete resources when finished.
- Validate and test in your own AWS account; credentials, account permissions, and region configuration affect results.

## System Architecture

The following diagram illustrates the architecture of CloudVault and the interaction between the user interface, Flask backend, AWS services, and Amazon S3 storage.

<p align="center">
  <img src="images/architecture.png" alt="CloudVault System Architecture" width="800">
</p>

<p align="center">
  <b>Figure: System Architecture of CloudVault</b>
</p>

## Project features
- Upload files to Amazon S3 cloud storage.
- View and list stored files.
- Download uploaded files.
- Delete unwanted files from cloud storage.
- Simple and user-friendly web dashboard.
- AWS integration using Boto3.
- IAM-based permissions for AWS operations.
- S3 Block Public Access configuration.
- Server-side encryption using SSE-S3.
- Environment-based configuration management.

## Technologies used
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
