import hashlib
import docx
import fitz  # PyMuPDF
import io

def generate_file_hash(file_bytes):
    """Generates a SHA-256 hash directly from raw bytes."""
    return hashlib.sha256(file_bytes).hexdigest()

def extract_text_from_file(file_bytes, filename):
    """Routes the raw bytes to the correct parser based on extension."""
    extracted_text = ""
    file_extension = filename.split('.')[-1].lower()

    try:
        if file_extension == 'pdf':
            # PyMuPDF reads the stream directly
            pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in pdf_doc:
                extracted_text += page.get_text() + "\n"
            pdf_doc.close()
        
        elif file_extension in ['doc', 'docx']:
            # docx needs the bytes wrapped in a standard IO stream
            byte_stream = io.BytesIO(file_bytes)
            doc = docx.Document(byte_stream)
            for para in doc.paragraphs:
                extracted_text += para.text + "\n"
                
        elif file_extension == 'txt':
            extracted_text = file_bytes.decode('utf-8', errors='ignore')
                
    except Exception as e:
        print(f"Error extracting text from {filename}: {e}")
        
    print("Content extracted from file:", extracted_text[:200])  # Print the first 200 characters for debugging
    return extracted_text.strip()

import os
def main():
    # Example usage
    material_path = os.path.join("..", "test")
    # material_path = os.path.join("..", "media", "materials", "2026", "03")
    with open(os.path.join(material_path, 'paper.pdf'), 'rb') as f:
        print("Extracted Text:", extract_text_from_file(f.read(), 'paper.pdf'))
        
if __name__ == "__main__":
    main()