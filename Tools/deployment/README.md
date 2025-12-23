# Universal FTP Deployer

## 🤖 AI Identity
**Purpose**: Destructive FTP deployment (Mirroring).
**Language**: Python 3.
**Key File**: `deploy.py`.
**Configuration**: `config.json` (Required).

## 📄 Configuration Schema (`config.json`)
Create a file named `config.json` in this directory.

```json
{
  "host": "ftp.example.com",     // [Required] FTP Hostname
  "user": "user@example.com",    // [Required] FTP Username
  "password": "secret_password", // [Required] FTP Password
  "preserve": [                  // [Optional] Remote paths to NEVER delete
    ".well-known",
    "users",
    "uploads",
    "public_html/images" 
  ],
  "skip_upload": [               // [Optional] Local paths to NEVER upload
    ".git",
    "node_modules",
    "__pycache__",
    "*.log"
  ]
}
```

## ⚠️ Critical Safety Validation
Before running:
1. **Check `preserve` list**: Ensure `users/` and `uploads/` are included to prevent data loss.
2. **Check `host`**: Confirm you are deploying to the correct environment (Staging vs Prod).
3. **Destructive Action**: This script performs `rm -rf` on remote files that do not exist locally (unless preserved).

## 🚀 Execution
```bash
python3 python/deployment/deploy.py
```
*Script automatically detects project root relative to its own location.*
