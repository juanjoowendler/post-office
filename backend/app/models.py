from pydantic import BaseModel 
from typing import List, Dict, Any

class FormParametros(BaseModel):
    lineas: int
    limInfExpertizEmpleado: int
    limSupExpertizEmpleado: int
    parametroT: float
    """
    Acá puse más o menos los parámetros que se supone que debería poder modificar el usuario
    Lineas a simular: Faltaría hacer la validación en el Forms que sea de: 100, 1000, 50000, 10000000 corte desplegable.
    Limite inferior expertiz del empleado: Indica q tan malo es definiendo un limite para la Distr. Uniforme.
    Lim Superior expertiz del empleado: Indica q tan bueno es definiendo el máximo de capacidad que este puede tener para la Distr. Uniforme.
    parametro T: Esté parámetro es una cte para poder realizar Runge Kutta de 4to orden.
    """

# class fila(BaseModel):
#     __root__: Dict[str, Any]

# class Simulacion(BaseModel):
#     filas: List[fila]

# backend/models.py

class Servidor(BaseModel):
    """
    Representa cualquiera de tus servidores (EDP E1, EDP E2, RYD E1, Estadísticas S1, S2…).
    El campo `id_servidor` debe coincidir con el sufijo que usas en las cabeceras,
    por ejemplo: 'edp_e1', 'edp_e2', 'ryd_e1', 's1', 's2', etc.
    """
    id_servidor: str
    rnd: float
    variable_t: float
    demora_de_atencion: float
    hora_fin_de_atencion: float
    estado: str

    def to_row(self) -> Dict[str, Any]:
        """
        Devuelve un dict cuyas keys coinciden con las columnas de la tabla:
         - rnd_<id>
         - variable_t_<id>
         - demora_de_atencion_<id>
         - hora_fin_de_atencion_<id>
         - estado_<id>
        """
        suffix = self.id_servidor
        return {
            f"rnd_{suffix}":                  round(self.rnd, 3),
            f"variable_t_{suffix}":           round(self.variable_t, 3),
            f"demora_de_atencion_{suffix}":   round(self.demora_de_atencion, 2),
            f"hora_fin_de_atencion_{suffix}": round(self.hora_fin_de_atencion, 2),
            f"estado_{suffix}":               self.estado,
        }


class Cliente(BaseModel):
    """
    Modela al cliente que entra/sale de la cola.
    Sus atributos coinciden con las últimas columnas:
      - id_cliente
      - tipo_cliente
      - estado_cliente
      - tiempo_llegada_cliente
      - inicio_atencion_cliente
      - fin_atencion_cliente
    """
    id_cliente: int
    tipo_cliente: int
    estado_cliente: str
    tiempo_llegada_cliente: float
    inicio_atencion_cliente: float | None
    fin_atencion_cliente: float | None

    def to_row(self) -> Dict[str, Any]:
        """
        Devuelve exactamente el dict con las keys que el Front espera.
        """

        return self.dict()

