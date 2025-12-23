<?php
/**
 * Contact Page - Pablo Cirre
 */

$page_title = "Contacto | Desarrollo y Formación - Pablo Cirre";
$page_description = "Contacta para proyectos de Big Data, Desarrollo Web o Formación. Email y WhatsApp directos.";
include '../../Components/header.php';
?>

<div class="container" style="padding-top: 80px; padding-bottom: 80px; max-width: 800px;">
    <h1 class="hero-title">Hablemos.</h1>
    <p class="hero-subtitle">
        ¿Tienes un proyecto técnico o necesitas formación especializada? <br>
        Respondo personalmente en menos de 24h.
    </p>

    <!-- Contact Grid -->
    <div class="row"
        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 50px;">

        <!-- Email Card -->
        <a href="mailto:pablo@centraldecomunicacion.es" class="data-panel"
            style="text-decoration: none; color: inherit; transition: transform 0.2s;">
            <div class="panel-header">
                <span class="panel-label">EMAIL</span>
                <div class="light on" style="background: var(--accent-color);"></div>
            </div>
            <div style="padding: 20px 0;">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px;">Email</h3>
                <p style="color: var(--text-secondary); margin-bottom: 5px;">Proyectos y Colaboraciones</p>
                <span
                    style="font-family: 'IBM Plex Mono', monospace; color: var(--accent-color);">pablo@centraldecomunicacion.es</span>
            </div>
        </a>

        <!-- WhatsApp Card -->
        <a href="https://wa.me/34657089081" target="_blank" class="data-panel"
            style="text-decoration: none; color: inherit; transition: transform 0.2s;">
            <div class="panel-header">
                <span class="panel-label">WHATSAPP</span>
                <div class="light on" style="background: #25D366;"></div>
            </div>
            <div style="padding: 20px 0;">
                <h3 style="font-size: 1.5rem; margin-bottom: 10px;">WhatsApp Directo</h3>
                <p style="color: var(--text-secondary); margin-bottom: 5px;">Consultas Rápidas</p>
                <span style="font-family: 'IBM Plex Mono', monospace; color: #25D366;">+34 657 089 081</span>
            </div>
        </a>

    </div>

    <!-- Service Areas -->
    <h2 class="section-title" style="margin-top: 80px;">Áreas de Respuesta</h2>
    <div style="margin-bottom: 80px; color: var(--text-secondary); line-height: 1.8;">
        <ul style="list-style: none; padding-left: 0;">
            <li style="margin-bottom: 10px;">✓ <strong>Desarrollo:</strong> Big Data, Integraciones API, Scripts a
                medida.</li>
            <li style="margin-bottom: 10px;">✓ <strong>Consultoría:</strong> Auditoría Técnica, Estrategia de Datos.
            </li>
            <li style="margin-bottom: 10px;">✓ <strong>Formación:</strong> Cursos in-company, Ponencias Técnicas.</li>
        </ul>
    </div>

</div>

<?php include '../../Components/footer.php'; ?>