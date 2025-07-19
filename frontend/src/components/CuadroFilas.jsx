import React, { useState } from "react";
import ModalRK from "./ModalRK";

function CuadroFilas({ filas }) {
  const [mostrarModal, setMostrarModal] = useState(false);
  const [datosRK, setDatosRK] = useState(null);
  const [filaSeleccionada, setFilaSeleccionada] = useState(null);

  const handleRKClick = async (valorRK, fila) => {
    try {
      const campoRK = Object.keys(fila).find((k) => fila[k] === valorRK && k.includes("RK_"));
      let tipo = "";
      if (campoRK?.includes("P1")) tipo = "TIPO_P1";
      else if (campoRK?.includes("P2")) tipo = "TIPO_P2";
      else if (campoRK?.includes("R1")) tipo = "TIPO_R1";

      const tipoEmpleado = fila[tipo];
      const R = tipoEmpleado === "aprendiz" ? 300 : 100;
      const T = fila.RELOJ;
      const C = campoRK?.includes("R") ? fila.COLA_REC : fila.COLA_PAQ;

      const url = `http://localhost:8000/runge-kutta?R=${R}&T=${T}&C=${C}`;
      const res = await fetch(url);
      const data = await res.json();

      setDatosRK(data);
      setMostrarModal(true);
    } catch (error) {
      console.error("Error al obtener detalle RK:", error);
      setDatosRK([]);
      setMostrarModal(true);
    }
  };

  const handleRowClick = (index) => {
    setFilaSeleccionada(prev => prev === index ? null : index);
  };

  return (
    <>
      <tbody>
        {filas.map((fila, index) => (
          <tr
            key={index}
            onClick={() => handleRowClick(index)}
            className={index === filaSeleccionada ? "fila-seleccionada table-danger" : ""}
            style={{ cursor: "pointer" }}
          >
            {Object.entries(fila).map(([key, valor], j) => {
              const stickyClass = j <= 2 ? `sticky-col${j > 0 ? `-${j + 1}` : ""}` : "";
              const esRK = key.includes("RK_");

              return (
                <td
                  key={j}
                  className={stickyClass}
                  style={{ cursor: esRK ? "pointer" : "default", color: esRK ? "blue" : "black" }}
                  onClick={(e) => {
                    if (esRK) {
                      e.stopPropagation(); // evita que vuelva a activar el resaltado
                      handleRKClick(valor, fila);
                    }
                  }}
                >
                  {valor}
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>

      <ModalRK show={mostrarModal} onClose={() => setMostrarModal(false)} datosRK={datosRK} />
    </>
  );
}

export default CuadroFilas;
