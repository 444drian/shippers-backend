# app/services/analysis_service.py

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

class AnalysisService:

    def _format_decimal(self, value):
        return float(
            Decimal(value or 0).quantize(
                Decimal("0.00"),
                rounding=ROUND_HALF_UP
            )
        )

    def procesar(self, payload: dict):

        clientes = payload.get("clientes", [])

        resultados = []

        for cliente in clientes:
            resultado_cliente = self._procesar_cliente(cliente)
            resultados.append(resultado_cliente)

        return {
            "clientes": resultados
        }

    # -------------------------
    # PROCESAR CLIENTE
    # -------------------------
    def _procesar_cliente(self, cliente: dict):

        nombre = cliente.get("nombre")
        partidas = cliente.get("partidas", [])

        grupos = self._agrupar_partidas(partidas)

        resultados = [
            self._construir_resultado(grupo)
            for grupo in grupos.values()
        ]

        return {
            "nombre": nombre,
            "resultados": resultados
        }

    # -------------------------
    # AGRUPAR PARTIDAS
    # -------------------------
    def _agrupar_partidas(self, partidas: list):

        grupos = defaultdict(list)

        for p in partidas:
            key = (p.get("fraccion"), p.get("origen"))
            grupos[key].append(p)

        return grupos

    # -------------------------
    # CONSTRUIR RESULTADO FINAL
    # -------------------------
    def _construir_resultado(self, partidas: list):

        fraccion = partidas[0].get("fraccion")
        origen = partidas[0].get("origen")

        totales_raw = {
            "valor_pesos": sum(p.get("valor_pesos", 0) for p in partidas),
            "valor_dolares": sum(p.get("valor_dolares", 0) for p in partidas),
            "cantidad": sum(p.get("cantidad", 0) for p in partidas),
            "peso": sum(p.get("peso", 0) for p in partidas),
        }

        totales = {
            k: self._format_decimal(v)
            for k, v in totales_raw.items()
        }

        descripciones = self._obtener_descripciones(partidas)

        pedimentos = self._mapear_pedimentos(partidas)

        return {
            "fraccion": fraccion,
            "origen": origen,
            "totales": totales,
            "partidas_count": len(partidas),
            "descripciones": descripciones,
            "pedimentos": pedimentos
        }

    # -------------------------
    # DESCRIPCIONES ÚNICAS
    # -------------------------
    def _obtener_descripciones(self, partidas: list):
        return [
            p.get("descripcion")
            for p in partidas
            if p.get("descripcion")
        ]

    # -------------------------
    # TRAZABILIDAD PEDIMENTOS
    # -------------------------
    def _mapear_pedimentos(self, partidas: list):

        ped_map = defaultdict(list)

        for p in partidas:
            ped = p.get("nume_ped")
            num = p.get("num_partida")

            ped_map[ped].append(num)

        return [
            {
                "nume_ped": ped,
                "partidas": nums
            }
            for ped, nums in ped_map.items()
        ]
    


    