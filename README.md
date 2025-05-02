# Llama 3.2 Vision OCR


<img width="1375" alt="Screenshot 2025-04-02 at 18 09 24" src="https://github.com/user-attachments/assets/6b90bcd6-4f4c-4afe-9940-038141c47b76" />

## Features

- Extract structured text from images using Vision Models
- Support for multiple Llama 3.2 vision models:
  - llama-3.2-11b-vision-preview
  - llama-3.2-90b-vision-preview
- Advanced handwriting recognition capabilities
<img width="1362" alt="Screenshot 2025-04-02 at 18 18 16" src="https://github.com/user-attachments/assets/9a86be37-8682-4b30-86ce-de8a917ddcce" />
- Responsive UI with image preview
- Results displayed in Markdown format
  



## Requirements

- Python 3.7+
- Streamlit
- Pillow
- Requests
- A valid Groq API key


## How It Works
The application uses the Groq API to access Meta's Llama 3.2 vision models. When you upload an image, the application:

1. Converts the image to a base64-encoded string
2. Sends the image to the Groq API along with a prompt for text extraction
3. Processes the API response
4. Displays the extracted text in a formatted Markdown layout

---
