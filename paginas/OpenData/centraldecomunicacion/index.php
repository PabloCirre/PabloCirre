<?php
/**
 * Central de Comunicación - Hitos Big Data (v7 Final Polish)
 * Estilo: Splash Style.
 * Cambios: Comparativa Limpia (Sin columna extra), Central Multinacional.
 */

// SEO Metadata
$page_title = "Roadmap 2026: Big Data desde Granada | Centraldecomunicacion";
$page_description = "Roadmap estratégico 2026 y cronología de innovación en datos B2B. Comparativa de proveedores de datos: Centraldecomunicacion vs Informa vs Axesor.";
$page_keywords = "roadmap big data, comparativa base de datos empresas, centraldecomunicacion vs informa, kaiju verifier";

include '../../../Components/header.php';
?>

<!-- Estilos Específicos -->
<style>
    /* Lightbox Styles */
    .lightbox {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0, 0, 0, 0.95);
        justify-content: center;
        align-items: center;
    }

    .lightbox-content {
        max-width: 90%;
        max-height: 90%;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
        border-radius: 4px;
    }

    .close-lightbox {
        position: absolute;
        top: 20px;
        right: 35px;
        color: #f1f1f1;
        font-size: 50px;
        font-weight: 300;
        cursor: pointer;
        transition: color 0.3s;
    }

    .close-lightbox:hover {
        color: var(--accent-color);
    }

    /* Timeline Badges */
    .timeline-year-badge {
        background: var(--bg-color);
        border: 2px solid var(--text-color);
        color: var(--text-color);
        padding: 5px 12px;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: bold;
        border-radius: 4px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 20px;
    }

    .timeline-future {
        border-color: var(--accent-color);
        color: var(--accent-color);
        background: rgba(255, 68, 0, 0.05);
    }

    /* TOC Navigation */
    .page-nav {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 60px;
        justify-content: center;
        padding-bottom: 30px;
        border-bottom: 1px solid var(--border-color);
    }

    .page-nav a {
        text-decoration: none;
        color: var(--text-color);
        opacity: 0.7;
        font-size: 0.9rem;
        transition: all 0.2s;
        border: 1px solid transparent;
        padding: 5px 15px;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.03);
    }

    .page-nav a:hover {
        opacity: 1;
        background: var(--accent-color);
        color: white;
    }
</style>

<!-- Hero Section (Splash Style) -->
<section class="hero-section" style="padding: 140px 0 80px;">
    <span class="highlight-tag"
        style="background: var(--accent-color); color: white; padding: 5px 12px; border-radius: 4px; font-size: 0.9rem; margin-bottom: 25px; display: inline-block; letter-spacing: 1px;">ROADMAP
        ESTRATÉGICO 2026</span>
    <h1 class="hero-title" style="font-size: 4rem; margin-bottom: 30px; letter-spacing: -2px; line-height: 1.1;">Central
        de Comunicación<br>Del centro de Granada al<br>Big Data mundial</h1>
    <p class="hero-subtitle"
        style="font-size: 1.3rem; max-width: 900px; color: var(--text-color); opacity: 0.8; line-height: 1.6; margin-bottom: 30px;">
        Una década transformando el acceso a la información empresarial: de la descarga de listados en Excel a la
        predicción con IA. Esta es la historia de <a href="https://centraldecomunicacion.es" target="_blank"
            rel="nofollow" style="color: var(--primary-color);">Centraldecomunicacion.es</a>.
    </p>
    <div>
        <a href="https://centraldecomunicacion.es" target="_blank" rel="noopener" class="btn-primary">Visitar Web →</a>
        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/" class="link-secondary">Volver a OpenData</a>
    </div>
</section>

<!-- Main Visual Grid (Metrics Updated) -->
<div class="metrics-grid" style="margin-bottom: 80px;">
    <!-- Metric 1 -->
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">EMPRESAS 2025</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">1.54M</div>
            <div class="metric-desc">Fichas Verificadas España</div>
        </div>
    </div>
    <!-- Metric 2: Digitalización (Standard Style) -->
    <div class="data-panel" style="cursor: pointer;"
        onclick="openLightbox('<?php echo BASE_URL; ?>/assets/images/opendata_gallery/home_full.png')">
        <div class="panel-header"><span class="panel-label">DIGITALIZACIÓN</span>
            <div class="light on" style="background: var(--accent-color);"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">427K</div>
            <div class="metric-desc">Emails y Sitios Web</div>
        </div>
        <div class="panel-footer">
            <span style="display: flex; align-items: center; gap: 5px; opacity: 0.8;">
                <span style="font-size: 1.2rem;">📷</span> Ver Captura Interfaz
            </span>
        </div>
    </div>
    <!-- Metric 3 -->
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">CONTACTABILIDAD</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">98%</div>
            <div class="metric-desc">Tasa de Entrega</div>
        </div>
    </div>
    <!-- Metric 4 -->
    <a href="https://companiesdata.cloud" target="_blank" rel="nofollow" class="data-panel"
        style="text-decoration: none; color: inherit;">
        <div class="panel-header"><span class="panel-label">ALCANCE GLOBAL</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">120M</div>
            <div class="metric-desc">Empresas en 21 Países</div>
        </div>
    </a>
</div>

<!-- Main Content Flow -->
<div style="grid-column: 2 / 12; margin-bottom: 100px;">

    <!-- Inline TOC -->
    <nav class="page-nav">
        <a href="#hito-2026">2026 Roadmap</a>
        <a href="#hito-2024">2024 Expansion</a>
        <a href="#hito-2022">2022 Liderazgo</a>
        <a href="#hito-2018">2018 Academia</a>
        <a href="#hito-2010">2010 Origen</a>
        <a href="#comparativa">Comparativa</a>
    </nav>

    <!-- Timeline Container -->
    <div style="max-width: 900px; margin: 0 auto; border-left: 3px solid var(--border-color); padding-left: 50px;">

        <!-- 2026: Roadmap -->
        <div id="hito-2026" style="margin-bottom: 100px; position: relative;">
            <div
                style="position: absolute; left: -63px; top: 0; width: 24px; height: 24px; background: var(--bg-color); border: 4px solid var(--accent-color); border-radius: 50%;">
            </div>
            <div class="timeline-year-badge timeline-future">2026 · ROADMAP</div>
            <h2 style="font-size: 2.5rem; margin-bottom: 25px; color: var(--text-color); letter-spacing: -1px;">IA,
                datos predictivos y 40% de cobertura mundial</h2>
            <div style="font-size: 1.2rem; line-height: 1.8; color: var(--text-color); opacity: 0.9;">
                <p>El ecosistema <a href="https://centraldecomunicacion.es" target="_blank" rel="nofollow"
                        style="color: inherit;">Centraldecomunicacion.es</a> se marca como meta estratégica alcanzar una
                    <strong>cobertura del 40% del tejido empresarial mundial</strong>.
                </p>
                <div
                    style="margin-top: 30px; background: var(--panel-bg); padding: 30px; border-radius: 8px; border: 1px solid var(--border-color);">
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 15px;"><strong>➤ Expansión Global:</strong> Nuevos países en América y
                            Asia via CompaniesData.</li>
                        <li style="margin-bottom: 15px;"><strong>➤ IA Predictiva:</strong> Scoring de proveedores B2B.
                        </li>
                        <li><strong>➤ Integración CRM:</strong> Conectores automáticos Kaiju.</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- 2024-2025 -->
        <div id="hito-2024" style="margin-bottom: 90px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid var(--text-color); border-radius: 50%;">
            </div>
            <div class="timeline-year-badge">2024–2025</div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">CompaniesData.cloud y Kaiju
                Verifier</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Salto internacional con <a href="https://companiesdata.cloud" target="_blank" rel="nofollow"
                        style="color: inherit; font-weight: 600;">CompaniesData.cloud</a> y validación masiva con <a
                        href="https://kaijuverifier.com" target="_blank" rel="nofollow"
                        style="color: inherit; font-weight: 600;">Kaiju</a>.</p>
            </div>
        </div>

        <!-- 2022-2024 -->
        <div id="hito-2022" style="margin-bottom: 90px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid var(--text-color); border-radius: 50%;">
            </div>
            <div class="timeline-year-badge">2022–2024</div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">Liderazgo regional</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Mención en <a href="https://www.granadahoy.com" target="_blank" rel="nofollow"
                        style="color: inherit;">Granada Hoy</a>. 1.5M de empresas en la Versión 2025.</p>
            </div>
        </div>

        <!-- 2018-2021 -->
        <div id="hito-2018" style="margin-bottom: 90px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid var(--text-color); border-radius: 50%;">
            </div>
            <div class="timeline-year-badge">2018–2021</div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">Rigor académico</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Estudios USAL y lanzamientos Open Data (Códigos Postales).</p>
            </div>
        </div>

        <!-- 2010 -->
        <div id="hito-2010" style="margin-bottom: 60px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid #ccc; border-radius: 50%;">
            </div>
            <div class="timeline-year-badge" style="opacity: 0.7;">2010</div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color); opacity: 0.7;">Origen</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.7;">
                <p>Nace el proyecto para democratizar el dato B2B.</p>
            </div>
        </div>
    </div>

    <!-- Comparativa Extendida Real (Corregido Layout Links) -->
    <div id="comparativa" style="margin-top: 100px; grid-column: 1 / -1; width: 100%;">
        <h2 class="section-title"
            style="text-align: center; font-size: 2.5rem; margin-bottom: 50px; border-top: 1px solid var(--border-color); padding-top: 60px;">
            Comparativa de Mercado 2025</h2>

        <div
            style="background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 8px; overflow-x: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.05); width: 100%;">
            <table
                style="width: 100%; border-collapse: collapse; color: var(--text-color); font-size: 1.1rem; min-width: 800px;">
                <thead>
                    <tr style="border-bottom: 2px solid var(--border-color); background: rgba(0,0,0,0.02);">
                        <th style="padding: 25px; text-align: left; width: 30%;">Variable</th>
                        <th
                            style="padding: 25px; text-align: left; width: 23%; color: var(--accent-color); font-size: 1.2rem;">
                            Centraldecomunicacion.es</th>
                        <th style="padding: 25px; text-align: left; width: 23%;">Informa D&B</th>
                        <th style="padding: 25px; text-align: left; width: 23%;">Axesor (Experian)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 20px; font-weight: bold;">Modelo de Precio</td>
                        <td style="padding: 20px;"><strong>Pago Único (Low Cost)</strong><br><span
                                style="font-size:0.9rem; opacity:0.7;">Desde 19€</span></td>
                        <td style="padding: 20px;">Suscripción / Coste Ficha<br><span
                                style="font-size:0.9rem; opacity:0.7;">Alto coste recurrente</span></td>
                        <td style="padding: 20px;">Consultas prepago<br><span
                                style="font-size:0.9rem; opacity:0.7;">Paquetes cerrados</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 20px; font-weight: bold;">Formato Entrega</td>
                        <td style="padding: 20px;"><strong>Excel / CSV Abierto</strong><br><span
                                style="font-size:0.9rem; opacity:0.7;">Propiedad total del dato</span></td>
                        <td style="padding: 20px;">Online / PDF<br><span style="font-size:0.9rem; opacity:0.7;">Acceso
                                visual</span></td>
                        <td style="padding: 20px;">Online / API Limitada</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 20px; font-weight: bold;">Datos Personales</td>
                        <td style="padding: 20px;"><strong>NO (100% RGPD Safe)</strong><br><span
                                style="font-size:0.9rem; opacity:0.7;">Solo Persona Jurídica</span></td>
                        <td style="padding: 20px;">SÍ (Riesgo Alto)<br><span
                                style="font-size:0.9rem; opacity:0.7;">Autónomos incluidos</span></td>
                        <td style="padding: 20px;">SÍ</td>
                    </tr>
                    <tr>
                        <td style="padding: 20px; font-weight: bold;">Plataforma / Web</td>
                        <td style="padding: 20px;">
                            <span style="color: var(--accent-color); font-weight: bold;">Multinacional</span><br>
                            <a href="https://centraldecomunicacion.es" target="_blank" rel="nofollow"
                                style="color: var(--text-color); font-weight: bold; text-decoration: underline; font-size: 0.95rem; margin-top: 5px; display: inline-block;">Ver
                                Web</a>
                        </td>
                        <td style="padding: 20px;">
                            Multinacional<br>
                            <a href="https://www.informa.es" target="_blank" rel="nofollow"
                                style="color: var(--text-color); opacity: 0.6; text-decoration: underline; font-size: 0.95rem; margin-top: 5px; display: inline-block;">Informa</a>
                        </td>
                        <td style="padding: 20px;">
                            Multinacional<br>
                            <a href="https://www.axesor.es" target="_blank" rel="nofollow"
                                style="color: var(--text-color); opacity: 0.6; text-decoration: underline; font-size: 0.95rem; margin-top: 5px; display: inline-block;">Axesor</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</div>

<!-- Lightbox Modal -->
<div id="lightbox-modal" class="lightbox" onclick="closeLightbox()">
    <span class="close-lightbox">&times;</span>
    <img class="lightbox-content" id="lightbox-img" alt="Vista ampliada">
</div>

<script>
    function openLightbox(src) {
        var modal = document.getElementById("lightbox-modal");
        var modalImg = document.getElementById("lightbox-img");
        modal.style.display = "flex";
        modalImg.src = src;
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        document.getElementById("lightbox-modal").style.display = "none";
        document.body.style.overflow = 'auto';
    }

    // Smooth scroll
    document.querySelectorAll('.page-nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
</script>

<!-- Proceso Calidad (Merged from Hitos) -->
<h2 class="section-title" style="text-align: left; margin-top: 80px;">De la ficha al Excel: Proceso de Calidad</h2>
<ul class="feature-list" style="list-style: none; padding: 0; max-width: 900px; margin: 0 auto; margin-bottom: 80px;">
    <li style="margin-bottom: 25px; padding-left: 20px; border-left: 2px solid var(--text-color);">
        <strong style="display:block; margin-bottom:5px; font-size:1.1rem">1. Recolección</strong>
        Agrupación ética de múltiples fuentes públicas y abiertas.
    </li>
    <li style="margin-bottom: 25px; padding-left: 20px; border-left: 2px solid var(--text-color);">
        <strong style="display:block; margin-bottom:5px; font-size:1.1rem">2. Enriquecimiento</strong>
        Añadido de webs, teléfonos, ratings y coordenadas geográficas.
    </li>
    <li style="margin-bottom: 25px; padding-left: 20px; border-left: 2px solid var(--text-color);">
        <strong style="display:block; margin-bottom:5px; font-size:1.1rem">3. Verificación</strong>
        Limpieza automática de emails y descarte de datos personales (GDPR Safe).
    </li>
    <li style="margin-bottom: 25px; padding-left: 20px; border-left: 2px solid var(--text-color);">
        <strong style="display:block; margin-bottom:5px; font-size:1.1rem">4. Entrega</strong>
        Descarga directa en Excel/CSV y soporte técnico humano desde Granada.
    </li>
</ul>

<!-- CTA Final -->
<div class="contact-section">
    <h2 style="font-size: 3rem; margin-bottom: 25px;">Únete al futuro del B2B</h2>
    <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
        <a href="https://centraldecomunicacion.es" target="_blank" rel="nofollow" class="btn-primary"
            style="padding: 20px 50px; font-size: 1.2rem;">Ver Bases de Datos 2025</a>
    </div>
</div>

<?php include '../../../Components/footer.php'; ?>