<?php
/**
 * Central Enterprises - Unified API (BETA)
 */

$page_title = "Central Enterprises | Unified API Beta - Pablo Cirre";
$page_description = "central.enterprises - Unified Enterprise API for accessing all business databases from a single endpoint. GraphQL and REST API in development.";
$page_keywords = "central enterprises, unified api, business data api, graphql api, enterprise data";

include '../../../Components/header.php';
?>

<!-- Hero Section -->
<section class="hero-section" style="padding: 80px 0;">
    <h1 class="hero-title" style="font-size: 4rem;">Central Enterprises<br>Unified API <span
            style="background: linear-gradient(135deg, #9945ff, #6b3fa0); color: #fff; padding: 5px 15px; font-size: 1.5rem; border-radius: 8px; vertical-align: middle;">BETA</span>
    </h1>
    <p class="hero-subtitle">
        API unificada para acceder a todas las bases de datos empresariales desde un solo endpoint. GraphQL y REST API
        en desarrollo.
    </p>
    <div>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="btn-primary">Solicitar Early Access</a>
        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/" class="link-secondary">Volver a OpenData</a>
    </div>
</section>

<!-- Metrics Console -->
<div class="metrics-grid" style="margin-bottom: 120px;">
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">API_TYPE</span>
            <div class="light" style="background: #9945ff; box-shadow: 0 0 10px #9945ff;"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">Unified</div>
            <div class="metric-desc">Single Endpoint</div>
        </div>
        <div class="panel-footer">
            <span>REST: YES</span>
            <span>GQL: YES</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">SOURCES</span>
            <div class="light" style="background: #9945ff; box-shadow: 0 0 10px #9945ff;"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">3</div>
            <div class="metric-desc">Data Sources</div>
        </div>
        <div class="panel-footer">
            <span>ES + EU + UK</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">AUTH</span>
            <div class="light" style="background: #9945ff; box-shadow: 0 0 10px #9945ff;"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">OAuth</div>
            <div class="metric-desc">2.0 Protocol</div>
        </div>
        <div class="panel-footer">
            <span>SECURE: YES</span>
            <span>JWT: OK</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">STATUS</span>
            <div class="light" style="background: #9945ff; box-shadow: 0 0 10px #9945ff;"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">Dev</div>
            <div class="metric-desc">In Development</div>
        </div>
        <div class="panel-footer">
            <span>PHASE: 2</span>
            <span>ETA: Q2 2025</span>
        </div>
    </div>
</div>

<!-- About Section -->
<div class="about-section" style="margin-bottom: 120px;">
    <h2 class="about-title">Un endpoint.<br>Toda la data.</h2>
    <div class="about-text">
        <p>
            <strong>Central Enterprises</strong> unifica el acceso a centraldecomunicacion.es, companiesdata.cloud y
            ukbusinessdatabases.club en una única API moderna.
        </p>
        <p>
            Consulta millones de empresas con una sola integración. GraphQL para queries flexibles, REST para
            compatibilidad total.
        </p>
        <p>
            <strong>Tecnologías:</strong> REST API, GraphQL, OAuth 2.0, JWT, Webhooks, JSON/CSV export.
        </p>
    </div>
</div>

<!-- Features Preview -->
<h2 class="section-title">Características Planificadas</h2>

<div class="projects-grid" style="margin-bottom: 120px;">

    <div class="project-card">
        <span class="project-tag" style="background: #9945ff;">COMING SOON</span>
        <h3 class="project-title">Unified REST API</h3>
        <p class="project-desc">
            Un solo endpoint REST para consultar empresas de cualquier país o fuente de datos.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Endpoint</span>
                <span class="pm-value">1</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Sources</span>
                <span class="pm-value">3</span>
            </div>
        </div>
    </div>

    <div class="project-card">
        <span class="project-tag" style="background: #9945ff;">COMING SOON</span>
        <h3 class="project-title">GraphQL Support</h3>
        <p class="project-desc">
            Consultas flexibles con GraphQL. Obtén exactamente los campos que necesitas.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Type</span>
                <span class="pm-value">GraphQL</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Flexible</span>
                <span class="pm-value">Yes</span>
            </div>
        </div>
    </div>

    <div class="project-card">
        <span class="project-tag" style="background: #9945ff;">COMING SOON</span>
        <h3 class="project-title">Real-time Sync</h3>
        <p class="project-desc">
            Sincronización en tiempo real entre todas las fuentes de datos.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Sync</span>
                <span class="pm-value">Real-time</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Webhooks</span>
                <span class="pm-value">Yes</span>
            </div>
        </div>
    </div>

</div>

<!-- Roadmap as data panels -->
<h2 class="section-title">Roadmap</h2>

<div class="metrics-grid" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 120px;">
    <div class="data-panel" style="border-color: var(--indicator-color);">
        <div class="panel-header">
            <span class="panel-label">FASE_1</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value" style="font-size: 1.5rem;">✓</div>
            <div class="metric-desc">Arquitectura</div>
        </div>
        <div class="panel-footer">
            <span>STATUS: DONE</span>
        </div>
    </div>

    <div class="data-panel" style="border-color: #9945ff; border-width: 2px;">
        <div class="panel-header">
            <span class="panel-label">FASE_2</span>
            <div class="light" style="background: #9945ff; box-shadow: 0 0 10px #9945ff;"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value" style="font-size: 1.5rem;">→</div>
            <div class="metric-desc">Core API</div>
        </div>
        <div class="panel-footer">
            <span>STATUS: IN PROGRESS</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">FASE_3</span>
            <div class="light"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value" style="font-size: 1.5rem;">3</div>
            <div class="metric-desc">GraphQL</div>
        </div>
        <div class="panel-footer">
            <span>ETA: Q1 2025</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">FASE_4</span>
            <div class="light"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value" style="font-size: 1.5rem;">4</div>
            <div class="metric-desc">Public Beta</div>
        </div>
        <div class="panel-footer">
            <span>ETA: Q2 2025</span>
        </div>
    </div>
</div>

<!-- CTA Section -->
<div class="contact-section">
    <h2 style="font-size: 2rem; margin-bottom: 10px;">Únete a la Waitlist</h2>
    <p style="color: var(--text-secondary); margin-bottom: 30px;">Sé el primero en acceder cuando lancemos la beta
        pública.</p>

    <div style="max-width: 500px; margin: 0 auto;">
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="btn-primary">Contactar para Early Access</a>
    </div>
</div>

<?php include '../../../Components/footer.php'; ?>