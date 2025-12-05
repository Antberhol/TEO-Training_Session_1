from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime
from typing import NamedTuple
import csv


class Alquiler(NamedTuple):
    nombre: str
    dni: str
    fecha_inicio: date
    fecha_fin: date
    estacion: str
    bici_tipo: str
    precio_dia: float
    servicios: list[str]


def parse_fecha(cadena: str) -> date:
    """Convierte una fecha ISO (YYYY-MM-DD) a date."""
    return datetime.strptime(cadena, "%Y-%m-%d").date()


def lee_alquileres(ruta: str) -> list[Alquiler]:
    lista_alquileres = []
    with open(ruta, encoding= "utf-8") as f:
        lector = csv.reader(f)
        next(lector)
        for campos in lector:
            nombre = campos[0]
            dni = campos[1]
            fecha_inicio = parse_fecha(campos[2])
            fecha_fin= parse_fecha(campos[3])
            estacion = campos[4]
            bici_tipo = campos[5]
            precio_dia = float(campos[6])
            servicios = campos[7].split(',')
            if servicios == "":
                servicios = []
                
            alquiler = Alquiler(nombre, dni, fecha_inicio, fecha_fin, estacion, bici_tipo, precio_dia, servicios)
            lista_alquileres.append(alquiler)
    return lista_alquileres   


def total_facturado(
    alquileres: list[Alquiler],
    fecha_ini: date | None = None,
    fecha_fin: date | None = None,
) -> float:
    total = 0.0
    for alquiler in alquileres:
        if alquiler.fecha_inicio ==fecha_ini  and alquiler.fecha_fin == fecha_fin:
            total = (alquiler.fecha_fin - alquiler.fecha_inicio).days * alquiler.precio_dia
    return total

def alquileres_mas_largos(
    alquileres: list[Alquiler],
    n: int = 3,
) -> list[tuple[str, date]]:
    diccionario = defaultdict()
    lista = []
    for alquiler in alquileres:
        diccionario[alquiler.nombre] = (alquiler.fecha_fin - alquiler.fecha_inicio).days
        lista = sorted(diccionario.items(), key=lambda x: x[1], reverse=True)
    return lista[:n]


def cliente_mayor_facturacion(alquileres, servicios=None):
    dicc = defaultdict(float)

    for alquiler in alquileres:
        if servicios is None or servicios <= alquiler.servicios:
            dias = (alquiler.fecha_fin - alquiler.fecha_inicio).days
            dicc[alquiler.dni] += dias * alquiler.precio_dia

    return max(dicc.items(), key=lambda x: x[1])


def servicio_top_por_mes(
    alquileres: list[Alquiler],
    estaciones: set[str] | None = None,
) -> dict[str, str]:
    """Servicio más contratado por mes (fecha_inicio), filtrando estaciones opcionalmente."""
    raise NotImplementedError


def media_dias_entre_alquileres(alquileres: list[Alquiler]) -> float:
    """Media de días entre alquileres consecutivos (por fecha_inicio)."""
    raise NotImplementedError


def indexar_por_estacion(alquileres: list[Alquiler]) -> dict[str, list[Alquiler]]:
    """Diccionario estacion -> lista de Alquiler."""
    raise NotImplementedError


if __name__ == "__main__":
    # Espacio para pruebas rápidas
    import pathlib

    ruta = pathlib.Path(__file__).resolve().parent.parent / "data" / "alquileres.csv"
    print(f"Dataset: {ruta}")
