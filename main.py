import requests
import fitz  # PyMuPDF
from PIL import Image
import os

def download_arxiv_pdf(arxiv_id, download_path="arxiv_paper.pdf"):
    # arXiv URL format for PDFs
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    response = requests.get(url)
    if response.status_code == 200:
        with open(download_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {arxiv_id} to {download_path}")
        return download_path
    else:
        print(f"Failed to download PDF: Status code {response.status_code}")
        return None

def create_cropped_thumbnail(pdf_path, thumbnail_path, zoom=2.0, width=400, height=300, crop_ratio=0.5):
    # Open the PDF file
    with fitz.open(pdf_path) as pdf:
        # Select the first page
        page = pdf[0]
        # Set zoom factor for higher resolution
        mat = fitz.Matrix(zoom, zoom)
        # Render page to an image (Pixmap) at the specified zoom level
        pix = page.get_pixmap(matrix=mat)
        # Convert Pixmap to PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Crop the top part of the image, based on crop_ratio
        cropped_height = int(pix.height * crop_ratio)
        image = image.crop((0, 0, pix.width, cropped_height))

        # Resize to the specified thumbnail dimensions
        image = image.resize((width, height), Image.LANCZOS)
        # Save the thumbnail
        image.save(thumbnail_path, "JPEG", quality=85)  # Quality parameter improves JPEG resolution
        print(f"Cropped thumbnail saved to {thumbnail_path}")

# Example Usage
arxiv_id = "2301.00001"  # Replace with the actual arXiv ID you want
pdf_path = download_arxiv_pdf(arxiv_id)
if pdf_path:
    create_cropped_thumbnail(pdf_path, "cropped_thumbnail.jpg")

    # Optionally delete the downloaded PDF to save space
    os.remove(pdf_path)
