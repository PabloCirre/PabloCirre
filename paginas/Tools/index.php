<?php
/**
 * Tools - Herramientas y Utilidades
 */

$page_title = "Tools | Herramientas Profesionales - Pablo Cirre";
$page_description = "Herramientas profesionales para desarrolladores y marketers. Kaiju Bulk Email Verifier email verification, análisis de datos, y más.";
$page_keywords = "herramientas desarrollo, verificador email, tools profesionales, Kaiju Bulk Email Verifier, utilidades desarrollador";

include '../../Components/header.php';
?>

<!-- Hero Section Tools -->
<section class="hero-section" style="padding: 80px 0;">
    <h1 class="hero-title" style="font-size: 4rem;">Tools.<br>Herramientas Profesionales.</h1>
    <p class="hero-subtitle">
        Suite de herramientas profesionales para desarrolladores, marketers y empresas. SaaS, APIs y utilidades de alto
        rendimiento.
    </p>
</section>

<!-- Tools Grid -->
<h2 class="section-title">Herramientas Disponibles</h2>

<div class="projects-grid" style="margin-bottom: 120px;">

    <div class="project-card">
        <span class="project-tag">SAAS / API</span>
        <h3 class="project-title">Kaiju Bulk Email Verifier</h3>
        <p class="project-desc">
            API de verificación de email de alto rendimiento. Valida emails en 50ms con 99.8% de precisión. Limpia tus
            listas y mejora deliverability.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Plataforma</span>
                <span class="pm-value">Web/Desk</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Precisión</span>
                <span class="pm-value">99.8%</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Rating</span>
                <span class="pm-value">4.9</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/Tools/KaijuEmailVerifier/" class="project-link">Acceder →</a>
    </div>

</div>

<!-- Features Section -->
<h2 class="section-title">Por Qué Nuestras Tools</h2>

<div class="metrics-grid" style="margin-bottom: 120px;">
    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">PERFORMANCE</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: #444; line-height: 1.6; flex: 1; margin: 20px 0;">
            Optimizadas para velocidad. Respuestas en milisegundos, arquitectura escalable, uptime garantizado.
        </p>
    </div>

    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">RELIABILITY</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: #444; line-height: 1.6; flex: 1; margin: 20px 0;">
            99.9% de uptime, monitoreo 24/7, backups automáticos, soporte técnico dedicado.
        </p>
    </div>

    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">INTEGRATION</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: #444; line-height: 1.6; flex: 1; margin: 20px 0;">
            APIs REST simples, documentación completa, librerías en múltiples lenguajes, webhooks.
        </p>
    </div>

    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">SECURITY</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: #444; line-height: 1.6; flex: 1; margin: 20px 0;">
            Encriptación end-to-end, autenticación OAuth2, rate limiting, protección DDoS.
        </p>
    </div>
</div>

<!-- CTA Section -->
<div class="contact-section">
    <h2 style="font-size: 2rem; margin-bottom: 10px;">¿Necesitas una herramienta custom?</h2>
    <p style="color: #666; margin-bottom: 30px;">Desarrollamos soluciones a medida para tu negocio.</p>

    <div style="max-width: 500px; margin: 0 auto;">
        <a href="<?php echo BASE_URL; ?>/paginas/Services/" class="btn-primary" style="margin-right: 10px;">Ver
            Servicios</a>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="link-secondary">Contactar</a>
    </div>
</div><?php include '../../Components/footer.php'; ?>