import pandas as pd
from io import BytesIO

class ExcelProcessor:

    def read_excel(self, content: bytes) -> pd.DataFrame:
        df = pd.read_excel(BytesIO(content), header=None)

        print("📊 Buscando header real...")

        header_row_index = self.find_header_row(df)

        print(f"✅ Header encontrado en fila: {header_row_index}")

        # 🔥 Re-crear DataFrame usando esa fila como header
        df.columns = df.iloc[header_row_index]
        df = df[header_row_index + 1:].reset_index(drop=True)
        df = self.trim_table(df)
        print(df.head(10).to_string())
        return df
    
    def find_header_row(self, df: pd.DataFrame) -> int:
        keywords = ["NO", "FACTURA", "FRAC", "DESCRIP"]

        for i, row in df.iterrows():
            row_values = [str(cell).upper() for cell in row.values]

            if all(any(keyword in cell for cell in row_values) for keyword in keywords):
                return i

        raise Exception("❌ No se encontró el header de la tabla")
    
    def trim_table(self, df):
        empty_streak = 0
        max_empty_allowed = 3

        last_valid_index = 0

        for i, row in df.iterrows():

            non_null_count = row.count()

            if non_null_count >= 2:
                empty_streak = 0
                last_valid_index = i  # 🔥 guardas última fila válida
            else:
                empty_streak += 1

            if empty_streak >= max_empty_allowed:
                break

        print(f"✂️ Tabla recortada hasta fila válida: {last_valid_index}")

        return df.iloc[:last_valid_index + 1].reset_index(drop=True)