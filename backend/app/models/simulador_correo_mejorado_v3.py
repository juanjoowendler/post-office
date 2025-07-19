
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

def rungeKutta(R_inicial, T, C, h=0.1):
    t = 0.0
    R = R_inicial
    while R > 0:
        k1 = h * funcionEDO(t, R, C, T)
        k2 = h * funcionEDO(t + h/2, R + k1/2, C, T)
        k3 = h * funcionEDO(t + h/2, R + k2/2, C, T)
        k4 = h * funcionEDO(t + h, R + k3, C, T)
        R -= (k1 + 2*k2 + 2*k3 + k4) / 6
        t += h
    return round(t, 2)

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

class SimuladorCorreo:
    def __init__(self, dias=1, iteraciones_a_mostrar=30):
        self.limite_minutos = dias * 480
        self.max_iteraciones = iteraciones_a_mostrar
        self.iteraciones_a_mostrar = iteraciones_a_mostrar

        self.reloj = 0.0
        self.iteracion = 0
        self.vector_estado = []

        self.cola_paquetes = deque()
        self.cola_reclamos = deque()

        self.servidores_paquetes = [{'estado': 'LIBRE', 'R': 100, 'cliente': None} for _ in range(2)]
        self.servidores_reclamos = [{'estado': 'LIBRE', 'R': 100, 'cliente': None}]

        self.fin_atencion = []
        self.clientes = {}
        self.contador_paquetes = 0
        self.contador_reclamos = 0

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
                cliente.reloj_inicio = self.reloj
                C = len(self.cola_paquetes if tipo == 'PAQUETE' else self.cola_reclamos)
                duracion = rungeKutta(servidor['R'], self.reloj, C)
                fin = round(self.reloj + duracion, 2)
                cliente.reloj_fin = fin
                self.fin_atencion.append({'tipo': tipo, 'fin': fin, 'id': i, 'cliente': cliente, 'rk': duracion})
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
            'RND_FIN_P1': '-',
            'RK_FIN_P1': '-',
            'FIN_P1': '-',
            'RND_FIN_P2': '-',
            'RK_FIN_P2': '-',
            'FIN_P2': '-',
            'RND_FIN_R1': '-',
            'RK_FIN_R1': '-',
            'FIN_R1': '-',
            'SERV_P1': self.servidores_paquetes[0]['estado'],
            'SERV_P2': self.servidores_paquetes[1]['estado'],
            'SERV_R1': self.servidores_reclamos[0]['estado'],
        }
        for e in self.fin_atencion:
            col_id = e['id']
            if e['tipo'] == 'PAQUETE':
                fila[f'RND_FIN_P{col_id+1}'] = round(random.uniform(0, 0.99), 2)
                fila[f'RK_FIN_P{col_id+1}'] = e['rk']
                fila[f'FIN_P{col_id+1}'] = e['fin']
            elif e['tipo'] == 'RECLAMO':
                fila['RND_FIN_R1'] = round(random.uniform(0, 0.99), 2)
                fila['RK_FIN_R1'] = e['rk']
                fila['FIN_R1'] = e['fin']

        for nombre, cliente in self.clientes.items():
            fila[nombre] = cliente.estado
        fila.update(info_extra)
        self.vector_estado.append(fila)

    def ejecutar(self):
        while self.iteracion < self.max_iteraciones and self.reloj <= self.limite_minutos:
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

            elif evento.startswith('LLEGADA_REC'):
                self.contador_reclamos += 1
                cliente = Cliente('REC', self.contador_reclamos)
                cliente.reloj_llegada = self.reloj
                nombre = cliente.nombre()
                self.clientes[nombre] = cliente
                self.prox_llegada_reclamo = self.generar_llegada(15)
                self.iniciar_atencion('RECLAMO', cliente)

            elif evento.startswith('FIN_PAQUETE'):
                id = int(evento.split('_')[2])
                cliente_nombre = '_'.join(evento.split('_')[3:])
                servidor = self.servidores_paquetes[id]
                servidor['estado'] = 'LIBRE'
                cliente = servidor['cliente']
                if cliente:
                    cliente.estado = 'FINALIZADO'
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
                servidor['cliente'] = None
                self.fin_atencion = [f for f in self.fin_atencion if f['tipo'] != 'RECLAMO']
                if self.cola_reclamos:
                    nuevo = self.cola_reclamos.popleft()
                    self.iniciar_atencion('RECLAMO', nuevo)

            self.registrar_estado(evento, info_extra)
            self.iteracion += 1

        df = pd.DataFrame(self.vector_estado)
        df.to_excel("salida_simulacion_correo_v3.xlsx", index=False)
        return df

if __name__ == '__main__':
    sim = SimuladorCorreo()
    df = sim.ejecutar()
    print(df.to_string(index=False))
