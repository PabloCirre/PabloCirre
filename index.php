<!-- CONTROL_TEST_999 -->
<?php
/**
 * Home - Pablo Cirre Portfolio
 */

$page_title = "Pablo Cirre - Big Data, Email Intelligence, Formación & Experiencias en Vídeo";
$page_description = "Pablo Cirre - Experto en Big Data, Email Intelligence, Formación y Experiencias en Vídeo. Granada, España.";
$page_keywords = "Big Data, verificador email, bases de datos empresas, formación desarrollo web, videojuegos indie, Granada, KaijuVerifier, Verne Games";

include 'Components/header.php';
?>

<!-- Hero Section -->
<!-- DEBUG: AM I LIVE? -->
<section class="hero-section">
    <div class="hero-panel panel-1"></div>
    <div class="hero-panel panel-2"></div>

    <h1 class="hero-title">Big Data, Email Intelligence,<br>Formación & Experiencias en Vídeo.</h1>
    <p class="hero-subtitle">
        Construyendo infraestructura digital escalable y experiencias narrativas inmersivas desde Granada,
        España.
    </p>
    <div>
        <a href="<?php echo BASE_URL; ?>/paginas/Projects/" class="btn-primary">Ver Proyectos</a>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="link-secondary">Leer Biografía</a>
    </div>
</section>

<!-- Metrics Grid (60s Console Style) -->
<div class="metrics-grid">

    <!-- Panel 1: BASE DE DATOS (Original) -->
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">BASE_DE_DATOS</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">1.4M</div>
            <div class="metric-desc">Empresas Indexadas</div>
        </div>
        <div class="panel-footer">
            <span>LOC: ES</span>
            <span>UPD: LIVE</span>
        </div>
    </div>

    <!-- Panel 2: ALCANCE (Original) -->
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">ALCANCE</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">15+</div>
            <div class="metric-desc">Países Europeos</div>
        </div>
        <div class="panel-footer">
            <span>SEC: B2B</span>
            <span>GRW: +12%</span>
        </div>
    </div>

    <!-- Panel 3: ESTADO SISTEMA (Original) -->
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">ESTADO_SISTEMA</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="switch-row">
                <div class="switch active"></div>
                <div class="switch active"></div>
                <div class="switch"></div>
            </div>
            <div class="metric-desc" style="margin-top: 15px;">ÓPTIMO</div>
        </div>
        <div class="panel-footer">
            <span>DESDE: 1997</span>
            <span>NIVEL: SENIOR</span>
        </div>
    </div>

    <!-- Panel 4: VERIFICACIÓN con Musical Knobs (MODIFICADO - Hidden Labels) -->
    <div class="data-panel knob-panel">
        <div class="panel-header">
            <span class="panel-label">VERIFICACIÓN</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0;">
                <!-- Knob C -->
                <div class="musical-knob" data-note="C" data-frequency="261.63" title="?">
                    <div class="knob-indicator"></div>
                </div>
                <!-- Knob G -->
                <div class="musical-knob" data-note="G" data-frequency="392.00" title="?">
                    <div class="knob-indicator"></div>
                </div>
                <!-- Knob Am -->
                <div class="musical-knob" data-note="Am" data-frequency="220.00" title="?">
                    <div class="knob-indicator"></div>
                </div>
                <!-- Knob F -->
                <div class="musical-knob" data-note="F" data-frequency="349.23" title="?">
                    <div class="knob-indicator"></div>
                </div>
            </div>
            <div class="metric-desc" style="margin-top: 10px;">VELOCIDAD</div>
        </div>
        <div class="panel-footer">
            <span>RTG: 4.9</span>
            <span>NPS: 72</span>
        </div>
    </div>

</div>

<!-- Projects Section -->
<h2 class="section-title">Proyectos Destacados</h2>

<div class="projects-grid">

    <div class="project-card">
        <span class="project-tag">VIDEOJUEGOS</span>
        <h3 class="project-title">Verne Games</h3>
        <p class="project-desc">
            Director y Productor de "The Shape of Fantasy", un RPG narrativo con pixel art y puzzles complejos.
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
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/VideoGames/" class="project-link">Ver más →</a>
    </div>

    <div class="project-card">
        <span class="project-tag">SAAS / API</span>
        <h3 class="project-title">KaijuVerifier</h3>
        <p class="project-desc">
            API de verificación de email de alto rendimiento diseñada para profesionales del marketing.
            Garantiza higiene de listas y entregabilidad.
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
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/Tools/KaijuEmailVerifier/" class="project-link">Ver más →</a>
    </div>

    <div class="project-card">
        <span class="project-tag">BIG DATA</span>
        <h3 class="project-title">Central Data</h3>
        <p class="project-desc">
            La base de datos B2B líder para el sector turístico en España. Conectando agencias con hoteles a
            través de arquitectura de datos masiva.
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
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/" class="project-link">Ver más →</a>
    </div>

</div>

<!-- About Section -->
<div class="about-section">
    <h2 class="about-title">Una carrera definida por<br>la curiosidad y el código.</h2>
    <div class="about-text">
        <p>
            Mi trayectoria comenzó en 1997 con experimentos en realidad virtual, mucho antes de que el metaverso
            fuera una palabra de moda. Desde entonces, he fundado múltiples empresas, desde "Mensajería Low
            Cost" hasta "Centraldecomunicacion.es".
        </p>
        <p>
            Combino experiencia técnica en Big Data y Arquitectura Web con pasión por la enseñanza y la
            narración. Como profesor en la Cámara de Comercio, he formado a la próxima generación de
            desarrolladores.
        </p>
        <p>
            Hoy divido mi tiempo entre optimizar infraestructura de datos y dirigir videojuegos narrativos en
            Verne Games.
        </p>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="link-secondary">Leer Biografía Completa</a>
    </div>
</div>

<!-- Contact Section -->
<div class="contact-section">
    <h2 style="font-size: 2rem; margin-bottom: 10px;">¿Listo para colaborar?</h2>
    <p style="color: #666; margin-bottom: 30px;">Disponible para consultoría en arquitectura Big Data y Diseño
        de Videojuegos.</p>

    <form class="contact-form" action="<?php echo BASE_URL; ?>/paginas/About-Me/" method="get">
        <input type="email" name="email" placeholder="introduce_tu_email@dominio.com" required>
        <button type="submit" class="btn-primary">Iniciar Contacto</button>
    </form>
</div>

<?php include 'Components/footer.php'; ?>