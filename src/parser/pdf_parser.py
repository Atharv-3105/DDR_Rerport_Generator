import fitz 
import os 


class PDFParser:
    def __init__(self, pdf_path, output_dir):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        
    def parse(self):
        doc = fitz.open(self.pdf_path)
        os.makedirs(self.output_dir, exist_ok=True)
        
        parsed_data = {
            "file_name": os.path.basename(self.pdf_path),
            "pages": []
        }
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            #Get the text of the page
            text = page.get_text().strip()
            #Get the images in the page
            images = self._extract_images(doc, page, page_num)
            
            parsed_data["pages"].append({
                "page_number": page_num + 1,
                "text": text,
                "images": images
            })
            
        
        return parsed_data
    

    def _extract_images(self, doc, page, page_num):
        image_paths = []
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            image_filename = f"page_{page_num+1}_img_{img_index}.png"
            image_path = os.path.join(self.output_dir, image_filename)
            
            with open(image_path, "wb") as f:
                f.write(image_bytes)
                
                
            image_paths.append(image_path)
            
        return image_paths