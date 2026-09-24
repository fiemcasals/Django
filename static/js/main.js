/**
 * ==============================================================================
 * static/js/main.js - Scripts JavaScript Didácticos
 * ==============================================================================
 * Explicación para alumnos:
 * Archivo base para interacciones del frontend en el navegador.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 Plantilla Django Didáctica inicializada correctamente.");

    // Cierre automático suave de alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});
