import React from "react";
import logoCorreo from "../assets/correo-utn.png";

function Navbar() {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary px-3">
            <img src={logoCorreo} alt="Correo UTN" height="60" />
            <a className="navbar-brand" href="">CORREO UTN</a>
            <button
                className="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation">
                <span className="navbar-toggler-icon" />
            </button>

            <div className="collapse navbar-collapse" id="navbarNav">
                <ul className="navbar-nav ms-auto">
                    <li className="nav-item">
                        <a className="nav-link active" href="#">Simulación Correo</a>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;
