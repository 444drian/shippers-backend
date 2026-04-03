import pandas as pd

class HojaTrabajoProcessor:

    def process(self, df):

        partidas_rows, total_row = self.split_rows(df)

        partidas = []

        for row in partidas_rows:
            valor_pesos = 0

            partida = {
                "num_partida": self._to_int(row.get("No.")),
                "fraccion": self._format_fraccion(row.get("FRACCIÓN")),
                "origen": row.get("ORIGEN"),
                "descripcion": str(row.get("DESCRIPCIÓN")).replace("\n", " "),
                "cantidad": self._to_float(row.get("CANTIDAD")),
                "peso": self._to_float(row.get("PESO")),
                "valor_pesos": valor_pesos,
                "valor_dolares": self._to_float(row.get("VALOR TOTAL")),
            }

            partidas.append(partida)

        # 🔥 Totales desde fila especial
        peso_bruto = self._to_float(total_row.get("PESO")) if total_row is not None else 0
        valor_dolares = self._to_float(total_row.get("VALOR TOTAL")) if total_row is not None else 0

        valor_calculado = sum(p["valor_dolares"] for p in partidas if p["valor_dolares"] is not None)
        num_partidas = len(partidas)

        # 🔥 Aquí necesitas extraer esto del header (luego lo refinamos)
        nume_ped = "BESSER"
        tipo_cambio = 0

        return {
            "pedimentos": [
                {
                    "nume_ped": nume_ped,
                    "contenido": [
                        {
                            "tipo_cambio": tipo_cambio,
                            "peso_bruto": peso_bruto,
                            "valor_dolares": valor_dolares,
                            "valor_calculado": valor_calculado,
                            "num_partidas": num_partidas,
                            "partidas": partidas
                        }
                    ]
                }
            ]
        }
    
    def _to_int(self, value):
        try:
            return int(value)
        except:
            return None
        
    def _format_fraccion(self, value):
        if not value:
            return None

        # convertir a string y quitar espacios
        value = str(value).strip()

        # eliminar puntos
        value = value.replace(".", "")

        # tomar primeros 6 caracteres
        return value[:6]    
   
    def _to_float(self, value):
        try:
            return float(value)
        except:
            return 0
    
    def split_rows(self, df):
        partidas = []
        total_row = None

        for _, row in df.iterrows():

            no = row.get("No.")
            fraccion = row.get("FRACCIÓN")

            if pd.notna(no) and pd.notna(fraccion):
                partidas.append(row)

            elif pd.isna(no) and (
                pd.notna(row.get("PESO")) or pd.notna(row.get("VALOR TOTAL"))
            ):
                total_row = row

        return partidas, total_row