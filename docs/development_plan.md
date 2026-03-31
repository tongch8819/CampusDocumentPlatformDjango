### **Phase 1: Foundation and Data Layer (Weeks 1-2)**
*The goal here is to establish the backbone of the application before introducing any complex logic.*

1. **Project Initialization:**
   * Fire up VS Code, ensure your Python interpreter is set to `campus_env`, and initialize the Django project.
   * Set up the core Django apps (e.g., `users`, `resources`, `api`).
   * Configure `settings.py` to connect to your Laragon MySQL instance and set up `django-cors-headers` for future frontend communication.
2. **Database Modeling:**
   * Translate the 6 core tables into Django Models: `Users` (extending Django's AbstractUser), `Materials`, `Tags`, `Sharing`, and `Favorites`.
   * Define the relationships (One-to-Many for uploads, Many-to-Many for tags and favorites).
   * Run initial migrations and register models to the Django Admin panel to easily inspect data during development.
3. **Basic Authentication API:**
   * Create endpoints for user registration, login, and session/token management.

### **Phase 2: File Handling and Parsing (Weeks 3-4)**
*Getting the raw data into the system and extracting its contents.*

1. **Upload Module:**
   * Build the API to handle file uploads, including the chunked upload logic for larger files.
   * Implement the file hash check (e.g., SHA-256) upon upload to prevent duplicate storage in the local system.
2. **Text Extraction Pipeline:**
   * Create a utility script utilizing `PyPDF2` and `python-docx`.
   * Write functions that take an uploaded file, determine its MIME type, and extract the raw text and metadata.
   * Save the extracted text into the database alongside the file reference for the upcoming ML phase.

### **Phase 3: The Intelligence Layer (Weeks 5-6)**
*This is the core algorithmic work. We will isolate this from the web logic to make testing easier.*

1. **Data Preparation:**
   * Gather the 600+ campus samples and format them for training.
   * Establish the "Predefined Tag Vector Library" based on your Subject → Course → Type hierarchy.
2. **NLP & Feature Extraction:**
   * Write text-cleaning utilities (removing stop words, standardizing formats).
   * Implement `scikit-learn`'s `TfidfVectorizer` to extract the top 20 weighted keywords from the cleaned text.
3. **Classification Engine:**
   * Build the Cosine Similarity matching logic.
   * Implement the threshold logic: if the similarity score is > X, automatically link the tag IDs to the material. If < X, flag the `status` as "Pending" for manual user review.

### **Phase 4: Advanced APIs and Business Logic (Weeks 7-8)**
*Connecting the intelligence layer to the user experience.*

1. **Search and Retrieval:**
   * Build the search API endpoint allowing multi-dimensional filtering (e.g., querying by a combination of keywords, specific tags, and upload date).
2. **Sharing & Permissions:**
   * Implement the logic for "Public", "Private", and "Targeted" sharing. Ensure the retrieval APIs respect these permission flags before returning results.
3. **Interactive Features:**
   * Build endpoints for users to favorite materials, leave comments, and manually update tags for "Pending" files (which will feed back into your dataset).

### **Phase 5: Frontend Integration & Testing (Weeks 9-10)**
*Bringing the UI to life and ensuring platform stability.*

1. **Frontend Construction:**
   * Build out the 5 core pages (Home, Profile, Upload, Category, Details) using HTML/CSS/JS.
   * Hook up the frontend to the Django APIs, ensuring cross-origin requests work smoothly.
2. **System Testing:**
   * Write Django test cases for the 15+ APIs.
   * Perform performance testing on the retrieval speed and validate that the classification accuracy meets the 60%+ target. 

### **Phase 6: Documentation and Finalization (Weeks 11-12)**
* When it comes time to draft the 15,000-word thesis and format your algorithm metrics, your usual LaTeX setup will make light work of generating a professional, camera-ready document.
* Finalize the user manual, deployment guides, and record the 5-8 minute demo video.

