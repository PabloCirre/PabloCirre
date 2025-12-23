<?php
/**
 * Services - Servicios y Consultoría
 */

$page_title = "Servicios Consultoría Big Data | Desarrollo Soluciones - Pablo Cirre";
$page_description = "Servicios de consultoría Big Data, desarrollo de soluciones, verificación email, videojuegos. Arquitectura de datos. Granada, España.";
$page_keywords = "servicios consultoría big data, consultor big data españa, desarrollo soluciones datos, servicios verificación email, consultor big data granada";

include '../../Components/header.php';
?>

<!-- Hero Section Services -->
<section class="hero-section" style="padding: 80px 0;">
    <h1 class="hero-title" style="font-size: 4rem;">Servicios &<br>Consultoría Técnica.</h1>
    <p class="hero-subtitle">
        Soluciones personalizadas en Big Data, verificación de email, desarrollo web y videojuegos. 20+ años de
        experiencia al servicio de tu proyecto.
    </p>
    <div>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="btn-primary">Solicitar Consultoría</a>
        <a href="#planes" class="link-secondary">Ver Planes</a>
    </div>
</section>

<!-- Services Grid -->
<h2 class="section-title">Servicios Principales</h2>

<div class="projects-grid" style="margin-bottom: 120px;">

    <div class="project-card">
        <span class="project-tag">BIG DATA</span>
        <h3 class="project-title">Consultoría Big Data</h3>
        <p class="project-desc">
            Diseño de arquitectura de datos, implementación de pipelines ETL, optimización de bases de datos, análisis
            de grandes volúmenes de información.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Desde</span>
                <span class="pm-value">2.500€</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Plazo</span>
                <span class="pm-value">2-4 sem</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="project-link">Consultar →</a>
    </div>

    <div class="project-card">
        <span class="project-tag">EMAIL</span>
        <h3 class="project-title">Implementación Email Verifier</h3>
        <p class="project-desc">
            Integración de KaijuVerifier API en tus sistemas. Configuración personalizada, validación de listas, mejora
            de deliverability.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Desde</span>
                <span class="pm-value">1.000€</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Plazo</span>
                <span class="pm-value">1-2 sem</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/Tools/KaijuEmailVerifier/" class="project-link">Ver Tool →</a>
    </div>

    <div class="project-card">
        <span class="project-tag">WEB DEVELOPMENT</span>
        <h3 class="project-title">Desarrollo WordPress</h3>
        <p class="project-desc">
            Themes y plugins personalizados, optimización de performance, seguridad, integraciones WooCommerce,
            migraciones, mantenimiento.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Desde</span>
                <span class="pm-value">1.500€</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Plazo</span>
                <span class="pm-value">2-3 sem</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="project-link">Consultar →</a>
    </div>

    <div class="project-card">
        <span class="project-tag">VIDEOJUEGOS</span>
        <h3 class="project-title">Desarrollo de Videojuegos</h3>
        <p class="project-desc">
            Desarrollo completo en Unity, desde concept hasta publicación. Diseño de gameplay, narrativa, pixel art,
            integración Steam.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Desde</span>
                <span class="pm-value">5.000€</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Plazo</span>
                <span class="pm-value">3-6 meses</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/VideoGames/" class="project-link">Ver Proyectos →</a>
    </div>

    <div class="project-card">
        <span class="project-tag">FORMACIÓN</span>
        <h3 class="project-title">Formación Corporativa</h3>
        <p class="project-desc">
            Cursos in-company personalizados. Desarrollo web, Big Data, marketing digital. Grupos reducidos, contenido
            adaptado.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Desde</span>
                <span class="pm-value">800€/día</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Grupo</span>
                <span class="pm-value">Max 15</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/Experiences/" class="project-link">Ver Cursos →</a>
    </div>

    <div class="project-card">
        <span class="project-tag">SEO / MARKETING</span>
        <h3 class="project-title">Consultoría SEO</h3>
        <p class="project-desc">
            Auditoría técnica, estrategia de contenido, link building, optimización on-page, análisis de competencia,
            reporting mensual.
        </p>
        <div class="project-metrics">
            <div class="p-metric">
                <span class="pm-label">Desde</span>
                <span class="pm-value">600€/mes</span>
            </div>
            <div class="p-metric">
                <span class="pm-label">Mínimo</span>
                <span class="pm-value">3 meses</span>
            </div>
        </div>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="project-link">Consultar →</a>
    </div>

</div>

<!-- Planes Section -->
<h2 class="section-title" id="planes">Planes de Servicio</h2>

<div class="metrics-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 120px;">
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">BASIC</span>
            <div class="light on"></div>
        </div>
        <div style="flex: 1; padding: 20px 0;">
            <div class="metric-value" style="font-size: 2rem;">500€</div>
            <div class="metric-desc">/ mes</div>
            <ul style="margin-top: 20px; font-size: 0.9rem; color: var(--text-secondary); list-style: none;">
                <li style="margin-bottom: 8px;">✓ 10 horas consultoría/mes</li>
                <li style="margin-bottom: 8px;">✓ Email y chat support</li>
                <li style="margin-bottom: 8px;">✓ Respuesta &lt; 48h</li>
                <li style="margin-bottom: 8px;">✓ Documentación incluida</li>
            </ul>
        </div>
        <div class="panel-footer">
            <span>IDEAL: PYMES</span>
        </div>
    </div>

    <div class="data-panel" style="border-color: var(--accent-color); border-width: 2px;">
        <div class="panel-header">
            <span class="panel-label">PRO</span>
            <div class="light on"></div>
        </div>
        <div style="flex: 1; padding: 20px 0;">
            <div class="metric-value" style="font-size: 2rem; color: var(--accent-color);">1.200€</div>
            <div class="metric-desc">/ mes</div>
            <ul style="margin-top: 20px; font-size: 0.9rem; color: var(--text-secondary); list-style: none;">
                <li style="margin-bottom: 8px;">✓ 25 horas consultoría/mes</li>
                <li style="margin-bottom: 8px;">✓ Soporte prioritario</li>
                <li style="margin-bottom: 8px;">✓ Respuesta &lt; 24h</li>
                <li style="margin-bottom: 8px;">✓ Videollamadas incluidas</li>
                <li style="margin-bottom: 8px;">✓ Reporting mensual</li>
            </ul>
        </div>
        <div class="panel-footer" style="background: var(--accent-color); color: white;">
            <span>MÁS POPULAR</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">ENTERPRISE</span>
            <div class="light on"></div>
        </div>
        <div style="flex: 1; padding: 20px 0;">
            <div class="metric-value" style="font-size: 2rem;">Custom</div>
            <div class="metric-desc">contactar</div>
            <ul style="margin-top: 20px; font-size: 0.9rem; color: var(--text-secondary); list-style: none;">
                <li style="margin-bottom: 8px;">✓ Horas ilimitadas</li>
                <li style="margin-bottom: 8px;">✓ Soporte 24/7</li>
                <li style="margin-bottom: 8px;">✓ Respuesta &lt; 2h</li>
                <li style="margin-bottom: 8px;">✓ Equipo dedicado</li>
                <li style="margin-bottom: 8px;">✓ SLA personalizado</li>
                <li style="margin-bottom: 8px;">✓ Desarrollo prioritario</li>
            </ul>
        </div>
        <div class="panel-footer">
            <span>IDEAL: CORP</span>
        </div>
    </div>
</div>

<!-- Process -->
<div class="about-section" style="margin-bottom: 120px;">
    <h2 class="about-title">Proceso de<br>Trabajo</h2>
    <div class="about-text">
        <p>
            <strong>1. Descubrimiento:</strong> Llamada inicial para entender tus necesidades, objetivos y
            restricciones. Análisis de situación actual y definición de alcance.
        </p>
        <p>
            <strong>2. Propuesta:</strong> Presupuesto detallado con hitos, entregables y timings. Plan de proyecto con
            metodología ágil y sprints de 2 semanas.
        </p>
        <p>
            <strong>3. Ejecución:</strong> Desarrollo iterativo con demos regulares. Comunicación constante vía
            Slack/email. Ajustes basados en feedback continuo.
        </p>
        <p>
            <strong>4. Entrega y Soporte:</strong> Documentación completa, transferencia de conocimiento. Soporte
            post-lanzamiento incluido según plan.
        </p>
    </div>
</div>

<!-- CTA -->
<div class="contact-section">
    <h2 style="font-size: 2rem; margin-bottom: 10px;">¿Listo para empezar tu proyecto?</h2>
    <p style="color: var(--text-secondary); margin-bottom: 30px;">Agenda una consultoría inicial gratuita de 30 minutos.
    </p>

    <form class="contact-form" action="<?php echo BASE_URL; ?>/paginas/About-Me/" method="get">
        <input type="email" name="email" placeholder="tu_email@empresa.com" required>
        <button type="submit" class="btn-primary">Agendar Consultoría</button>
    </form>
</div>

<?php include '../../Components/footer.php'; ?>