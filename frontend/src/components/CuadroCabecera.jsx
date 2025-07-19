import React from "react";

function CuadroCabecera({ filas }) {
  // Obtener las claves de la última fila para buscar los clientes
  const ultimaFila = filas[filas.length - 1] || {};
  const nombresClientes = Object.keys(ultimaFila)
    .filter((k) => k.endsWith("_ESTADO"))
    .map((k) => k.replace("_ESTADO", ""));
  return (
    <thead className="fijada">
      <tr >
        <th colSpan={3} className="sticky-col"></th>
        <th colSpan={6} className="table-dark">SERVICIOS</th>
        <th colSpan={2}></th>
        <th colSpan={10} className="table-success">SERVIDORES ENVIO DE PAQUETES</th>
        <th colSpan={5} className="table-danger">SERVIDOR RECLAMOS Y DEVOLUCIONES</th>
        <th colSpan={6} className="table-primary">VARIABLES PARA ESTADISTICAS</th>
        <th colSpan={nombresClientes.length * 4} className="table-warning">CLIENTES</th>
      </tr>

      <tr >
        <th colSpan={3} className="sticky-col"></th>

        <th colSpan={3} className="table-success">LLEGADA DE CLIENTE A ENVIO DE PAQUETE</th>
        <th colSpan={3} className="table-danger">LLEGADA DE CLIENTE A RECLAMOS Y DEVOLUCIONES</th>
        <th colSpan={2}></th>
        <th colSpan={5} className="table-dark">EMPLEADO 1</th>
        <th colSpan={5} className="table-dark">EMPLEADO 2</th>
        <th colSpan={5} className="table-dark">EMPLEADO 1</th>
        <th colSpan={3} className="table-primary">SERVICIO PAQUETES</th>
        <th colSpan={3} className="table-primary">SERVICIO RECLAMOS</th>


        {nombresClientes.map((nombre) => (
          <th key={`${nombre}_grupo`} colSpan={7} className="table-warning">{nombre}</th>
        ))}
      </tr>

      <tr >
        <th className="table-warning sticky-col-1">IT</th>
        <th className="table-warning sticky-col-2">RELOJ</th>
        <th className="table-warning sticky-col-3">EVENTO</th>

        <th className="table-dark sticky-col-3">RND</th>
        <th className="table-secondary sticky-col-4">TMPO ENTRE LLEG</th>
        <th className="table-secondary">PROX LLEG</th>

        <th className="table-dark">RND</th>
        <th className="table-secondary">TMPO ENTRE LLEG</th>
        <th className="table-secondary">PROX LLEG</th>

        <th className="table-success">COLA PAQ</th>
        <th className="table-danger">COLA REC</th>

        <th className="table-dark">T</th>
        <th className="table-dark">R</th>
        <th className="table-secondary">RK</th>
        <th className="table-secondary">FIN AT</th>
        <th className="table-secondary">ESTADO</th>



        <th className="table-dark">T</th>
        <th className="table-dark">R</th>
        <th className="table-secondary">RK</th>
        <th className="table-secondary">FIN AT</th>
        <th className="table-secondary">ESTADO</th>


        <th className="table-dark">T</th>
        <th className="table-dark">R</th>
        <th className="table-secondary">RK</th>
        <th className="table-secondary">FIN AT</th>
        <th className="table-secondary">ESTADO</th>



        <th className="table-secondary">TMPO ACUM DE ESPERA</th>
        <th className="table-secondary">CONT CLIENTES ATENDIDOS</th>
        <th className="table-secondary">TMPO ACUM USO</th>
        <th className="table-secondary">TMPO ACUM DE ESPERA</th>
        <th className="table-secondary">CONT CLIENTES ATENDIDOS</th>
        <th className="table-secondary">TMPO ACUM USO</th>
        
        {nombresClientes.map((nombre) => (
          <React.Fragment key={nombre}>
            <th className="table-warning">TIPO</th>
            <th className="table-warning">ID</th>
            <th className="table-warning">ESTADO</th>
            <th className="table-warning">LLEGADA</th>
            <th className="table-warning">INICIO</th>
            <th className="table-warning">FIN</th>

          </React.Fragment>
        ))}
      </tr>
    </thead>
  );
}

export default CuadroCabecera;
