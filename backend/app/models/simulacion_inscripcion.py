import random
import math
import pandas as pd
from collections import deque

class SimuladorInscripcion:
    def __init__(self, tiempo_limite, max_iteraciones, mostrar_desde, iteraciones_a_mostrar, paso_euler):
        self.tiempo_limite = tiempo_limite
        self.max_iteraciones = max_iteraciones
        self.mostrar_desde = mostrar_desde
        self.iteraciones_a_mostrar = iteraciones_a_mostrar
        self.paso_euler = paso_euler

        self.reloj = 0.0
        self.iteracion = 0
        self.cola = deque()
        self.pcs = ["LIBRE"] * 6
        self.max_cola = 4
        self.contador_pc1 = 0

        self.prox_llegada = 0.0
        self.rnd_llegada = None
        self.dt_llegada = None
        self.prox_fin_pc = {i+1: float('inf') for i in range(6)}
        self.prox_fin_mantenimiento = float('inf')

        self.total_llegadas = 0
        self.total_rechazos = 0
        self.total_inscripciones = 0
        self.total_mantenimientos = 0

        self.vector_estado = []
        self.integraciones = []

        self._generar_proxima_llegada()
        ini = {
            'ITERACION': 0,
            'TIEMPO': 0.0,
            'EVENTO': 'INICIO',
            'RND_INSCRIPCION': '-',
            'TIEMPO_INSCRIPCION': '-',
            'RND_LLEGADA': self.rnd_llegada,
            'TIEMPO_ENTRE_LLEGADA': self.dt_llegada,
            'PROXIMA_LLEGADA': self.prox_llegada,
        }
        for pc in range(1,7):
            ini[f'FIN_INSCRIPCION_PC{pc}'] = '-'
            ini[f'PC{pc}_ESTADO'] = self.pcs[pc-1]
        ini.update({
            'RND_MANTENIMIENTO': '-',
            'A0': '-',
            'TIEMPO_FIN_MANTENIMIENTO': '-',
            'COLA_ALUMNOS': 0,
            'CONT_RECHAZOS': 0,
            'CONT_LLEGADAS': 0,
            'PORC_RECHAZOS': 0,
            'INSCRIPCIONES_FINALIZADAS': 0,
            'MANT_FIN_PC1': 0,
            'MANT_PROM_DIARIO_PC1': 0
        })
        self.vector_estado.append(ini)

    def _generar_proxima_llegada(self):
        rnd = round(random.uniform(0, 0.99), 2)
        dt = round(-2 * math.log(1 - rnd), 2)
        self.rnd_llegada = rnd
        self.dt_llegada = dt
        self.prox_llegada = round(self.reloj + dt, 2)

    def _generar_inscripcion(self):
        rnd = round(random.uniform(0, 0.99), 2)
        dur = round(5 + rnd * (8 - 5), 2)
        return dur, rnd

    def _generar_A0(self):
        opciones = [1000, 1500, 2000]
        rnd = round(random.uniform(0, 0.99), 2)
        A0 = opciones[int(rnd * len(opciones)) % len(opciones)]
        return A0, rnd

    def ejecutar(self):
        while self.iteracion < self.max_iteraciones and self.reloj <= self.tiempo_limite:
            tiempos = {'LLEGADA': self.prox_llegada}
            for pc, tfin in self.prox_fin_pc.items():
                tiempos[f'FIN_INS_PC{pc}'] = tfin
            tiempos['FIN_MANT'] = self.prox_fin_mantenimiento
            evento, t_evento = min(tiempos.items(), key=lambda x: x[1])
            self.reloj = round(t_evento, 2)

            rnd_ins = '-'
            dt_insc = '-'
            rnd_mant = '-'
            A0 = '-'

            if evento == 'LLEGADA':
                self.total_llegadas += 1
                self._generar_proxima_llegada()
                libres = [i for i, st in enumerate(self.pcs) if st == 'LIBRE']
                if libres:
                    idx = libres[0]
                    dur_insc, rnd_ins = self._generar_inscripcion()
                    dt_insc = dur_insc
                    self.pcs[idx] = 'OCUPADO'
                    self.prox_fin_pc[idx+1] = round(self.reloj + dur_insc, 2)
                    self.total_inscripciones += 1
                else:
                    if len(self.cola) < self.max_cola:
                        self.cola.append(self.reloj)
                    else:
                        self.total_rechazos += 1

            elif evento.startswith('FIN_INS_PC'):
                pc = int(evento.split('FIN_INS_PC')[-1])
                self.pcs[pc-1] = 'LIBRE'
                self.prox_fin_pc[pc] = float('inf')
                if self.cola:
                    _ = self.cola.popleft()
                    dur_insc, rnd_ins = self._generar_inscripcion()
                    dt_insc = dur_insc
                if pc == 1:
                    self.contador_pc1 += 1
                    if self.contador_pc1 >= 3:
                        A0, rnd_mant = self._generar_A0()
                        tabla = []
                        t = 0.0
                        A = A0
                        while A >= 0:
                            dA = -68 - (A**2 / A0)
                            tabla.append((round(t, 2), round(A, 2), round(dA, 2)))
                            A = round(A + self.paso_euler * dA, 2)
                            t = round(t + self.paso_euler, 2)
                        self.integraciones.append({'A0': A0, 'tabla': tabla})
                        dur_mant = tabla[-1][0] if tabla else 0
                        self.prox_fin_mantenimiento = round(self.reloj + dur_mant, 2)
                        self.contador_pc1 = 0
                        self.pcs[pc-1] = 'EN MANTENIMIENTO'
                else:
                    self.pcs[pc-1] = 'OCUPADO'
                    self.prox_fin_pc[pc] = round(self.reloj + dur_insc, 2)
                    self.total_inscripciones += 1    

            else:  # FIN_MANT
                self.prox_fin_mantenimiento = float('inf')
                self.pcs[0] = 'LIBRE'
                self.total_mantenimientos += 1
                if self.cola:
                    _ = self.cola.popleft()
                    dur_insc, rnd_ins = self._generar_inscripcion()
                    dt_insc = dur_insc
                    self.pcs[0] = 'OCUPADO'
                    self.prox_fin_pc[1] = round(self.reloj + dur_insc, 2)
                    self.total_inscripciones += 1

            fila = {
                'ITERACION': self.iteracion + 1,
                'TIEMPO': self.reloj,
                'EVENTO': evento,
                'RND_INSCRIPCION': rnd_ins,
                'TIEMPO_INSCRIPCION': dt_insc,
                'RND_LLEGADA': self.rnd_llegada,
                'TIEMPO_ENTRE_LLEGADA': self.dt_llegada,
                'PROXIMA_LLEGADA': self.prox_llegada,
            }
            for pc in range(1, 7):
                val = self.prox_fin_pc[pc]
                fila[f'FIN_INSCRIPCION_PC{pc}'] = val if val != float('inf') else '-'
            fila.update({
                'RND_MANTENIMIENTO': rnd_mant,
                'A0': A0,
                'TIEMPO_FIN_MANTENIMIENTO': self.prox_fin_mantenimiento if self.prox_fin_mantenimiento != float('inf') else '-'
            })
            for pc in range(1, 7):
                fila[f'PC{pc}_ESTADO'] = self.pcs[pc-1]
            fila.update({
                'COLA_ALUMNOS': len(self.cola),
                'CONT_RECHAZOS': self.total_rechazos,
                'CONT_LLEGADAS': self.total_llegadas,
                'PORC_RECHAZOS': round(self.total_rechazos / self.total_llegadas * 100, 2) if self.total_llegadas > 0 else 0,
                'INSCRIPCIONES_FINALIZADAS': self.total_inscripciones,
                'MANT_FIN_PC1': self.total_mantenimientos,
                'MANT_PROM_DIARIO_PC1': round(self.total_mantenimientos / (self.reloj / self.tiempo_limite if self.reloj > 0 else 1), 2)
            })
            self.vector_estado.append(fila)
            self.iteracion += 1

        df = pd.DataFrame(self.vector_estado)
        df_m = df[df['TIEMPO'] >= self.mostrar_desde].head(self.iteraciones_a_mostrar)
        ultima = df[df['TIEMPO'] <= self.tiempo_limite].tail(1)
        return pd.concat([df_m, ultima], ignore_index=True), self.integraciones
