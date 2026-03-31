## Project Description: Intelligent Campus Learning Resource Organization and Sharing Platform

### I. Project Rationale
As digital campus initiatives advance, university students accumulate vast amounts of fragmented learning materials, including courseware, exercises, and literature notes. Students often face low retrieval efficiency and difficulties in sharing high-quality resources. Current storage methods (local folders, standard cloud drives) lack intelligent classification and collaborative features, failing to meet the demands of efficient resource management in a campus setting.

**Why Python?** Python’s ecosystem is perfectly suited for this project:
* **Technical Fit:** Excellent for multi-format parsing and lightweight semantic analysis.
* **Web Efficiency:** Django shortens development cycles and is ideal for campus intranet deployment.
* **Rich Ecosystem:** Access to proven open-source tools for storage and retrieval.
* **Integration:** Seamlessly connects file processing, algorithms, and interactive features, providing the optimal balance between development cost and functional depth.

### II. Complexity and Workload
#### (A) Complexity
1.  **Technical Level:** Implementing "Intelligent Organization" requires multi-disciplinary integration of data mining and Web development. Key tasks include format recognition, designing auto-classification algorithms based on keywords/semantics, and managing complex user permissions (departmental/grade-based sharing).
2.  **Requirement Level:** Must balance "intelligence" with "usability." The project requires accurate classification algorithms paired with a clean UI, ensuring the technical implementation aligns with actual student needs.

#### (B) Workload
1.  **Preparation (2 Weeks):** Researching campus course systems and common material types (lab reports, design guides, etc.) to create a *Campus Academic Resource Classification List*.
2.  **Core Development (8 Weeks):**
    * **Phase 1 (Data Layer):** Design MySQL database (6 core tables: Users, Materials, Tags, Sharing, Favorites, etc.). Develop the upload module with support for PDF/Word, chunked uploading (for large files), and version management.
    * **Phase 2 (Algorithm Layer):** Build text extraction tools using `PyPDF2` and `python-docx`. Implement auto-classification using **TF-IDF and Cosine Similarity**. Train the model on 600+ campus samples to achieve 60%+ accuracy.
    * **Phase 3 (Application Layer):** Build a 5-page frontend (Home, Profile, Upload, Category, Details). Develop 15+ Django APIs for authentication, file operations, and security.
3.  **Testing & Optimization (2 Weeks):** Functional testing (10+ cases) and performance testing for retrieval speed and accuracy.
4.  **Documentation (3 Weeks):** Writing the thesis (approx. 15,000 words), user manual, and deployment guides.

### III. Theoretical and Practical Value
* **Theoretical:** Validates the effectiveness of lightweight semantic classification in small-sample learning environments, providing a reference for similar resource management platforms.
* **Practical:** Enables "one-click upload, smart sorting, and precise search" for students. It facilitates cross-major resource flow, assists teachers in distributing materials, and creates a "Teaching-Learning-Sharing" closed loop.

### IV. Main Content
1.  **Material Parsing:** Extracting text and metadata from PDF/Word files.
2.  **Auto-Classification:**
    * **Three-Tier Tagging:** Subject (e.g., CS) → Course (e.g., OS) → Type (e.g., Notes).
    * **Feature Extraction:** Clean text and use TF-IDF to identify the top 20 weighted keywords as the "feature vector."
    * **Vector Matching:** Use **Cosine Similarity** to match the file vector against the "Predefined Tag Vector Library."
    * **Thresholding:** Files exceeding the similarity threshold are auto-filed; others are marked "Pending" for manual user input to improve future training.
3.  **Duplicate Detection:** Using file hashes to prevent redundant storage.
4.  **Resource Sharing:** Supporting "Public," "Private," or "Targeted" (specific class) sharing with comments and favorites.
5.  **Search & Retrieval:** Multi-dimensional filtering by keyword, tag, or upload time.

### V. Implementation Path
* **Technical Route:** Decoupled Frontend/Backend architecture. Frontend (HTML/CSS/JS), Backend (Django), Database (MySQL), AI Layer (Scikit-learn).
* **Tools:** PyCharm/VS Code, Git (Version Control), Postman (API Testing).
* **Management:** Iterative development with bi-weekly milestones.

### VI. Expected Deliverables
1.  **Core:** A fully functional platform with source code, database scripts, and deployment manuals.
2.  **Documentation:** A 15,000-word graduation thesis and a 20-slide presentation PPT.
3.  **Demonstration:** A 5-8 minute demo video and a live test environment.



