<?php
/**
 * OpenData - Big Data & Bases de Datos Empresas
 */

$page_title = "OpenData Empresas España: 1.4M Datos B2B - Pablo Cirre";
$page_description = "Base de datos de 1.4 millones de empresas en España. OpenData empresarial, sector turismo B2B, 15+ países europeos. Centraldecomunicacion.es";
$page_keywords = "base de datos empresas españa, opendata empresas, datos abiertos empresariales, 1.4 millones empresas, base datos turismo b2b, centraldecomunicacion";

include '../../Components/header.php';
?>

<!-- Hero Section OpenData -->
<section class="hero-section" style="padding: 80px 0;">
    <h1 class="hero-title" style="font-size: 4rem;">1.4M Empresas.<br>OpenData Empresarial.</h1>
    <p class="hero-subtitle">
        La mayor base de datos empresarial B2B de España. Arquitectura Big Data diseñada para el sector turismo y más
        allá.
    </p>
    <div>
        <a href="#" class="btn-primary">Acceder a la API</a>
        <a href="#" class="link-secondary">Ver Documentación</a>
    </div>
</section>

<!-- Metrics Console (Global) -->
<div class="metrics-grid" style="margin-bottom: 120px;">
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">EMPRESAS TOTALES</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">7,072,734</div>
            <div class="metric-desc">Registros B2B</div>
        </div>
        <div class="panel-footer">
            <span>TYPE: B2B</span>
            <span>UPD: WEEKLY</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">EMAILS</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">5,001,427</div>
            <div class="metric-desc">Emails Verificados</div>
        </div>
        <div class="panel-footer">
            <span>VALID: 98%</span>
            <span>FORMAT: CSV</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">COUNTRIES</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">27</div>
            <div class="metric-desc">Países Cubiertos</div>
        </div>
        <div class="panel-footer">
            <span>REGION: GLOBAL</span>
            <span>EUROPE: 21</span>
        </div>
    </div>

    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">CLIENTS_ACTIVE</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">13K+</div>
            <div class="metric-desc">Clientes Activos</div>
        </div>
        <div class="panel-footer">
            <span>GROWTH: +15%</span>
            <span>NPS: 4.8/5</span>
        </div>
    </div>
</div>

<!-- About Section (Mission & Privacy) -->
<div class="about-section" style="margin-bottom: 120px;">
    <h2 class="about-title">La mayor aportación mundial de datos B2B</h2>
    <div class="about-text">
        <p>
            Desde Granada, lidero una lucha personal y tecnológica con un único objetivo:
            <strong>construir y liberar la mayor aportación de datos empresariales B2B del mundo</strong>. Un ecosistema
            único con <strong>36 puntos de datos</strong> por empresa, consolidando información dispersa de 27 países.
        </p>
        <p>
            <strong>Privacidad vs. Open Data:</strong><br>
            Entendemos el valor del dato, pero también la privacidad. Por ello, nuestras <strong>bases de datos
                comerciales</strong> son
            las únicas que incluyen los campos de contacto directo (<strong>Email, Teléfono y Sitio Web</strong>),
            garantizando un uso profesional.
        </p>
        <p>
            Sin embargo, aportamos al mundo <strong>Open Data</strong> las cantidades exactas y el resto de campos
            estructurales (Social, Métricas, Operativa), permitiendo entrenar modelos de IA, realizar estudios de
            mercado y análisis macroeconómicos sin comprometer la privacidad individual.
        </p>
    </div>
</div>
</div>
<!-- End Main Container for Full Width Section -->

<!-- Data Structure Breakdown (Full Width) -->
<section class="structure-section"
    style="width: 100%; background: var(--panel-bg); padding: 80px 0; border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); margin-bottom: 80px;">
    <div class="container">

        <div style="grid-column: 1 / -1; text-align: center;">
            <h2 class="section-title" style="margin-bottom: 40px; border-top: none;">Estructura del Dato (48 Campos)
            </h2>
            <p style="max-width: 700px; margin: 0 auto 50px; color: var(--text-secondary); font-size: 1.1rem;">
                La riqueza del dato va más allá del contacto. Aportamos inteligencia de negocio real estructurada para
                análisis masivo.
            </p>
        </div>

        <style>
            .field-grid {
                grid-column: 1 / -1;
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 15px;
            }

            .field-item {
                background: var(--bg-color);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 15px;
                font-size: 0.9rem;
                display: flex;
                flex-direction: column;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            .field-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                border-color: var(--accent-color);
            }

            .field-name {
                font-family: 'IBM Plex Mono', monospace;
                font-weight: 600;
                color: var(--accent-color);
                margin-bottom: 6px;
                font-size: 0.95rem;
            }

            .field-desc {
                color: var(--text-secondary);
                font-size: 0.85rem;
                line-height: 1.4;
            }

            .restricted {
                border-color: var(--indicator-color);
                background: rgba(0, 255, 200, 0.05);
            }

            .restricted .field-name {
                color: var(--indicator-color);
            }

            .grid-full-width {
                grid-column: 1 / -1;
                background: var(--bg-color);
                border: 1px dashed var(--border-color);
            }
        </style>

        <div class="field-grid">
            <!-- Core Identity -->
            <div class="field-item">
                <span class="field-name">name</span>
                <span class="field-desc">Nombre comercial o razón social de la empresa.</span>
            </div>
            <div class="field-item">
                <span class="field-name">address</span>
                <span class="field-desc">Dirección física completa geolocalizada.</span>
            </div>

            <!-- Commercial Restricted -->
            <div class="field-item restricted">
                <span class="field-name">emails*</span>
                <span class="field-desc">Direcciones de correo electrónico validadas.</span>
            </div>
            <div class="field-item restricted">
                <span class="field-name">phone*</span>
                <span class="field-desc">Números de teléfono de contacto directo.</span>
            </div>
            <div class="field-item restricted">
                <span class="field-name">website*</span>
                <span class="field-desc">URL del sitio web oficial corporativo.</span>
            </div>

            <!-- Intelligence & Metadata -->
            <div class="field-item">
                <span class="field-name">main_category</span>
                <span class="field-desc">Categoría principal de actividad económica.</span>
            </div>
            <div class="field-item">
                <span class="field-name">categories</span>
                <span class="field-desc">Etiquetas secundarias y nichos de mercado.</span>
            </div>
            <div class="field-item">
                <span class="field-name">rating</span>
                <span class="field-desc">Puntuación media basada en reseñas de usuarios.</span>
            </div>
            <div class="field-item">
                <span class="field-name">reviews</span>
                <span class="field-desc">Volumen total de reseñas acumuladas.</span>
            </div>
            <div class="field-item">
                <span class="field-name">review_keywords</span>
                <span class="field-desc">Keywords temáticas extraídas de las opiniones.</span>
            </div>
            <div class="field-item">
                <span class="field-name">description</span>
                <span class="field-desc">Extracto o descripción de la actividad.</span>
            </div>

            <!-- Operational -->
            <div class="field-item">
                <span class="field-name">workday_timing</span>
                <span class="field-desc">Horario comercial detallado por días.</span>
            </div>
            <div class="field-item">
                <span class="field-name">is_temporarily_closed</span>
                <span class="field-desc">Indicador de cierre temporal del negocio.</span>
            </div>
            <div class="field-item">
                <span class="field-name">closed_on</span>
                <span class="field-desc">Días específicos de cierre habitual.</span>
            </div>

            <!-- Advanced Data -->
            <div class="field-item">
                <span class="field-name">is_spending_on_ads</span>
                <span class="field-desc">Detecta inversión publicitaria activa.</span>
            </div>
            <div class="field-item">
                <span class="field-name">competitors</span>
                <span class="field-desc">Lista de competidores directos identificados.</span>
            </div>
            <div class="field-item">
                <span class="field-name">can_claim</span>
                <span class="field-desc">Estado de reclamación del perfil (Claimed/Unclaimed).</span>
            </div>

            <div class="field-item">
                <span class="field-name">featured_image</span>
                <span class="field-desc">URL a la imagen destacada o logotipo.</span>
            </div>
            <div class="field-item">
                <span class="field-name">link</span>
                <span class="field-desc">Enlace permanente al recurso/ficha.</span>
            </div>

            <!-- Social Ecosystem -->
            <div class="field-item">
                <span class="field-name">linkedin</span>
                <span class="field-desc">Perfil corporativo o personal asociado.</span>
            </div>
            <div class="field-item">
                <span class="field-name">instagram</span>
                <span class="field-desc">Cuenta de marca y feed visual.</span>
            </div>
            <div class="field-item">
                <span class="field-name">facebook</span>
                <span class="field-desc">Fanpage oficial y engagement.</span>
            </div>
            <div class="field-item">
                <span class="field-name">youtube</span>
                <span class="field-desc">Canal de contenido audiovisual.</span>
            </div>
            <div class="field-item">
                <span class="field-name">tiktok</span>
                <span class="field-desc">Presencia en red de vídeo corto.</span>
            </div>
            <div class="field-item">
                <span class="field-name">twitter</span>
                <span class="field-desc">Canal de comunicación en tiempo real.</span>
            </div>
            <div class="field-item">
                <span class="field-name">pinterest</span>
                <span class="field-desc">Catálogos visuales y tableros.</span>
            </div>
            <div class="field-item">
                <span class="field-name">whatsapp</span>
                <span class="field-desc">Contacto directo Business API.</span>
            </div>
            <div class="field-item">
                <span class="field-name">telegram</span>
                <span class="field-desc">Canal de difusión o contacto.</span>
            </div>
            <div class="field-item">
                <span class="field-name">rss</span>
                <span class="field-desc">Feed de noticias corporativas.</span>
            </div>
            <div class="field-item">
                <span class="field-name">github</span>
                <span class="field-desc">Repositorios de código y desarrollo.</span>
            </div>
            <div class="field-item">
                <span class="field-name">vk</span>
                <span class="field-desc">Presencia en mercado rusoparlante.</span>
            </div>
            <div class="field-item">
                <span class="field-name">wechat</span>
                <span class="field-desc">Canal oficial en ecosistema asiático.</span>
            </div>
            <div class="field-item">
                <span class="field-name">weibo</span>
                <span class="field-desc">Microblogging corporativo chino.</span>
            </div>
            <div class="field-item">
                <span class="field-name">medium</span>
                <span class="field-desc">Blog corporativo y artículos.</span>
            </div>
        </div>

        <div style="grid-column: 1 / -1; margin-top: 30px; text-align: center;">
            <p style="font-size:0.85rem; color: var(--text-secondary); opacity:0.6;">
                <em>* Campos marcados están disponibles exclusivamente en versiones Comerciales/Premium por razones de
                    privacidad y regulación.</em>
            </p>
        </div>
    </div>
</section>

<!-- Restart Main Container -->
<?php $container_class = isset($is_fluid_container) && $is_fluid_container ? 'container-fluid' : 'container'; ?>
<div class="<?php echo $container_class; ?>">

    <!-- OpenData Tools Portfolio -->
    <h2 class="section-title">Plataformas OpenData</h2>

    <div class="projects-grid" style="margin-bottom: 120px;">

        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/centraldecomunicacion/" class="project-card"
            style="text-decoration: none; color: inherit;">
            <h3 class="project-title">CentralDeComunicacion.es</h3>
            <p class="project-desc">
                La referencia en datos empresariales B2B en España. Especialización en sector turístico con 1.4M+
                empresas.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Empresas</span>
                    <span class="pm-value">1.4M+</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Focus</span>
                    <span class="pm-value">España</span>
                </div>
            </div>
        </a>

        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/companiesdata/" class="project-card"
            style="text-decoration: none; color: inherit;">
            <h3 class="project-title">CompaniesData.cloud</h3>
            <p class="project-desc">
                Bases de datos empresariales de Europa y el mundo. 27 países con descarga directa en Excel y CSV.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Empresas</span>
                    <span class="pm-value">7.1M+</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Países</span>
                    <span class="pm-value">27</span>
                </div>
            </div>
        </a>

        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/ukbusiness/" class="project-card"
            style="text-decoration: none; color: inherit;">
            <h3 class="project-title">UKBusinessDatabases</h3>
            <p class="project-desc">
                La base de datos B2B más completa del Reino Unido. Todos los sectores con información de contacto
                verificada.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Empresas UK</span>
                    <span class="pm-value">840K+</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Con Email</span>
                    <span class="pm-value">100%</span>
                </div>
            </div>
        </a>

        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/enterprises/" class="project-card"
            style="text-decoration: none; color: inherit; position: relative;">
            <span class="project-tag" style="background: linear-gradient(135deg, #9945ff, #6b3fa0);">BETA</span>
            <h3 class="project-title">Central.Enterprises</h3>
            <p class="project-desc">
                API unificada para acceder a todas las bases de datos desde un solo endpoint. GraphQL y REST API.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">API</span>
                    <span class="pm-value">Unificada</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Status</span>
                    <span class="pm-value">Coming</span>
                </div>
            </div>
        </a>

    </div>

    <!-- Features Grid -->
    <h2 class="section-title">Características Principales</h2>

    <div class="projects-grid" style="margin-bottom: 120px;">

        <div class="project-card">
            <h3 class="project-title">API REST</h3>
            <p class="project-desc">
                API RESTful con endpoints documentados. Respuestas JSON optimizadas, autenticación segura, rate limiting
                inteligente.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Formato</span>
                    <span class="pm-value">JSON</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Velocidad</span>
                    <span class="pm-value">&lt;150ms</span>
                </div>
            </div>
        </div>

        <div class="project-card">
            <h3 class="project-title">Datos Actualizados</h3>
            <p class="project-desc">
                Actualización continua de registros. Verificación periódica de direcciones, teléfonos, emails y datos
                fiscales.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Frecuencia</span>
                    <span class="pm-value">Semanal</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Precisión</span>
                    <span class="pm-value">98%</span>
                </div>
            </div>
        </div>

        <div class="project-card">
            <h3 class="project-title">Categorización Detallada</h3>
            <p class="project-desc">
                Clasificación granular por actividad principal y categorías secundarias. Hoteles, Industria, Tecnología,
                Retail, Servicios.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Categorías</span>
                    <span class="pm-value">5K+</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Segmentos</span>
                    <span class="pm-value">Global</span>
                </div>
            </div>
        </div>

        <div class="project-card">
            <h3 class="project-title">Integración Fácil</h3>
            <p class="project-desc">
                Librerías para PHP, Python, JavaScript. Webhooks para actualizaciones en tiempo real. Documentación
                completa.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Lenguajes</span>
                    <span class="pm-value">5+</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Docs</span>
                    <span class="pm-value">100%</span>
                </div>
            </div>
        </div>

        <div class="project-card">
            <h3 class="project-title">Exportación Masiva</h3>
            <p class="project-desc">
                Exporta listas completas en CSV, Excel, JSON. Filtros avanzados por sector, ubicación, tamaño,
                actividad.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Formatos</span>
                    <span class="pm-value">4</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Max</span>
                    <span class="pm-value">100K</span>
                </div>
            </div>
        </div>

        <div class="project-card">
            <h3 class="project-title">Soporte Técnico</h3>
            <p class="project-desc">
                Equipo técnico dedicado. Respuesta &lt;24h, documentación exhaustiva, ejemplos de código, sandbox de
                pruebas.
            </p>
            <div class="project-metrics">
                <div class="p-metric">
                    <span class="pm-label">Respuesta</span>
                    <span class="pm-value">&lt;24h</span>
                </div>
                <div class="p-metric">
                    <span class="pm-label">Rating</span>
                    <span class="pm-value">4.8</span>
                </div>
            </div>
        </div>

    </div>

    <!-- CTA Section -->
    <div class="contact-section">
        <h2 style="font-size: 2rem; margin-bottom: 10px;">¿Necesitas acceso a los datos?</h2>
        <p style="color: var(--text-secondary); margin-bottom: 30px;">Solicita una demo o consulta nuestros planes
            empresariales.</p>

        <div style="max-width: 500px; margin: 0 auto;">
            <a href="<?php echo BASE_URL; ?>/paginas/Services/" class="btn-primary" style="margin-right: 10px;">Ver
                Planes</a>
            <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" class="link-secondary">Contactar</a>
        </div>
    </div>

    <?php include '../../Components/footer.php'; ?>