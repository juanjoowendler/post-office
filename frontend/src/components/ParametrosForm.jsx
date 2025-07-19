import React, { useState } from "react";

export default function ParametrosForm({ onSimulacionCompleta }) {
  const [lineas, setLineas] = useState(100);
  const [paramT, setParamT] = useState("");
  const [experiencia, setExperiencia] = useState({
    paquetes: { s1: "aprendiz", s2: "aprendiz" },
    ryd: { s1: "aprendiz" },
  });
  const [respuesta, setRespuesta] = useState(null);
  const [estadisticas, setEstadisticas] = useState(null);
  const [error, setError] = useState(null);

  const handleExperienciaChange = (categoria, servidor, valor) => {
    setExperiencia(prev => ({
      ...prev,
      [categoria]: {
        ...prev[categoria],
        [servidor]: valor
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setRespuesta(null);

    // Validaciones
    const nLineas = Number(lineas);
    if (isNaN(nLineas) || nLineas < 0 || nLineas > 10000000) {
      setError("Las líneas deben ser un número entre 0 y 10 000 000.");
      return;
    }
    if (!paramT) {
      setError("El parámetro T es obligatorio.");
      return;
    }

    try {
      // 1) Enviar parámetros al backend
      const res = await fetch("http://localhost:8000/parametros", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lineas: nLineas,
          parametroT: parseFloat(paramT),
          experienciaEmpleados: experiencia
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error en servidor");
      setRespuesta(data);

      // 2) Ejecutar simulación automáticamente
      const simRes = await fetch("http://localhost:8000/simular");
      const datos = await simRes.json();
      const filas = await datos['filas']
      const resumen = datos['estadisticas'];
      if (!simRes.ok) throw new Error(filas.detail || "Error al ejecutar simulación");

      // 3) Devolver filas al componente padre
      onSimulacionCompleta(filas);
      setEstadisticas(resumen);

    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  return (
    <div className="container my-4">
      <h2 className="text-center mb-4">Parámetros de Simulación</h2>

      <form
        onSubmit={handleSubmit}
        className="mx-auto row row-cols-1 row-cols-md-2 g-3"
        style={{ maxWidth: "600px" }}
      >
        {/* Líneas a simular */}
        <div className="col-12">
          <label className="form-label">Líneas a simular:</label>
          <input
            type="number"
            className="form-control"
            value={lineas}
            onChange={(e) => setLineas(e.target.value)}
            min="0"
            max="10000000"
            step="1"
            placeholder="0 – 10 000 000"
            required
          />
        </div>

        {/* Parámetro T */}
        <div className="col-12">
          <label className="form-label">Parámetro T (Runge-Kutta):</label>
          <input
            type="number"
            step="0.01"
            className="form-control"
            value={paramT}
            onChange={(e) => setParamT(e.target.value)}
            placeholder="p.ej. 0.5"
            required
          />
        </div>

        {/* Experiencia de Envio de Paquetes */}
        <fieldset className="col-12 mb-4">
          <legend className="form-label">Envio de Paquetes</legend>
          {["s1", "s2"].map((s, idx) => (
            <div key={s} className="col-12 d-flex align-items-center flex-nowrap mb-2">
              <span className="me-2">{`Empleado${idx + 1}:`}</span>
              <div className="form-check form-check-inline">
                <input
                  type="radio"
                  id={`paq-${s}-aprendiz`}
                  name={`paq-${s}`}
                  className="form-check-input"
                  value="aprendiz"
                  checked={experiencia.paquetes[s] === "aprendiz"}
                  onChange={() => handleExperienciaChange("paquetes", s, "aprendiz")}
                />
                <label className="form-check-label" htmlFor={`paq-${s}-aprendiz`}>
                  Aprendiz
                </label>
              </div>
              <div className="form-check form-check-inline">
                <input
                  type="radio"
                  id={`paq-${s}-experto`}
                  name={`paq-${s}`}
                  className="form-check-input"
                  value="experto"
                  checked={experiencia.paquetes[s] === "experto"}
                  onChange={() => handleExperienciaChange("paquetes", s, "experto")}
                />
                <label className="form-check-label" htmlFor={`paq-${s}-experto`}>
                  Experto
                </label>
              </div>
            </div>
          ))}
        </fieldset>

        {/* Experiencia Reclamos y Devoluciones */}
        <fieldset className="col-12 mb-4">
          <legend className="form-label">Reclamos y Devoluciones</legend>
          <div className="d-flex align-items-center flex-nowrap mb-2">
            <span className="me-3">Empleado:</span>
            {["aprendiz", "experto"].map((val) => (
              <div key={val} className="form-check form-check-inline">
                <input
                  type="radio"
                  id={`ryd-s1-${val}`}
                  name="ryd-s1"
                  className="form-check-input"
                  value={val}
                  checked={experiencia.ryd.s1 === val}
                  onChange={() => handleExperienciaChange("ryd", "s1", val)}
                />
                <label className="form-check-label" htmlFor={`ryd-s1-${val}`}>
                  {val.charAt(0).toUpperCase() + val.slice(1)}
                </label>
              </div>
            ))}
          </div>
        </fieldset>

        {/* Botón de envío */}
        <div className="col-md-6 offset-md-3 mt-4 d-grid">
          <button type="submit" className="btn btn-primary">
            Enviar Parámetros
          </button>
        </div>

        {/* Mensajes de error y éxito */}
        {error && (
          <div className="col-12 alert alert-danger mt-2 text-center">
            <strong>Error:</strong> {error}
          </div>
        )}
        {respuesta && (
          <div className="col-12 alert alert-success mt-2 text-center">
            <strong>Respuesta del backend:</strong> {respuesta.message}
          </div>
        )}
      </form>
      {estadisticas && (
        <div className="col-12 mt-4">
          <h5>Estadísticas Finales</h5>
          <table className="table table-warning table-sm table-bordered mt-2">
            <thead className="table-dark">
              <tr>
                <th>Servidor</th>
                <th>Tiempo de Espera Promedio (min)</th>
                <th>% de Ocupación</th>
                <th>Tiempo Espera Modif</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Paquetes P1 y P2</td>
                <td>{estadisticas.espera_promedio_p.toFixed(2)}</td>
                <td>{estadisticas.ocupacion_p.toFixed(2)}%</td>
                <td>{estadisticas.cambio_tiempo_esp.toFixed(2)}</td>

              </tr>
              <tr>
                <td>Reclamos R1</td>
                <td>{estadisticas.espera_promedio_r1.toFixed(2)}</td>
                <td>{estadisticas.ocupacion_r1.toFixed(2)}%</td>
                <td>-</td>

              </tr>
        
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
