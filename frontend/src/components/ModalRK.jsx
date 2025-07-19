import React from "react";

export default function ModalRK({ show, onClose, datosRK }) {
  if (!show || !datosRK) return null;

  return (
    <div className="modal fade show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Detalle de Runge-Kutta</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <div className="modal-body">
            <table className="table table-striped table-bordered table-hover">
              <thead>
                <tr>
                  <th>t</th>
                  <th>R</th>
                  <th>K1</th>
                  <th>K2</th>
                  <th>K3</th>
                  <th>K4</th>
                </tr>
              </thead>
              <tbody>
                {datosRK.map((fila, idx) => (
                  <tr key={idx}>
                    <td>{fila.t}</td>
                    <td>{fila.R}</td>
                    <td>{fila.k1}</td>
                    <td>{fila.k2}</td>
                    <td>{fila.k3}</td>
                    <td>{fila.k4}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="modal-footer">
            <button className="btn btn-secondary" onClick={onClose}>Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  );
}
