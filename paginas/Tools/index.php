<?php
/**
 * Tools - Herramientas y Utilidades
 */

$page_title = "Kaiju Tools | Herramientas de Ingeniería SEO - Pablo Cirre";
$page_description = "Kaiju Tools: Suite de ingeniería SEO y automatización. Kaiju Translator, Bulk Email Verifier, y utilidades de alto rendimiento.";
$page_keywords = "kaiju tools, kaiju translator, verificador email, seo engineering, herramientas pablo cirre";

include '../../Components/header.php';
?>

<!-- Hero Section Tools -->
<section class="hero-section" style="padding: 80px 0;">
    <h1 class="hero-title" style="font-size: 4rem;">Kaiju Tools.<br>Ingeniería SEO & Automatización.</h1>
    <p class="hero-subtitle">
        Suite de herramientas de alto rendimiento para desarrolladores y equipos de crecimiento.
        Soluciones "Zero-Rewrite" diseñadas para escalar.
    </p>
</section>

<!-- Tools Grid -->
<h2 class="section-title">Herramientas Disponibles</h2>

<div class="projects-grid" style="margin-bottom: 120px;">

    <!-- Kaiju Translator -->
    <div class="project-card">
        <span class="project-tag" style="background: var(--accent-color); color: white;">NEW / AI</span>
        <h3 class="project-title">Kaiju Translator</h3>
        <p class="project-desc">
            Motor de localización PHP "Zero-Rewrite". Genera espejos SEO físicos usando LLMs (OpenAI/DeepSeek).
            Internacionalización instantánea sin deuda técnica.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Arquitectura</span>
                <span class="pm-value">SEO Mirror</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">AI Engine</span>
                <span class="pm-value">Multi-LLM</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Setup</span>
                <span class="pm-value">5 min</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/Tools/KaijuTranslator/" class="project-link">Explorar Tool →</a>
    </div>

    <!-- Kaiju Bulk Email Verifier -->
    <div class="project-card">
        <span class="project-tag">SAAS / API</span>
        <h3 class="project-title">Kaiju Email Verifier</h3>
        <p class="project-desc">
            API de verificación de email de alto rendimiento. Valida emails en 50ms con 99.8% de precisión.
            Limpia tus listas y mejora deliverability.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Plataforma</span>
                <span class="pm-value">SaaS</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Precisión</span>
                <span class="pm-value">99.8%</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Status</span>
                <span class="pm-value">Live</span>
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
        <p style="font-size: 0.95rem; color: var(--text-color); line-height: 1.6; flex: 1; margin: 20px 0;">
            Optimizadas para velocidad. Respuestas en milisegundos, arquitectura escalable, uptime garantizado.
        </p>
    </div>

    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">RELIABILITY</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); line-height: 1.6; flex: 1; margin: 20px 0;">
            99.9% de uptime, monitoreo 24/7, backups automáticos, soporte técnico dedicado.
        </p>
    </div>

    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">INTEGRATION</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); line-height: 1.6; flex: 1; margin: 20px 0;">
            APIs REST simples, documentación completa, librerías en múltiples lenguajes, webhooks.
        </p>
    </div>

    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">SECURITY</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); line-height: 1.6; flex: 1; margin: 20px 0;">
            Encriptación end-to-end, autenticación OAuth2, rate limiting, protección DDoS.
        </p>
    </div>
</div>

<!-- CTA Section -->
<div class="contact-section">
    <h2 style="font-size: 2rem; margin-bottom: 10px;">¿Necesitas una herramienta custom?</h2>
    <p style="color: var(--text-secondary); margin-bottom: 30px;">Desarrollamos soluciones a medida para tu negocio.</p>

    <div style="max-width: 500px; margin: 0 auto;">
        <a href="<?php echo BASE_URL; ?>/paginas/Services/" class="btn-primary" style="margin-right: 10px;">Ver
            Servicios</a>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="link-secondary">Contactar</a>
    </div>
</div><?php include '../../Components/footer.php'; ?>