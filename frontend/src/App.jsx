import "./App.css";

import { useState } from "react";
import Navbar from "./components/Navbar";
import Cuadro from "./components/Cuadro";
import ParametrosForm from "./components/ParametrosForm";

function App() {
  const [filas, setFilas] = useState([]); 

  const onSimulacionCompleta = (nuevasFilas) => {
    // const primeras150 = nuevasFilas.slice(0, 150);
    // const ultimas150 = nuevasFilas.slice(-150);
    // const filaSeparadora = { EVENTO: '... FILAS OMITIDAS ...' };
    // const datosReducidos = [...primeras150, filaSeparadora, ...ultimas150];
    setFilas(nuevasFilas);
  };

  return (
    <>
      <Navbar />
      <div>
        {/* Le pasamos la función al formulario */}
        <ParametrosForm onSimulacionCompleta={onSimulacionCompleta} />
      </div>

      <h3>Tabla de simulación:</h3>

      {/* Le pasamos las filas al componente Cuadro */}
      <Cuadro filas={filas} />
    </>
  );
}

export default App;
