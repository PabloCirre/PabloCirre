<?php
/**
 * Lab 5 - Sitemap Extractor
 */

$page_title = "Sitemap Extractor - Labs - Pablo Cirre";
$page_description = "Extrator recursivo de URLs desde sitemaps XML con descarga en TXT y ZIP.";
$page_keywords = "sitemap extractor, xml parser, seo tools, pablo cirre labs";

include '../../Components/header.php';
?>

<!-- Lab Specific CSS -->
<link rel="stylesheet" href="css/style.css">

<div class="back-nav">
    <a href="<?php echo BASE_URL; ?>/Labs/">← Back to Labs</a>
</div>

<main class="lab-container">
    <div class="extractor-grid">
        
        <!-- Input Section -->
        <div class="data-panel full-width">
            <div class="panel-header">
                <span class="panel-label">CONFIG_EXTRACTOR</span>
                <div class="light on"></div>
            </div>
            <div class="panel-content">
                <div class="input-group">
                    <input type="url" id="sitemap-url" placeholder="https://example.com/sitemap.xml" required>
                    <button id="extract-btn">EXTRACT_DATA</button>
                </div>
                <div class="metric-desc">Introduce la URL del sitemap o sitemap_index para comenzar la extracción recursiva.</div>
            </div>
        </div>

        <!-- Progress & Stats -->
        <div class="data-panel">
            <div class="panel-header">
                <span class="panel-label">ESTADÍSTICAS</span>
                <div class="light" id="status-light"></div>
            </div>
            <div class="panel-content">
                <div class="metric-value" id="url-count">0</div>
                <div class="metric-desc">URLs Encontradas</div>
            </div>
            <div class="panel-footer">
                <span id="process-status">STATUS: IDLE</span>
                <span id="sitemap-depth">DEPTH: 0</span>
            </div>
        </div>

        <!-- Downloads -->
        <div class="data-panel">
            <div class="panel-header">
                <span class="panel-label">EXPORTAR_RESULTADOS</span>
                <div class="light" id="export-light"></div>
            </div>
            <div class="panel-content">
                <div class="download-buttons">
                    <button id="download-txt" class="btn-secondary" disabled>DOWNLOAD_TXT</button>
                    <button id="download-zip" class="btn-secondary" disabled>DOWNLOAD_ZIP</button>
                </div>
                <div class="metric-desc">Los archivos se generarán tras completar la extracción.</div>
            </div>
            <div class="panel-footer">
                <span>FORMAT: UTF-8</span>
                <span>COMPRESSION: ZIP</span>
            </div>
        </div>

        <!-- Console View -->
        <div class="data-panel full-width console-panel">
            <div class="panel-header">
                <span class="panel-label">EXTRACTOR_CONSOLE</span>
                <div class="light" id="console-light"></div>
            </div>
            <div class="panel-content console-view" id="console-output">
                <div class="line">Initializing Sitemap Extractor module...</div>
                <div class="line">Waiting for input...</div>
            </div>
        </div>

    </div>
</main>

<?php include '../../Components/footer.php'; ?>

<!-- Lab Specific JS -->
<script src="js/app.js"></script>
