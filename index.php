<?php
/**
 * Home - Pablo Cirre Portfolio
 */

$page_title = "Pablo Cirre | Big Data, Formación & Videojuegos - Granada";
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
            Mi trayectoria profesional comenzó oficialmente en 1997, experimentando con las primeras versiones de
            realidad virtual y VRML, mucho antes de que el concepto de metaverso se convirtiera en una tendencia global.
            Esta fascinación temprana por la tecnología inmersiva sentó las bases de mi carrera. Desde entonces, he
            fundado y dirigido múltiples empresas tecnológicas, destacando proyectos como "Mensajería Low Cost", que
            revolucionó la logística para e-commerce, y "Centraldecomunicacion.es", que se ha consolidado como un
            referente en datos B2B.
        </p>
        <p>
            A lo largo de más de dos décadas, he combinado mi experiencia técnica en Big Data, Arquitectura Web y
            Automatización de Procesos con una profunda pasión por la enseñanza y la comunicación. Como profesor titular
            en programas de la Cámara de Comercio de Granada y otras instituciones, he tenido el privilegio de formar y
            mentorizar a la próxima generación de desarrolladores y profesionales del marketing digital, compartiendo no
            solo código, sino una visión estratégica del negocio digital.
        </p>
        <p>
            Actualmente, divido mi tiempo profesional entre dos grandes pasiones que convergen en la tecnología: la
            optimización de infraestructuras de datos masivos (Big Data) para inteligencia de negocio, y la dirección
            creativa y técnica de videojuegos narrativos en Verne Games. En Verne Games, exploramos nuevas formas de
            contar historias a través de mecánicas de juego innovadoras, como en nuestro título "The Shape of Fantasy".
        </p>
        <p>
            Esta dualidad entre la lógica estructurada de los datos y la creatividad narrativa de los videojuegos define
            mi enfoque: técnico, riguroso, pero siempre centrado en la experiencia del usuario final.
        </p>
        <p>
            En un entorno digital saturado, la diferencia entre un producto funcional y uno memorable reside en los
            detalles. Ya sea optimizando una consulta SQL para que se ejecute en milisegundos o diseñando la curva de
            aprendizaje de un videojuego, mi compromiso es con la excelencia técnica y estética. Creo firmemente que la
            tecnología debe ser invisible, sirviendo como un facilitador transparente para las necesidades humanas, y
            este principio guía cada línea de código que escribo y cada sistema que diseño.
        </p>
        <p>
            La formación continua es otro pilar fundamental de mi filosofía. En un sector donde las herramientas cambian
            cada seis meses, mantenerse relevante requiere una curiosidad insaciable. Por ello, no solo aplico las
            últimas tecnologías en mis proyectos, sino que dedico gran parte de mi tiempo a investigar, probar y
            documentar nuevos frameworks y metodologías en mi sección de 'Knowledge' y 'Labs', contribuyendo así al
            conocimiento colectivo de la comunidad de desarrolladores.
        </p>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="link-secondary">Leer Biografía Completa</a>
    </div>
</div>

<!-- Contact Section -->
<div class="contact-section">
    <h2 style="font-size: 2rem; margin-bottom: 10px;">¿Listo para colaborar?</h2>
    <p style="color: var(--text-secondary); margin-bottom: 30px;">Disponible para consultoría en arquitectura Big Data y
        Diseño
        de Videojuegos. Cuéntame tu proyecto.</p>

    <form class="contact-form" action="<?php echo BASE_URL; ?>/paginas/About-Me/" method="get">
        <label for="contact-email" class="sr-only">Tu Email</label>
        <input type="email" id="contact-email" name="email" placeholder="introduce_tu_email@dominio.com"
            aria-label="Tu dirección de correo electrónico" required>
        <button type="submit" class="btn-primary">Iniciar Contacto</button>
    </form>
</div>

<?php include 'Components/footer.php'; ?>