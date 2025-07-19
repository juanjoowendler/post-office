
import React from "react";
import CuadroCabecera from "./CuadroCabecera";
import CuadroFilas from "./CuadroFilas";

function Cuadro({ filas }) {
  if (!filas || filas.length === 0) {
    return <p className="text-center mt-3">Esperando resultados de simulación...</p>;
  }

  const filasFijas = filas.slice(0, 3);
  const filasRestantes = filas.slice(3);

  return (
    <div className="container-fluid px-0">
      <div className="table-responsive table-container">
        <table className="table table-bordered border-dark text-center mb-0">
          <CuadroCabecera filas={filas} />
          <thead className="filas-fijas">
            {filasFijas.map((fila, i) => (
              <tr key={`fija-${i}`}>
                {Object.values(fila).map((valor, j) => (
                  <td key={j}>{valor}</td>
                ))}
              </tr>
            ))}
          </thead>
          <CuadroFilas filas={filasRestantes} />
        </table>
      </div>
    </div>
  );
}

export default Cuadro;
