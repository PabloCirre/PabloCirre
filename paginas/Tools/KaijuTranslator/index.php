<?php
/**
 * Tools - Kaiju Translator
 * Estilo: Splash Style
 */

// SEO Metadata
$page_title = "Kaiju Translator · Motor de Localización PHP con AI | Pablo Cirre Tools";
$page_description = "KaijuTranslator (KT) es un motor de localización automatizado para PHP que genera espejos SEO estáticos usando LLMs (OpenAI, DeepSeek, Gemini).";
$page_keywords = "kaiju translator, traduccion ai, localizacion php, seo multilingue, ai translation engine";

include '../../../Components/header.php';
?>

<style>
    /* --- NAVIGATION BAR --- */
    .project-nav-bar {
        position: fixed;
        top: 20px;
        left: 40px;
        z-index: 100;
        display: flex;
        gap: 15px;
        align-items: center;
        background: rgba(40, 40, 40, 0.8);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 50px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    [data-theme="light"] .project-nav-bar {
        background: rgba(255, 255, 255, 0.8);
    }

    .nav-back-btn {
        text-decoration: none;
        color: var(--text-color);
        font-weight: 500;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: color 0.2s;
    }

    .nav-back-btn:hover {
        color: var(--accent-color);
    }

    /* Custom Badges */
    .tech-tag {
        background: rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border-color);
        padding: 5px 10px;
        font-size: 0.8rem;
        border-radius: 4px;
        font-family: monospace;
        color: var(--text-color);
        opacity: 0.8;
    }

    .diagram-container {
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        padding: 40px;
        border-radius: 12px;
        margin: 40px 0;
        overflow-x: auto;
    }

    .diagram-step {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }

    .step-num {
        background: var(--accent-color);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
    }

    @media (max-width: 768px) {
        .project-nav-bar {
            top: auto;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: max-content;
        }
    }
</style>

<!-- --- NAVIGATION --- -->
<div class="project-nav-bar">
    <a href="<?php echo BASE_URL; ?>/paginas/Tools/" class="nav-back-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        Volver a Kaiju Tools
    </a>
    <span style="opacity: 0.3;">|</span>
    <a href="https://github.com/branvan3000/KaijuTranslator" target="_blank" class="nav-back-btn"
        style="color: var(--accent-color);">
        Ver Repo &nearr;
    </a>
</div>

<!-- Hero Section -->
<section class="hero-section" style="padding: 140px 0 80px;">
    <span class="highlight-tag"
        style="background: var(--accent-color); color: white; padding: 5px 12px; border-radius: 4px; font-size: 0.9rem; margin-bottom: 25px; display: inline-block; letter-spacing: 1px;">ENGINEERING-FIRST
        LOCALIZATION</span>
    <h1 class="hero-title" style="font-size: 4rem; margin-bottom: 30px; letter-spacing: -2px; line-height: 1.1;">
        Kaiju Translator:<br>El Espejo SEO para PHP</h1>
    <p class="hero-subtitle"
        style="font-size: 1.3rem; max-width: 900px; color: var(--text-color); opacity: 0.8; line-height: 1.6;">
        Internacionalización automática sin redirecciones ni deuda técnica. <strong>KaijuTranslator</strong> genera
        capas físicas de contenido traducido por AI, listas para ser indexadas por Google en minutos.
    </p>
    <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-top: 30px;">
        <span class="tech-tag">PHP LAYER</span>
        <span class="tech-tag">ZERO-REWRITE</span>
        <span class="tech-tag">AI-DRIVEN</span>
        <span class="tech-tag">PHYSICAL MIRRORS</span>
    </div>
</section>

<!-- Metrics Grid -->
<div class="metrics-grid" style="margin-bottom: 80px;">
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">CRAWLABILITY</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">100%</div>
            <div class="metric-desc">Server-Rendered</div>
        </div>
    </div>
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">SETUP TIME</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">&lt; 5m</div>
            <div class="metric-desc">Plug & Play Integration</div>
        </div>
    </div>
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">AI MODELS</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">Multi</div>
            <div class="metric-desc">OpenAI / DeepSeek / Gemini</div>
        </div>
    </div>
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">CACHE</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">File</div>
            <div class="metric-desc">High-Performance Storage</div>
        </div>
    </div>
</div>

<!-- Main Content Flow -->
<div style="grid-column: 2 / 12; margin-bottom: 100px;">

    <!-- Timeline / Features -->
    <div style="max-width: 900px; margin: 0 auto; border-left: 3px solid var(--border-color); padding-left: 50px;">

        <!-- Feature 1: Architecture -->
        <div style="margin-bottom: 80px; position: relative;">
            <div
                style="position: absolute; left: -63px; top: 0; width: 24px; height: 24px; background: var(--bg-color); border: 4px solid var(--accent-color); border-radius: 50%;">
            </div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">Arquitectura de "Espejo
                Físico"</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Nuestra filosofía es el <strong>"Zero-Rewrite"</strong>. En lugar de complicar tu base de datos o
                    lógica de rutas, Kaiju actúa como una capa de pre-procesamiento que construye una réplica física de
                    tu sitio en subdirectorios nativos (ej. <code>/en/</code>, <code>/ja/</code>).</p>

                <div class="diagram-container">
                    <div class="diagram-step">
                        <div class="step-num">1</div>
                        <div><strong>KT Scanner:</strong> Detecta cambios en tus archivos PHP originales.</div>
                    </div>
                    <div class="diagram-step">
                        <div class="step-num">2</div>
                        <div><strong>Stub Generator:</strong> Crea ficheros "espejo" ligeros en los subdirectorios.
                        </div>
                    </div>
                    <div class="diagram-step">
                        <div class="step-num">3</div>
                        <div><strong>AI Brain:</strong> Traduce el contenido en caliente usando modelos de última
                            generación.</div>
                    </div>
                    <div class="diagram-step">
                        <div class="step-num">4</div>
                        <div><strong>SEO Injector:</strong> Añade hreflangs, sitemaps y canonicals automáticamente.
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Feature 2: SEO -->
        <div style="margin-bottom: 80px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid var(--text-color); border-radius: 50%;">
            </div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">Ingeniería para el Crecimiento
            </h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Kaiju se encarga de toda la "deuda técnica" del SEO internacional:</p>
                <ul style="margin-top: 15px;">
                    <li><strong>Smart Hreflang:</strong> Inyección automática de etiquetas de alternancia.</li>
                    <li><strong>Sitemap Indexing:</strong> Generación de sitemaps XML por idioma y sitemap_index
                        general.</li>
                    <li><strong>Logic Canonical:</strong> Gestión inteligente de canonicals para evitar contenido
                        duplicado.</li>
                </ul>
            </div>
        </div>

        <!-- Feature 3: Performance -->
        <div style="margin-bottom: 60px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid #ccc; border-radius: 50%;">
            </div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">Rendimiento y Seguridad</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Utiliza una caché de archivos local agresiva. Una vez que una página se traduce, se sirve
                    instantáneamente como HTML estático, eliminando la latencia de la AI en visitas subsiguientes.</p>
            </div>
        </div>
    </div>

</div>

<!-- CTA Final -->
<div class="contact-section">
    <h2 style="font-size: 3rem; margin-bottom: 25px;">Internacionaliza tu PHP ahora</h2>
    <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
        <a href="https://github.com/branvan3000/KaijuTranslator" target="_blank" class="btn-primary"
            style="padding: 20px 50px; font-size: 1.2rem;">Ver en GitHub -></a>
    </div>
</div>

<?php include '../../../Components/footer.php'; ?>