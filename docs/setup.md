### Revised Environment Setup

**Operating System:** Windows
**Package Manager:** Anaconda / Laragon

**1. Create Environment:**
```bash
conda create -n campus_env python=3.11
conda activate campus_env
```

**2. Local Server Setup:**
Download and install [Laragon](https://laragon.org/download) to manage your MySQL database and local server environment.

**3. Install Project Stack:**
```bash
# Core Framework & Database
pip install django mysqlclient

# File Processing
pip install pypdf2 python-docx

# Machine Learning & Data Analysis
pip install scikit-learn pandas

# Utilities (For Frontend-Backend Communication)
pip install django-cors-headers
```