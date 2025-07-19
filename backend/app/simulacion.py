
import random
import math
import pandas as pd
from collections import deque

def media_entre_llegadas(tasa_por_hora):
    return 60 / tasa_por_hora

def distribucion_exponencial(tasa_por_hora):
    rnd = round(random.uniform(0, 0.99), 2)
    media = media_entre_llegadas(tasa_por_hora)
    tiempo = round(-media * math.log(1 - rnd), 2)
    return rnd, tiempo

def funcionEDO(t, R, C, T):
    return C + 0.2 * T + t**2

def rungeKutta(R, T, C, h=1):
    """
    Integra dR/dt = f(C, T, t) desde R_act = 0 hasta superar R.
    Devuelve los primeros 2 pasos, una línea suspensiva y el paso final.
    """
    pasos = []
    R_act = 0.00
    t = 0.00

    while R_act <= R:
        k1 = funcionEDO(t, R, C, T)
        k2 = funcionEDO(t + h/2, R, C, T)
        k3 = funcionEDO(t + h/2, R, C, T)
        k4 = funcionEDO(t + h, R, C, T)

        pasos.append({
            "t": round(t, 2),
            "R": round(R_act, 2),  # mostrar R acumulado
            "k1": round(k1, 2),
            "k2": round(k2, 2),
            "k3": round(k3, 2),
            "k4": round(k4, 2),
        })

        delta_R = (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
        R_act += delta_R
        t += h

    # Agregar última fila que marca el final
    pasos.append({
        "t": round(t, 2),
        "R": round(R_act, 2),
        "k1": "-",
        "k2": "-",
        "k3": "-",
        "k4": "-",
    })

    return {
        "resultado": round(t, 2),
        "detalle": pasos
    }

class Cliente:
    def __init__(self, tipo, id):
        self.tipo = tipo
        self.id = id
        self.estado = 'EN SISTEMA'
        self.reloj_llegada = None
        self.reloj_inicio = None
        self.reloj_fin = None

    def nombre(self):
        return f'{self.tipo}{self.id}'

#     {
#   "lineas": 100,
#   "parametroT": 1,
#   "experienciaEmpleados": {
#     "paquetes": { "s1": "aprendiz", "s2": "aprendiz" },
#     "ryd": { "s1": "aprendiz" }
#   }
# }
class SimuladorCorreo:
    def __init__(self, lineas, parametroT, experienciaEmpleados):
        self.lineas = lineas
        self.experienciaEmpleados = experienciaEmpleados
        self.param_t = parametroT

        self.limite_minutos = 480
        self.iteraciones_a_mostrar = lineas

        self.reloj = 0.0
        self.iteracion = 0
        self.vector_estado = []

        self.cola_paquetes = deque()
        self.cola_reclamos = deque()

        self.servidores_paquetes = [
    {
        'estado': 'LIBRE',
        'R': 300 if experienciaEmpleados.paquetes.s1 == 'aprendiz' else 100,
        'cliente': None
    },
    {
        'estado': 'LIBRE',
        'R': 300 if experienciaEmpleados.paquetes.s2 == 'aprendiz' else 100,
        'cliente': None
    }
]
        self.servidores_reclamos = [{'estado': 'LIBRE', 'R': 300 if experienciaEmpleados.ryd.s1 == "aprendiz" else 100, 'cliente': None}]

        self.fin_atencion = []
        self.clientes = {}
        self.contador_paquetes = 0
        self.contador_reclamos = 0

        self.acum_espera_paq = 0.0
        self.acum_espera_rec = 0.0
        self.cont_clientes_atendidos_paq = 0
        self.cont_clientes_atendidos_rec = 0
        self.acum_uso_ryd = 0.0
        self.reloj_anterior = 0.0
    
        #RND ! TIEMPO ENTRE ! PROXIMA LLEGADA {}
        self.prox_llegada_paquete = self.generar_llegada(25)
        self.prox_llegada_reclamo = self.generar_llegada(15)
        self.registrar_estado('INICIO', {})

    def generar_llegada(self, tasa):
        rnd, tiempo = distribucion_exponencial(tasa)
        return {'rnd': rnd, 'dt': tiempo, 'hora': round(self.reloj + tiempo, 2)}

    def iniciar_atencion(self, tipo, cliente):
        duracion = None
        for i, servidor in enumerate(self.servidores_paquetes if tipo == 'PAQUETE' else self.servidores_reclamos):
            if servidor['estado'] == 'LIBRE':
                servidor['estado'] = 'OCUPADO'
                servidor['cliente'] = cliente
                cliente.estado = 'SIENDO ATENDIDO'
                
                # para estadisticos

                if tipo == 'PAQUETE':
                    espera = self.reloj - cliente.reloj_llegada
                    self.acum_espera_paq += espera
                if tipo == 'RECLAMO':
                    espera = self.reloj - cliente.reloj_llegada
                    self.acum_espera_rec += espera


                cliente.reloj_inicio = self.reloj
                C = len(self.cola_paquetes if tipo == 'PAQUETE' else self.cola_reclamos)
                res_rk = rungeKutta(servidor['R'], self.reloj, C)
                duracion = res_rk["resultado"]
                detalle_rk = res_rk["detalle"]

                fin = round(self.reloj + duracion, 2)
                cliente.reloj_fin = fin
                self.fin_atencion.append({'tipo': tipo, 'fin': fin, 'id': i, 'cliente': cliente, 'rk': duracion, 'detalle_rk': detalle_rk})
                break
        else:
            if tipo == 'PAQUETE':
                self.cola_paquetes.append(cliente)
            else:
                self.cola_reclamos.append(cliente)
            cliente.estado = 'EN COLA'


    def registrar_estado(self, evento, info_extra):
        fila = {
            'ITERACION': self.iteracion + 1,
            'RELOJ': round(self.reloj, 2),
            'EVENTO': evento,
            'RND_PAQ': self.prox_llegada_paquete['rnd'],
            'TE_PAQ': self.prox_llegada_paquete['dt'],
            'PROX_LLEGADA_PAQ': self.prox_llegada_paquete['hora'],
            'RND_REC': self.prox_llegada_reclamo['rnd'],
            'TE_REC': self.prox_llegada_reclamo['dt'],
            'PROX_LLEGADA_REC': self.prox_llegada_reclamo['hora'],
            'COLA_PAQ': len(self.cola_paquetes),
            'COLA_REC': len(self.cola_reclamos),

            'T_P1': self.param_t,
            'TIPO_P1': '-',
            'RK_FIN_P1': '-',
            'FIN_P1': '-',
            'SERV_P1': self.servidores_paquetes[0]['estado'],

            'T_P2': self.param_t,
            'TIPO_P2': '-',
            'RK_FIN_P2': '-',
            'FIN_P2': '-',
            'SERV_P2': self.servidores_paquetes[1]['estado'],

            'T_R1': self.param_t,
            'TIPO_R1': '-',
            'RK_FIN_R1': '-',
            'FIN_R1': '-',
            'SERV_R1': self.servidores_reclamos[0]['estado'],

            'ACUM_T_ESPERA_P': round(self.acum_espera_paq, 2),
            'CONT_CLI_AT_P': self.cont_clientes_atendidos_paq,
            'ACUM_T_USO_P': '-',

            'ACUM_T_ESPERA_R': round(self.acum_espera_rec, 2),
            'CONT_CLI_AT_R': self.cont_clientes_atendidos_rec,
            'ACUM_T_USO_R': round(self.acum_uso_ryd, 2),

        }
        fila['TIPO_P1'] = 'aprendiz' if self.servidores_paquetes[0]['R'] == 300 else 'experto'
        fila['TIPO_P2'] = 'aprendiz' if self.servidores_paquetes[1]['R'] == 300 else 'experto'
        fila['TIPO_R1'] = 'aprendiz' if self.servidores_reclamos[0]['R'] == 300 else 'experto'
        for e in self.fin_atencion:
            col_id = e['id']
            if e['tipo'] == 'PAQUETE':
                # fila[f'RND_FIN_P{col_id+1}'] = round(random.uniform(0, 0.99), 2)
                fila[f'RK_FIN_P{col_id+1}'] = e['rk']
                fila[f'FIN_P{col_id+1}'] = e['fin']
            elif e['tipo'] == 'RECLAMO':
                # fila['RND_FIN_R1'] = round(random.uniform(0, 0.99), 2)
                fila['RK_FIN_R1'] = e['rk']
                fila['FIN_R1'] = e['fin']

        for nombre, cliente in self.clientes.items():
            fila[f'{nombre}_TIPO'] = cliente.tipo
            fila[f'{nombre}_ID'] = cliente.id
            fila[f'{nombre}_ESTADO'] = cliente.estado
            fila[f'{nombre}_LLEGADA'] = cliente.reloj_llegada
            fila[f'{nombre}_INICIO'] = cliente.reloj_inicio
            fila[f'{nombre}_FIN'] = cliente.reloj_fin
        fila.update(info_extra)
        self.vector_estado.append(fila)

    def ejecutar(self):
        while self.iteracion < self.lineas and self.reloj <= self.limite_minutos:
            eventos = [
                ('LLEGADA_PAQ', self.prox_llegada_paquete['hora']),
                ('LLEGADA_REC', self.prox_llegada_reclamo['hora'])
            ] + [(f'FIN_{e["tipo"]}_{e["id"]}_{e["cliente"].nombre()}', e['fin']) for e in self.fin_atencion]

            evento, instante = min(eventos, key=lambda x: x[1])
            self.reloj = instante
            info_extra = {}

            if evento.startswith('LLEGADA_PAQ'):
                self.contador_paquetes += 1
                cliente = Cliente('PAQ', self.contador_paquetes)
                cliente.reloj_llegada = self.reloj
                nombre = cliente.nombre()
                self.clientes[nombre] = cliente
                self.prox_llegada_paquete = self.generar_llegada(25)
                self.iniciar_atencion('PAQUETE', cliente)
                evento = f'LLEGADA_PAQ_{cliente.id}'

            elif evento.startswith('LLEGADA_REC'):
                self.contador_reclamos += 1
                cliente = Cliente('REC', self.contador_reclamos)
                cliente.reloj_llegada = self.reloj
                nombre = cliente.nombre()
                self.clientes[nombre] = cliente
                self.prox_llegada_reclamo = self.generar_llegada(15)
                self.iniciar_atencion('RECLAMO', cliente)
                evento = f'LLEGADA_REC_{cliente.id}'

            elif evento.startswith('FIN_PAQUETE'):
                id = int(evento.split('_')[2])
                cliente_nombre =  '_'.join(evento.split('_')[3:])
                servidor = self.servidores_paquetes[id]
                servidor['estado'] = 'LIBRE'
                cliente = servidor['cliente']
                if cliente:
                    cliente.estado = 'FINALIZADO'
                    self.cont_clientes_atendidos_paq += 1
                servidor['cliente'] = None
                self.fin_atencion = [f for f in self.fin_atencion if not (f['tipo'] == 'PAQUETE' and f['id'] == id)]
                if self.cola_paquetes:
                    nuevo = self.cola_paquetes.popleft()
                    self.iniciar_atencion('PAQUETE', nuevo)

            elif evento.startswith('FIN_RECLAMO'):
                servidor = self.servidores_reclamos[0]
                cliente = servidor['cliente']
                servidor['estado'] = 'LIBRE'
                if cliente:
                    cliente.estado = 'FINALIZADO'
                    self.cont_clientes_atendidos_rec += 1
                servidor['cliente'] = None
                self.fin_atencion = [f for f in self.fin_atencion if f['tipo'] != 'RECLAMO']
                if self.cola_reclamos:
                    nuevo = self.cola_reclamos.popleft()
                    self.iniciar_atencion('RECLAMO', nuevo)

            if self.servidores_reclamos[0]['estado'] == 'OCUPADO':
                delta = self.reloj - self.reloj_anterior
                self.acum_uso_ryd += delta

            uso_paq = 0.0
            for servidor in self.servidores_paquetes:
                if servidor['estado'] == 'OCUPADO':
                    uso_paq += self.reloj - self.reloj_anterior

            acum_uso_paq = 0.0
            if self.vector_estado:
                ultima_fila = self.vector_estado[-1]
                if isinstance(ultima_fila['ACUM_T_USO_P'], (int, float)):
                    acum_uso_paq = ultima_fila['ACUM_T_USO_P']
                elif str(ultima_fila['ACUM_T_USO_P']).replace('.', '', 1).isdigit():
                    acum_uso_paq = float(ultima_fila['ACUM_T_USO_P'])

            info_extra['ACUM_T_USO_P'] = round(acum_uso_paq + uso_paq, 2)

            self.registrar_estado(evento, info_extra)
            self.reloj_anterior = self.reloj
            self.iteracion += 1

        df = pd.DataFrame(self.vector_estado)
        df = df.fillna("")
        # return df

        reloj_final = self.reloj

        descansos = reloj_final // 60
        retraso_total = descansos * 5
   
        estadisticas = {
            "espera_promedio_p": self.acum_espera_paq / self.cont_clientes_atendidos_paq if self.cont_clientes_atendidos_paq > 0 else 0,
            "espera_promedio_r1": self.acum_espera_rec / self.cont_clientes_atendidos_rec if self.cont_clientes_atendidos_rec > 0 else 0,

            "ocupacion_p": ((float(self.vector_estado[-1]['ACUM_T_USO_P'])/2 )/ reloj_final) * 100 if reloj_final > 0 else 0,
            "ocupacion_r1": (self.acum_uso_ryd / reloj_final) * 100 if reloj_final > 0 else 0,
        
            "cambio_tiempo_esp": (retraso_total  + self.acum_espera_paq )

        }

        return {
            "filas": df.to_dict(orient="records") ,
            "estadisticas": estadisticas
        }

