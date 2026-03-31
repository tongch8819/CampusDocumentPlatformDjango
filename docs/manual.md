# Intelligent Campus Learning Resource Platform
## Part I: Deployment Guide (Administrator Manual)

This section outlines the steps required to deploy the platform in a local development environment for testing and evaluation.

### 1. Prerequisites
Ensure the following software is installed on the host machine:
* **Operating System:** Windows 10/11
* **Python Environment:** Anaconda or Miniconda
* **Database Engine:** Laragon (Recommended) or standalone MySQL Server
* **Code Editor:** Visual Studio Code (with the "Live Server" extension installed)

### 2. Database Setup (Laragon)
1. Launch **Laragon** and click **Start All** to initialize the MySQL server.
2. Open the Laragon terminal or your preferred database GUI (e.g., HeidiSQL, DBeaver).
3. Create a new, empty database named `campus_db`:
   ```sql
   CREATE DATABASE campus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 3. Backend Environment Configuration
1. Open an Anaconda Prompt and create a dedicated Python 3.11 environment:
   ```bash
   conda create -n campus_env python=3.11
   conda activate campus_env
   ```
2. Navigate to the backend directory of the project (where `manage.py` is located).
3. Install the required dependencies:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-cors-headers mysqlclient PyMuPDF python-docx scikit-learn pandas
   ```

### 4. Database Migration & Initialization
1. Apply the database schemas to your MySQL instance:
   ```bash
   python manage.py makemigrations users resources
   python manage.py migrate
   ```
2. Create an administrative superuser account:
   ```bash
   python manage.py createsuperuser
   ```
   *(Follow the prompts to set a username and password. You will use this to log into the frontend.)*

### 5. Launching the System
1. **Start the Django Backend:** In your Anaconda terminal, ensure you are in the directory with `manage.py` and run:
   ```bash
   python manage.py runserver
   ```
   *The backend API will now be listening on `http://127.0.0.1:8000`.*
2. **Start the Frontend UI:**
   Open the `frontend` folder in Visual Studio Code. Right-click on `index.html` and select **"Open with Live Server"**.
   *The frontend will launch in your default web browser.*

***

## Part II: User Manual (Student & Faculty Guide)

Welcome to the Intelligent Campus Learning Resource Platform. This guide explains how to navigate and utilize the system's core features.

### 1. Account Access
* Navigate to the platform's landing page.
* Enter your assigned university credentials (Username and Password).
* Upon successful authentication, you will be redirected to the main **Browse** dashboard.

### 2. Browsing and Searching Resources
The **Browse** page displays all public materials and targeted materials shared with your department.
* **Smart Search:** Use the search bar at the top of the screen to find specific documents. The search engine queries both the document's title and the AI-extracted internal text.
* **Quick Actions:** Click the **Heart Icon (♡)** on any card to instantly save a document to your personal favorites.

### 3. Uploading and Auto-Classification
Contribute to the campus repository using the **Upload** page.
1. Click **Upload** in the top navigation bar.
2. Provide a descriptive title for your document.
3. Select a `.pdf`, `.doc`, or `.docx` file from your computer.
4. Click **Upload and Process**.
5. **AI Processing:** The system will automatically extract the text and run a semantic analysis using TF-IDF and Cosine Similarity. It will assign appropriate course tags and auto-file the document. *Note: If a file with an identical hash already exists in the system, the upload will be blocked to prevent duplicates.*

### 4. Viewing Document Details
Click **View Details** on any resource card to access the dedicated document page.
* **Extracted Text Preview:** Read the core content of the document directly in the browser without needing to download it.
* **Download:** Click "Open Original File" to view or download the raw PDF/Word document.
* **Toggle Favorite:** Save or remove the document from your personal dashboard.

### 5. Managing Your Uploads (Owner Controls)
If you are the original uploader of a document, the Details page will display a blue **Owner Settings** panel.
* **Update Visibility:** By default, new uploads are **Private**. You can change the permission to **Public** (visible to all students) or **Targeted** (visible only to your department).
* **Delete Document:** Click the red "Delete Document" button to permanently remove the file from the server and database.

### 6. Your Personal Dashboard
Click **My Profile** in the navigation bar to access your personal hub.
* **My Uploads Tab:** Review, manage, and update permissions for all files you have contributed to the platform.
* **My Saved Materials Tab:** Quickly access all documents you have favorited for your current study sessions.
