import pdfplumber
from io import BytesIO


class PDFProcessor:

    def extract_text(self, file_bytes: bytes) -> str:
        text = ""

        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            print("📄 Total de páginas:", len(pdf.pages))

            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    def normalize_text(self, raw_text: str) -> list[str]:
        """
        Limpia el texto y lo convierte en líneas numeradas
        """

        lines = raw_text.split("\n")

        normalized_lines = []

        for line in lines:
            clean_line = line.strip()

            # 🔥 quitar líneas vacías
            if not clean_line:
                continue

            # 🔥 colapsar espacios múltiples
            clean_line = " ".join(clean_line.split())

            normalized_lines.append(clean_line)

        # 🔥 numerar
        numbered_lines = [
            f"{i+1} | {line}"
            for i, line in enumerate(normalized_lines)
        ]

        print("\n📑 Líneas normalizadas:", len(numbered_lines))
        print("🔎 Preview líneas:")
        for l in numbered_lines:
            print(l)

        return numbered_lines
    


    # {
    #     "pedimentos": [
    #         {
    #             "nume_ped": "string",
    #             "contenido": [
    #                 {
    #                     "tipo_cambio": "float",
    #                     "peso_bruto": "float",
    #                     "valor_dolares": "float",
    #                     "valor_calculaodo": "float",
    #                     "num_partidas": "int",
    #                     "partidas": [
    #                         {
    #                             "num_partida": "int",
    #                             "fraccion": "string",
    #                             "origen": "string",
    #                             "descripcion": "string",
    #                             "cantidad": "float",
    #                             "peso": "float",
    #                             "valor_pesos": "float",
    #                             "valor_dolares": "float"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }