import 'bootstrap/dist/css/bootstrap.min.css'; // ✅ Estilos de Bootstrap
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // ✅ Opcional: solo si usás componentes JS como modals
import './index.css';
import App from './App.jsx';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
