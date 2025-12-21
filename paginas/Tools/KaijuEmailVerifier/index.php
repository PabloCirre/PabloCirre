<?php
/**
 * Tools - Kaiju Bulk Email Verifier
 * Estilo: Splash Style (Clone of CentralDeComunicacion)
 */

// SEO Metadata
$page_title = "Kaiju Bulk Email Verifier · Validación de Email en Tiempo Real | Pablo Cirre Tools";
$page_description = "Verificador de emails profesional. Limpia tus listas, mejora tu reputación de envío y reduce rebotes con precisión del 99.9%.";
$page_keywords = "verificador email, validar correo, limpiar lista email, api validacion email, kaiju verifier";

include '../../../Components/header.php';
?>

<!-- Estilos Específicos (Heredados de Central Splash) -->
<!-- Master Template Features (Nav & Lightbox) -->
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
        /* Hardcoded dark for contrast or use var if available */
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

    /* --- LIGHTBOX SYSTEM --- */
    .lightbox {
        display: none;
        position: fixed;
        z-index: 99999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(5px);
        justify-content: center;
        align-items: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .lightbox.active {
        display: flex;
        opacity: 1;
    }

    .lightbox-container {
        position: relative;
        max-width: 90%;
        max-height: 90%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .lightbox-content {
        max-width: 100%;
        max-height: 90vh;
        box-shadow: 0 0 50px rgba(0, 0, 0, 0.5);
        border-radius: 4px;
        object-fit: contain;
    }

    .lightbox-iframe {
        width: 80vw;
        height: 45vw;
        /* 16:9 Aspect Ratio */
        max-width: 1280px;
        max-height: 720px;
        border: none;
        border-radius: 8px;
    }

    .close-lightbox {
        position: absolute;
        top: -50px;
        right: 0;
        color: #fff;
        font-size: 40px;
        font-weight: 300;
        cursor: pointer;
        transition: transform 0.2s, color 0.2s;
        line-height: 1;
    }

    .close-lightbox:hover {
        color: var(--accent-color);
        transform: rotate(90deg);
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

    /* Mobile Nav Adjustments */
    @media (max-width: 768px) {
        .project-nav-bar {
            top: auto;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: auto;
            justify-content: center;
            width: max-content;
        }
    }
</style>

<!-- --- NAVIGATION --- -->
<div class="project-nav-bar">
    <a href="<?php echo BASE_URL; ?>/paginas/OpenData/" class="nav-back-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        Volver a OpenData
    </a>
    <span style="opacity: 0.3;">|</span>
    <a href="https://kaijuverifier.com" target="_blank" class="nav-back-btn" style="color: var(--accent-color);">
        Visitar Web &nearr;
    </a>
</div>

<!-- --- LIGHTBOX SYSTEM --- -->
<div id="lightbox-modal" class="lightbox" onclick="closeLightbox(event)">
    <div class="lightbox-container">
        <span class="close-lightbox" onclick="closeCloseButton(event)">&times;</span>

        <!-- Containers for different media types -->
        <img id="lb-image" class="lightbox-content" src="" style="display:none;">
        <video id="lb-video" class="lightbox-content" controls style="display:none;"></video>
        <iframe id="lb-youtube" class="lightbox-iframe" src="" allow="autoplay; encrypted-media" allowfullscreen
            style="display:none;"></iframe>
    </div>
</div>

<script>
    const lightbox = document.getElementById('lightbox-modal');
    const lbImage = document.getElementById('lb-image');
    const lbVideo = document.getElementById('lb-video');
    const lbYoutube = document.getElementById('lb-youtube');

    function openLightbox(type, src) {
        // Fallback for old calls if they pass just one arg (src) which implies image
        if (!src && type.includes('/')) {
            src = type;
            type = 'image';
        }

        // Reset all
        lbImage.style.display = 'none';
        lbVideo.style.display = 'none';
        lbYoutube.style.display = 'none';

        // Stop any playing video
        lbVideo.pause();
        lbVideo.src = "";
        lbYoutube.src = "";

        if (type === 'image') {
            lbImage.src = src;
            lbImage.style.display = 'block';
        } else if (type === 'video') {
            lbVideo.src = src;
            lbVideo.style.display = 'block';
        } else if (type === 'youtube') {
            lbYoutube.src = src;
            lbYoutube.style.display = 'block';
        }

        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox(e) {
        // If clicked on content, do not close
        if (e && (e.target.closest('.lightbox-content') || e.target.closest('.lightbox-iframe'))) {
            return;
        }

        lightbox.classList.remove('active');
        document.body.style.overflow = 'auto';

        // Cleanup sources to stop playback
        setTimeout(() => {
            lbVideo.pause();
            lbVideo.src = "";
            lbYoutube.src = "";
        }, 300);
    }

    function closeCloseButton(e) {
        e.stopPropagation(); // Prevent double firing
        lightbox.classList.remove('active');
        document.body.style.overflow = 'auto';

        setTimeout(() => {
            lbVideo.pause();
            lbVideo.src = "";
            lbYoutube.src = "";
        }, 300);
    }

    // Close on Escape key
    document.addEventListener('keydown', function (event) {
        if (event.key === "Escape" && lightbox.classList.contains('active')) {
            closeCloseButton(event);
        }
    });
</script>

<!-- Hero Section (Splash Style) -->
<section class="hero-section" style="padding: 140px 0 80px;">
    <span class="highlight-tag"
        style="background: var(--accent-color); color: white; padding: 5px 12px; border-radius: 4px; font-size: 0.9rem; margin-bottom: 25px; display: inline-block; letter-spacing: 1px;">BETA
        PÚBLICA · ACCESO GRATUITO</span>
    <h1 class="hero-title" style="font-size: 4rem; margin-bottom: 30px; letter-spacing: -2px; line-height: 1.1;">
        Validación de Email<br>en Tiempo Real</h1>
    <p class="hero-subtitle"
        style="font-size: 1.3rem; max-width: 900px; color: var(--text-color); opacity: 0.8; line-height: 1.6;">
        Deja de enviar correos al vacío. <strong>KaijuVerifier</strong> elimina hard bounces, detecta trampas de spam y
        valida tus leads en milisegundos. Protege la reputación de tu dominio.
    </p>
    <div style="display: flex; gap: 15px; flex-wrap: wrap;">
        <span class="tech-tag">ONLINE</span>
        <span class="tech-tag">API</span>
        <span class="tech-tag">PORTABLE APPS</span>
    </div>
</section>

<!-- Metrics Grid -->
<div class="metrics-grid" style="margin-bottom: 80px;">
    <!-- Metric 1 -->
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">PRECISIÓN</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">99.9%</div>
            <div class="metric-desc">Tasa de Acierto</div>
        </div>
    </div>
    <!-- Metric 2: Box para ver interfaz (Lightbox) -->
    <div class="data-panel" style="cursor: pointer;"
        onclick="openLightbox('image', '<?php echo BASE_URL; ?>/assets/images/kaiju_preview.png')">
        <!-- Placeholder image path -->
        <div class="panel-header"><span class="panel-label">INTERFAZ</span>
            <div class="light on" style="background: var(--accent-color);"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">Simple</div>
            <div class="metric-desc">Drag & Drop Cleaning</div>
        </div>
        <div class="panel-footer">
            <span style="display: flex; align-items: center; gap: 5px; opacity: 0.8;">
                <span style="font-size: 1.2rem;">📷</span> Ver Captura
            </span>
        </div>
    </div>
    <!-- Metric 3 -->
    <div class="data-panel">
        <div class="panel-header"><span class="panel-label">VELOCIDAD</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">50ms</div>
            <div class="metric-desc">Latencia Media API</div>
        </div>
    </div>
    <!-- Metric 4 -->
    <a href="https://kaijuverifier.com" target="_blank" rel="nofollow" class="data-panel"
        style="text-decoration: none; color: inherit;">
        <div class="panel-header"><span class="panel-label">ACCESO</span>
            <div class="light on"></div>
        </div>
        <div class="panel-content">
            <div class="metric-value">WEB</div>
            <div class="metric-desc">kaijuverifier.com</div>
        </div>
    </a>
</div>

<!-- Main Content Flow -->
<div style="grid-column: 2 / 12; margin-bottom: 100px;">

    <!-- Timeline / Features -->
    <div style="max-width: 900px; margin: 0 auto; border-left: 3px solid var(--border-color); padding-left: 50px;">

        <!-- Feature 1: Limpieza -->
        <div style="margin-bottom: 80px; position: relative;">
            <div
                style="position: absolute; left: -63px; top: 0; width: 24px; height: 24px; background: var(--bg-color); border: 4px solid var(--accent-color); border-radius: 50%;">
            </div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">Limpieza Masiva de Listas</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Sube tus archivos CSV o Excel directamente. Kaiju procesa miles de correos por minuto, separando los
                    válidos de los riesgosos (catch-all, mailbox full) y los inválidos definitivos.</p>
            </div>
        </div>

        <!-- Feature 2: API -->
        <div style="margin-bottom: 80px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid var(--text-color); border-radius: 50%;">
            </div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">API para Desarrolladores</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Integra la validación en tus formularios de registro. Impide que usuarios falsos o typos entren en tu
                    base de datos desde el primer momento.</p>
                <code
                    style="display: block; background: var(--panel-bg); padding: 15px; margin-top: 20px; border-radius: 4px; font-size: 0.9rem;">GET https://api.kaijuverifier.com/v1/validate?email=test@example.com</code>
            </div>
        </div>

        <!-- Feature 3: Seguridad -->
        <div style="margin-bottom: 60px; position: relative;">
            <div
                style="position: absolute; left: -59px; top: 0; width: 16px; height: 16px; background: var(--bg-color); border: 3px solid #ccc; border-radius: 50%;">
            </div>
            <h2 style="font-size: 2.2rem; margin-bottom: 20px; color: var(--text-color);">Privacidad Garantizada</h2>
            <div style="font-size: 1.15rem; line-height: 1.8; color: var(--text-color); opacity: 0.85;">
                <p>Tus datos son procesados en memoria y nunca son almacenados ni compartidos. Cumplimiento estricto con
                    GDPR para tranquilidad total.</p>
            </div>
        </div>
    </div>

    <!-- Comparativa Compacta -->
    <div id="comparativa" style="margin-top: 100px; grid-column: 1 / -1; width: 100%;">
        <h2 class="section-title"
            style="text-align: center; font-size: 2.5rem; margin-bottom: 50px; border-top: 1px solid var(--border-color); padding-top: 60px;">
            Kaiju vs El Resto</h2>

        <div
            style="background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 8px; overflow-x: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.05); width: 100%;">
            <table
                style="width: 100%; border-collapse: collapse; color: var(--text-color); font-size: 1.1rem; min-width: 600px;">
                <thead>
                    <tr style="border-bottom: 2px solid var(--border-color); background: rgba(0,0,0,0.02);">
                        <th style="padding: 25px; text-align: left; width: 40%;">Característica</th>
                        <th
                            style="padding: 25px; text-align: left; width: 30%; color: var(--accent-color); font-size: 1.2rem;">
                            KaijuVerifier</th>
                        <th style="padding: 25px; text-align: left; width: 30%;">Tradicionales</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 20px; font-weight: bold;">Precio / Crédito</td>
                        <td style="padding: 20px;"><strong>Gratis (Beta)</strong></td>
                        <td style="padding: 20px;">$0.008 avg</td>
                    </tr>
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 20px; font-weight: bold;">Validación SMTP</td>
                        <td style="padding: 20px;"><strong>PORTABLE APPS Handshake</strong></td>
                        <td style="padding: 20px;">Ping estático</td>
                    </tr>
                    <tr>
                        <td style="padding: 20px; font-weight: bold;">Detección Catch-all</td>
                        <td style="padding: 20px; color: var(--accent-color);"><strong>Avanzada AI</strong></td>
                        <td style="padding: 20px;">Limitada</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</div>



<!-- CTA Final -->
<div class="contact-section">
    <h2 style="font-size: 3rem; margin-bottom: 25px;">Limpia tus listas hoy</h2>
    <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
        <a href="https://kaijuverifier.com" target="_blank" rel="nofollow" class="btn-primary"
            style="padding: 20px 50px; font-size: 1.2rem;">Ir a KaijuVerifier -></a>
    </div>
</div>

<?php include '../../../Components/footer.php'; ?>