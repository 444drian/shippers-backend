# app/services/ocr/ocr_service.py

from pdf2image import convert_from_bytes
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRService:

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        print("Iniciando extracción OCR...")
        images = convert_from_bytes(
            pdf_bytes,
            poppler_path=r"C:\poppler-25.12.0\Library\bin"
        )
        print(f"PDF convertido a {len(images)} imagen(es) para OCR.")

        full_text = []

        for img in images:
            print("Procesando nueva página...")

            open_cv_image = self.pil_to_cv(img)

            # 🔥 RECORTE AQUÍ
            h, w = open_cv_image.shape[:2]
            open_cv_image = open_cv_image[int(h*0.15):h, 0:w]

            processed = self.preprocess_image(open_cv_image)

            cv2.imwrite("debug_original.png", open_cv_image)
            cv2.imwrite("debug_processed.png", processed)

            print("Ejecutando OCR...")
            text = pytesseract.image_to_string(
                processed,
                config="--psm 6"
            )

            print("OCR OK")

            full_text.append(text)
        
        # print("Extracción OCR completada.")
        # print(f"Texto completo extraído:\n{full_text}\n{'='*50}")

        return "\n".join(full_text)

    def pil_to_cv(self, pil_image):
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def preprocess_image(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 🔥 1. Quitar ruido con blur suave
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # 🔥 2. Binarización adaptativa (clave)
        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            15,
            10
        )

        # 🔥 3. Invertir (Tesseract funciona mejor así en muchos casos)
        thresh = cv2.bitwise_not(thresh)

        # 🔥 4. Eliminar líneas horizontales
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel)

        # 🔥 5. Eliminar líneas verticales
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)

        # 🔥 6. Restar líneas
        no_lines = cv2.subtract(thresh, remove_horizontal)
        no_lines = cv2.subtract(no_lines, remove_vertical)

        # 🔥 7. Escalar imagen (MUY importante)
        resized = cv2.resize(no_lines, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        return resized