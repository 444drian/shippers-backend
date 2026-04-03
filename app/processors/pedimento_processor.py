import re


class PedimentoProcessor:

    def process(self, lines: list[str]) -> dict:
        """
        Entrada: líneas normalizadas del PDF
        Salida: estructura parcial del pedimento
        """

        nume_ped = self._extract_nume_ped(lines)
        self.tipo_cambio = self._extract_tipo_cambio(lines)
        peso_bruto = self._extract_peso_bruto(lines)
        valor_dolares = self._extract_valor_dolares(lines)
        partidas = self._extract_partidas(lines)
        valor_calculado = self.calcular_valor_calculado(partidas)
        num_partidas = len(partidas)

        return {
            "pedimentos": [
                {
                    "nume_ped": nume_ped,
                    "contenido": [
                        {
                            "tipo_cambio": self.tipo_cambio,
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
    
    def parse_float(self, value: str) -> float | None:
        if not value:
            return None

        try:
            # 🔥 quitar comas (separadores de miles)
            clean = value.replace(",", "")
            return float(clean)
        except ValueError:
            return value
        
    def format_float(self, value: float | None) -> float | None:
        if value is None:
            return None
        return round(value, 2)

    def _buscar_linea_con(self, lines, palabra):
        for line in lines:
            if palabra in line:
                return line
        return ""

    def _extract_nume_ped(self, lines: list[str]) -> str:
        """
        Busca el número de pedimento en las líneas
        """
        line = self._buscar_linea_con(lines, "PEDIMENTO:")
        pattern = re.search(r"PEDIMENTO:.*(\b\d{7}\b)", line, re.IGNORECASE) 

        if pattern:
            value = pattern.group(1)
            print(f"✅ Pedimento encontrado: {value}")
            return value

        print("⚠️ No se encontró número de pedimento")
        return ""
    
    def _extract_tipo_cambio(self, lines: list[str]) -> float | None:
        """
        Busca el tipo de cambio en las líneas
        """
                
        line = self._buscar_linea_con(lines, "CAMBIO:")
        pattern = re.search(r"TIPO\s+CAMBIO:\s*(\d+(?:\.\d{4,5}))", line, re.IGNORECASE)
        if pattern:
            value = float(pattern.group(1))
            print(f"💱 Tipo de cambio encontrado: {value}")
            return value
        
        print("⚠️ No se encontró tipo de cambio")
        return None
    
    def _extract_peso_bruto(self, lines: list[str]) -> float | None:
        """
        Busca el peso bruto en las líneas
        """
        line = self._buscar_linea_con(lines, "PESO BRUTO:")
        pattern = re.search(r"PESO\s+BRUTO:\s*(\d+\,*\d*(?:\.\d{2,5}))", line, re.IGNORECASE)
        if pattern:
            value = self.parse_float(pattern.group(1))
            print(f"⚖️ Peso bruto encontrado: {value}")
            return value
        
        print("⚠️ No se encontró peso bruto")
        return None

    def _extract_valor_dolares(self, lines: list[str]) -> float | None:
        """
        Busca el valor en dólares en las líneas
        """
        line = self._buscar_linea_con(lines, "VALOR DOLARES:")
        pattern = re.search(r"VALOR\s+DOLARES:\s*(\d+\,*\d*(?:\.\d{2,5}))", line, re.IGNORECASE)
        if pattern:
            value = self.parse_float(pattern.group(1))
            print(f"💵 Valor en dólares encontrado: {value}")
            return value
        
        print("⚠️ No se encontró valor en dólares")
        return None

    def _extract_partidas(self, lines: list[str]) -> list[dict]:
        block = self._get_partidas_block(lines)


        partidas = [self._parse_partida(b) for b in block]

        #print(f"📦 Partidas extraídas: {partidas}")

        return partidas
    
    def _get_partidas_block(self, lines: list[str]) -> list[str]:
        # Extraer bloques de partidas
        pat_header = re.compile(r'\b\d{1,3}\s+\d{8}\b')

        bloques = []
        bloque_actual = []

        # Recorre las líneas y agrupa en bloques según el patrón de header
        for line in lines:
            if pat_header.search(line):          # ¿Empieza una nueva partida?
                if bloque_actual:                 # si había una abierta, guárdala
                    bloques.append(bloque_actual)
                bloque_actual = [line]           # abre un nuevo bloque
            else:
                if bloque_actual:                 # líneas internas de la partida actual
                    bloque_actual.append(line)

        # cierra el último bloque si existe
        if bloque_actual:
            bloques.append(bloque_actual)

        # Ejemplo de salida
        # print(f"Partidas encontradas: {len(bloques)}")
        # for i, b in enumerate(bloques, 1):
        #     print(f"--- Partida {i} ---")
        #     print("\n".join(b))

        return bloques

    def _parse_partida(self, lines: list[str]) -> dict:
        num_partida = self._extract_num_partida(lines[0])
        fraccion = self._extract_fraccion(lines[0])
        origen = self._extract_origen(lines[0])  
        descripcion = self._extract_descripcion(lines)
        cantidad = self._extract_cantidad(lines[0])
        peso = self._extract_peso(lines[0])
        valor_pesos = self._extract_valor_pesos(lines)
        valor_dolares = (valor_pesos) / self.tipo_cambio 
        valor_dolares = round(valor_dolares,2)
            
        return {
            "num_partida": num_partida,
            "fraccion": fraccion,
            "origen": origen,
            "descripcion": descripcion,
            "cantidad": cantidad,
            "peso": peso,
            "valor_pesos": valor_pesos,
            "valor_dolares": valor_dolares
        } 

    def _extract_num_partida(self, line: str) -> int | None:
        match = re.search(r'\b(\d{1,3})\s+(\d{6})', line)
        if match:
            value = int(match.group(1))
            print(f"🔢 Número de partida encontrado: {value}")
            return value
        return None
    
    def _extract_fraccion(self, line: str) -> int | None:
        match = re.search(r'\b(\d{1,3})\s+(\d{6})', line)
        if match:
            value = match.group(2)
            print(f"📊 Fracción encontrada: {value}")
            return value
        return None

    def _extract_origen(self, line: str) -> str:
        match = re.search(r'(\d{1,5}\.*\d{1,5})\s\d\s(\d{1,5}\.*\d{1,5})\sUSA\s(\w{3})', line)
        if match:
            value = match.group(3)
            print(f"🌎 Origen encontrado: {value}")
            return value
        return ""
    
    def _extract_cantidad(self, line: str) -> float:
        match = re.search(r'(\d{1,5}\.*\d{1,5})\s\d\s(\d{1,5}\.*\d{1,5})\sUSA\s(\w{3})', line)
        if match:
            value = float(match.group(1))
            value = round(value,2)
            print(f"XD Cantidad encontrada: {value}")
            return value
        return ""
    
    def _extract_peso(self, line: str) -> float:
        match = re.search(r'(\d{1,5}\.*\d{1,5})\s\d\s(\d{1,5}\.*\d{1,5})\sUSA\s(\w{3})', line)
        if match:
            value = float(match.group(2))
            value = round(value,2)
            print(f"DX Peso encontrado: {value}")
            return value
        return ""
           
    def _extract_descripcion(self, lines: list[str]) -> str:
        # Caso 1: estructura "rara"
        if re.search(r'AGENTE\sADUANAL', lines[1]):
            prev_line = lines[1]

            for linea in lines[2:]:
                m = re.search(
                    r'\|\s\d{1,7}(?:\.\d{1,5})?(?:[ \t]+)(\d{1,7})(?:[ \t]+)\d{1,7}(?:\.\d{1,5})\S',
                    linea
                )
                if m:
                    value = prev_line.strip()
                    print(f"Descripcion rara: {value}")
                    return value

                prev_line = linea  # actualizamos la línea previa

        # Caso 2: estructura "normal"
        if len(lines) > 1:
            linea = lines[1]
            value = linea.split("|", 1)[1].strip() if "|" in linea else linea.strip()
        else:
            value = ""

        print(f"Descripcion bien: {value}")
        return value

    def _extract_valor_pesos(self, lines: list[str]) -> float:
        for line in lines:
            m = re.search(r'\|\s\d{1,7}(?:\.\d{1,5})?(?:[ \t]+)(\d{1,7})(?:[ \t]+)\d{1,7}(?:\.\d{1,5})\S', line)
            if m:
                value= m.group(1)
                value = round(float(value), 2)
                print(f"💰 Valor en pesos encontrado: {value}")
                return value

    def calcular_valor_calculado(self, partidas: list[dict]) -> float:
        total = 0.0

        for partida in partidas:
            valor = partida.get("valor_dolares")

            if valor is None:
                continue

            try:
                total += float(valor)
            except (ValueError, TypeError):
                print(f"⚠️ Valor inválido en partida: {valor}")

        return round(total, 2)