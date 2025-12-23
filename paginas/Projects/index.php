<?php
/**
 * Projects - Portfolio y Casos de Éxito
 */

$page_title = "Proyectos Big Data & SaaS - Pablo Cirre";
$page_description = "Portfolio de proyectos Big Data, SaaS y Videojuegos. Casos de éxito con 1.4M empresas, KaijuVerifier y Verne Games. Granada.";
$page_keywords = "proyectos big data, casos de éxito big data, portfolio desarrollador web, proyectos verificación email, desarrollo videojuegos indie";

include '../../Components/header.php';
?>

<!-- Hero Section Projects -->
<section class="hero-section" style="padding: 80px 0;">
    <h1 class="hero-title" style="font-size: 4rem;">Portfolio &<br>Casos de Éxito.</h1>
    <p class="hero-subtitle">
        Proyectos de Big Data, SaaS y Videojuegos que han impactado a más de 12,000 clientes y procesado 1.4M de
        registros empresariales.
    </p>
</section>

<!-- Projects Grid -->
<h2 class="section-title">Proyectos Destacados</h2>

<div class="projects-grid">

    <!-- Project 1: Central Data -->
    <div class="project-card">
        <span class="project-tag">BIG DATA</span>
        <h3 class="project-title">Centraldecomunicacion.es</h3>
        <p class="project-desc">
            La base de datos B2B líder para el sector turístico en España. Conectando agencias con hoteles a través de
            arquitectura de datos masiva.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Registros</span>
                <span class="pm-value">1.4M</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Sector</span>
                <span class="pm-value">Turismo</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Países</span>
                <span class="pm-value">15+</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/" class="project-link">Ver más →</a>
    </div>

    <!-- Project 2: KaijuVerifier -->
    <div class="project-card">
        <span class="project-tag">SAAS / API</span>
        <h3 class="project-title">KaijuVerifier</h3>
        <p class="project-desc">
            API de verificación de email de alto rendimiento diseñada para profesionales del marketing. Garantiza
            higiene de listas y entregabilidad.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Velocidad</span>
                <span class="pm-value">50ms</span>
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
        <a href="<?php echo BASE_URL; ?>/Tools/verificador-email/" class="project-link">Ver más →</a>
    </div>

    <!-- Project 3: Verne Games -->
    <div class="project-card">
        <span class="project-tag">VIDEOJUEGOS</span>
        <h3 class="project-title">Verne Games</h3>
        <p class="project-desc">
            Director y Productor de "The Shape of Fantasy", un RPG narrativo con pixel art y puzzles complejos
            desarrollado en Unity.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Plataforma</span>
                <span class="pm-value">Steam</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Motor</span>
                <span class="pm-value">Unity</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Género</span>
                <span class="pm-value">RPG</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/VideoGames/" class="project-link">Ver más →</a>
    </div>

    <!-- Project 4: CompaniesData.cloud -->
    <div class="project-card">
        <span class="project-tag">BIG DATA</span>
        <h3 class="project-title">CompaniesData.cloud</h3>
        <p class="project-desc">
            Servicio de datos empresariales en la nube con API REST. Consultas en tiempo real sobre empresas de
            múltiples países europeos.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">API Calls</span>
                <span class="pm-value">10K/día</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Uptime</span>
                <span class="pm-value">99.9%</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Clientes</span>
                <span class="pm-value">50+</span>
            </div>
        </div>
    </div>

    <!-- Project 5: Formación Cámara Comercio -->
    <div class="project-card">
        <span class="project-tag">FORMACIÓN</span>
        <h3 class="project-title">Formación Cámara de Comercio</h3>
        <p class="project-desc">
            Profesor de desarrollo web en la Cámara de Comercio de Granada. Más de 500 alumnos formados en tecnologías
            web modernas.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Alumnos</span>
                <span class="pm-value">500+</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Cursos</span>
                <span class="pm-value">20+</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Rating</span>
                <span class="pm-value">4.8</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/Experiences/" class="project-link">Ver más →</a>
    </div>

    <!-- Project 6: Servidor3000 -->
    <div class="project-card">
        <span class="project-tag">HISTÓRICO</span>
        <h3 class="project-title">Servidor3000</h3>
        <p class="project-desc">
            Uno de los primeros proyectos (2000). Servidor de hosting y soluciones web que atendió a cientos de pequeñas
            empresas en Granada.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Año</span>
                <span class="pm-value">2000</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Clientes</span>
                <span class="pm-value">300+</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Años</span>
                <span class="pm-value">10+</span>
            </div>
        </div>
    </div>

</div>

<!-- Testimonials Section -->
<h2 class="section-title" style="margin-top: 120px;">Lo Que Dicen los Clientes</h2>

<div class="metrics-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 120px;">
    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">CLIENTE_A</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); opacity: 0.85; line-height: 1.6; flex: 1;">
            "La base de datos de Centraldecomunicacion.es transformó nuestra operación. Acceso instantáneo a 1.4M
            empresas con datos actualizados."
        </p>
        <div class="panel-footer">
            <span>SECTOR: TURISMO</span>
            <span>★★★★★</span>
        </div>
    </div>

    <div class="data-panel" style="min-height: auto;">
        <div class="panel-header">
            <span class="panel-label">CLIENTE_B</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); opacity: 0.85; line-height: 1.6; flex: 1;">
            "KaijuVerifier redujo nuestro bounce rate del 15% al 2%. La API es rapidísima y la precisión es increíble."
        </p>
        <div class="panel-footer">
            <span>SECTOR: MARKETING</span>
            <span>★★★★★</span>
        </div>
    </div>
</div>

<?php include '../../Components/footer.php'; ?>