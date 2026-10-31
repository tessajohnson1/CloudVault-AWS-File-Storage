import os
import uuid
from datetime import datetime, timezone
from functools import wraps

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-development-secret")

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
S3_BUCKET = os.getenv("S3_BUCKET", "")
MAX_FILE_MB = int(os.getenv("MAX_FILE_MB", "20"))
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "ppt", "pptx", "txt", "csv",
    "png", "jpg", "jpeg", "gif", "zip", "xlsx"
}

s3 = boto3.client("s3", region_name=AWS_REGION) if S3_BUCKET else None


def format_size(size):
    size = float(size)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.1f} TB"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def aws_ready():
    if not S3_BUCKET:
        flash("AWS is not configured yet. Set S3_BUCKET and AWS_REGION in your .env file.", "warning")
        return False
    return True


@app.route("/")
def index():
    files = []
    total_bytes = 0
    error = None

    if S3_BUCKET and s3:
        try:
            paginator = s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=S3_BUCKET):
                for obj in page.get("Contents", []):
                    total_bytes += obj["Size"]
                    files.append({
                        "key": obj["Key"],
                        "name": obj["Key"].split("/", 1)[-1],
                        "size": format_size(obj["Size"]),
                        "last_modified": obj["LastModified"].strftime("%d %b %Y, %H:%M"),
                        "bytes": obj["Size"],
                    })
            files.sort(key=lambda item: item["last_modified"], reverse=True)
        except (ClientError, NoCredentialsError) as exc:
            error = str(exc)
    else:
        error = "AWS setup incomplete. Follow README.md to configure your S3 bucket."

    return render_template(
        "index.html",
        files=files,
        total_files=len(files),
        total_size=format_size(total_bytes),
        error=error,
        bucket=S3_BUCKET,
        region=AWS_REGION,
        max_file_mb=MAX_FILE_MB,
    )


@app.post("/upload")
def upload():
    if not aws_ready():
        return redirect(url_for("index"))

    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename:
        flash("Choose a file before uploading.", "danger")
        return redirect(url_for("index"))

    safe_name = secure_filename(uploaded.filename)
    if not safe_name or not allowed_file(safe_name):
        flash("This file type is not allowed. Check the supported types shown below.", "danger")
        return redirect(url_for("index"))

    data = uploaded.read(MAX_FILE_BYTES + 1)
    if not data:
        flash("The selected file is empty.", "danger")
        return redirect(url_for("index"))
    if len(data) > MAX_FILE_BYTES:
        flash(f"File is larger than the {MAX_FILE_MB} MB limit.", "danger")
        return redirect(url_for("index"))

    key = f"uploads/{uuid.uuid4().hex}_{safe_name}"
    try:
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=data,
            ContentType=uploaded.mimetype or "application/octet-stream",
            ServerSideEncryption="AES256",
        )
        flash(f"Upload successful: {safe_name}", "success")
    except (ClientError, NoCredentialsError) as exc:
        flash(f"Upload failed: {exc}", "danger")

    return redirect(url_for("index"))


@app.get("/download/<path:key>")
def download(key):
    if not aws_ready():
        return redirect(url_for("index"))
    try:
        # URL is short-lived; the S3 object remains private.
        link = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": key},
            ExpiresIn=300,
        )
        return redirect(link)
    except (ClientError, NoCredentialsError) as exc:
        flash(f"Could not create download link: {exc}", "danger")
        return redirect(url_for("index"))


@app.post("/delete/<path:key>")
def delete(key):
    if not aws_ready():
        return redirect(url_for("index"))
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=key)
        flash("File deleted from S3.", "success")
    except (ClientError, NoCredentialsError) as exc:
        flash(f"Delete failed: {exc}", "danger")
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok", "application": "CloudVault"}


if __name__ == "__main__":
    # Development only. For deployment, use a production WSGI server and HTTPS.
    app.run(debug=True)
