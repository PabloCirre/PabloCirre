<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

if (isset($_GET['raw_mode'])) {
    if ($_GET['raw_mode'] === 'on') {
        $_SESSION['raw_mode'] = true;
    } elseif ($_GET['raw_mode'] === 'off') {
        $_SESSION['raw_mode'] = false;
    }
}

$is_raw_mode = isset($_SESSION['raw_mode']) && $_SESSION['raw_mode'] === true;

header('Content-Type: text/html; charset=utf-8');
/**
 * Header común para Pablo Cirre Portfolio
 * Incluye navegación principal y estilos
 */

// Detectar la página actual para marcar el enlace activo
$current_page = basename(dirname($_SERVER['PHP_SELF']));
if ($current_page == 'PabloCirre') {
    $current_page = 'home';
}

// Canonical URL Logic
$protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' || $_SERVER['SERVER_PORT'] == 443) ? "https://" : "http://";
$host = $_SERVER['HTTP_HOST'];
$uri_path = strtok($_SERVER["REQUEST_URI"], '?');
// Strip index.php from the URI path to avoid duplicate content
$uri_path = str_replace('/index.php', '', $uri_path);
// Ensure trailing slash for directories (optional, but good for consistency) if it's not root
if ($uri_path !== '/' && substr($uri_path, -1) !== '/') {
    $uri_path .= '/';
}
$canonical_url = $protocol . $host . $uri_path;

require_once __DIR__ . '/config.php';
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="canonical" href="<?php echo htmlspecialchars($canonical_url); ?>" />

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content="<?php echo htmlspecialchars($canonical_url); ?>" />
    <meta property="og:title"
        content="<?php echo isset($page_title) ? htmlspecialchars($page_title) : 'Pablo Cirre'; ?>" />
    <meta property="og:description"
        content="<?php echo isset($page_description) ? htmlspecialchars($page_description) : 'Pablo Cirre - Big Data, Email Intelligence, Formación & Experiencias en Vídeo'; ?>" />
    <meta property="og:image" content="<?php echo $protocol . $host . BASE_URL; ?>/assets/images/favicon.png" />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:url" content="<?php echo htmlspecialchars($canonical_url); ?>" />
    <meta name="twitter:title"
        content="<?php echo isset($page_title) ? htmlspecialchars($page_title) : 'Pablo Cirre'; ?>" />
    <meta name="twitter:description"
        content="<?php echo isset($page_description) ? htmlspecialchars($page_description) : 'Pablo Cirre - Big Data, Email Intelligence, Formación & Experiencias en Vídeo'; ?>" />
    <meta name="twitter:image" content="<?php echo $protocol . $host . BASE_URL; ?>/assets/images/favicon.png" />

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Pablo Cirre",
        "url": "<?php echo htmlspecialchars($canonical_url); ?>",
        "description": "<?php echo isset($page_description) ? htmlspecialchars($page_description) : 'Pablo Cirre - Big Data, Email Intelligence, Formación & Experiencias en Vídeo'; ?>",
        "author": {
            "@type": "Person",
            "name": "Pablo Cirre"
        }
    }
    </script>

    <meta name="description"
        content="<?php echo isset($page_description) ? $page_description : 'Pablo Cirre - Big Data, Email Intelligence, Formación & Experiencias en Vídeo'; ?>">
    <meta name="keywords"
        content="<?php echo isset($page_keywords) ? $page_keywords : 'Big Data, verificador email, bases de datos empresas, formación desarrollo web, videojuegos indie, Granada'; ?>">
    <title>
        <?php echo isset($page_title) ? $page_title : 'Pablo Cirre - Big Data, Email Intelligence, Formación & Experiencias en Vídeo'; ?>
    </title>

    <?php if (!$is_raw_mode): ?>
        <!-- Favicon -->
        <link rel="icon" type="image/png" href="<?php echo BASE_URL; ?>/assets/images/favicon.png">

        <!-- Performance Optimization -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link rel="preconnect" href="https://www.google-analytics.com">

        <!-- Theme Initialization -->
        <script>
            const BASE_URL = '<?php echo BASE_URL; ?>';
            const currentTheme = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', currentTheme);
        </script>

        <!-- Performance Optimization: Async Fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link rel="preload" as="style"
            href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap">
        <link rel="stylesheet"
            href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap"
            media="print" onload="this.media='all'">
        <noscript>
            <link rel="stylesheet"
                href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap">
        </noscript>

        <!-- Inline Critical CSS -->
        <style>
            <?php
            $css_files = [
                __DIR__ . '/../assets/css/main.css',
                __DIR__ . '/../assets/css/mobile-nav.css',
                __DIR__ . '/../assets/css/cookie-banner.css'
            ];

            foreach ($css_files as $css_file) {
                if (file_exists($css_file)) {
                    echo file_get_contents($css_file);
                }
            }
            ?>
        </style>
        <!-- Removed blocking links -->
    <?php endif; ?>
</head>

<body>

    <div class="grid-bg"></div>

    <!-- Theme Toggle with Sun/Moon Icons -->
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
        <svg class="icon-sun" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2" fill="none" />
            <path d="M12 2v2m0 16v2M2 12h2m16 0h2m-3.5-7.5l-1.5 1.5M5 19l1.5-1.5m12 0l1.5 1.5M5 5l1.5 1.5"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
        <svg class="icon-moon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="2" fill="none"
                stroke-linecap="round" stroke-linejoin="round" />
        </svg>
    </button>

    <!-- Hamburger Menu Button -->
    <button class="hamburger-btn" onclick="toggleMobileMenu()" aria-label="Toggle menu">
        <span></span>
        <span></span>
        <span></span>
    </button>

    <?php
    $container_class = isset($is_fluid_container) && $is_fluid_container ? 'container-fluid' : 'container';
    ?>
    <div class="<?php echo $container_class; ?>">

        <!-- Header Navigation -->
        <header class="main-header">
            <div class="logo">
                <a href="<?php echo BASE_URL; ?>/" style="text-decoration: none; color: inherit;">Pablo Cirre <span
                        style="font-size: 0.5em; opacity: 0.5;">v.101</span></a>
            </div>
            <nav>
                <div class="nav-item-dropdown">
                    <a href="<?php echo BASE_URL; ?>/paginas/OpenData/"
                        class="<?php echo $current_page == 'OpenData' ? 'active' : ''; ?>">
                        <span class="nav-text">OpenData</span> <span
                            style="font-size: 0.7em; margin-left: 5px;">▼</span>
                    </a>
                    <div class="mega-menu">
                        <!-- CentralDeComunicacion.es -->
                        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/centraldecomunicacion/" class="mega-card">
                            <div class="mega-card-header">
                                <span class="mega-title">CentralDeComunicacion.es</span>
                            </div>
                            <div class="mega-desc">La referencia en datos empresariales B2B en España. Especialización
                                en sector turístico con 1.4M+ empresas.</div>
                            <div class="mega-metrics">
                                <div class="mm-item">
                                    <span class="mm-label">Empresas</span>
                                    <span class="mm-value">1.4M+</span>
                                </div>
                                <div class="mm-item">
                                    <span class="mm-label">Focus</span>
                                    <span class="mm-value">España</span>
                                </div>
                            </div>
                        </a>

                        <!-- CompaniesData.cloud -->
                        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/companiesdata/" class="mega-card">
                            <div class="mega-card-header">
                                <span class="mega-title">CompaniesData.cloud</span>
                            </div>
                            <div class="mega-desc">Bases de datos empresariales de Europa y el mundo. 27 países con
                                descarga directa en Excel y CSV.</div>
                            <div class="mega-metrics">
                                <div class="mm-item">
                                    <span class="mm-label">Empresas</span>
                                    <span class="mm-value">7.1M+</span>
                                </div>
                                <div class="mm-item">
                                    <span class="mm-label">Países</span>
                                    <span class="mm-value">27</span>
                                </div>
                            </div>
                        </a>

                        <!-- UKBusinessDatabases -->
                        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/ukbusiness/" class="mega-card">
                            <div class="mega-card-header">
                                <span class="mega-title">UKBusinessDatabases</span>
                            </div>
                            <div class="mega-desc">La base de datos B2B más completa del Reino Unido. Todos los sectores
                                con información de contacto verificada.</div>
                            <div class="mega-metrics">
                                <div class="mm-item">
                                    <span class="mm-label">Empresas UK</span>
                                    <span class="mm-value">840K+</span>
                                </div>
                                <div class="mm-item">
                                    <span class="mm-label">Con Email</span>
                                    <span class="mm-value">100%</span>
                                </div>
                            </div>
                        </a>

                        <!-- Central.Enterprises -->
                        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/enterprises/" class="mega-card"
                            style="border-style: dashed;">
                            <div class="mega-card-header">
                                <span class="mega-title">Central.Enterprises</span>
                                <span class="tag-beta">BETA</span>
                            </div>
                            <div class="mega-desc">API unificada para acceder a todas las bases de datos desde un solo
                                endpoint. GraphQL y REST API.</div>
                            <div class="mega-metrics">
                                <div class="mm-item">
                                    <span class="mm-label">API</span>
                                    <span class="mm-value">Unificada</span>
                                </div>
                                <div class="mm-item">
                                    <span class="mm-label">Status</span>
                                    <span class="mm-value">BETA</span>
                                </div>
                            </div>
                        </a>
                    </div>
                </div>
                <a href="<?php echo BASE_URL; ?>/paginas/Tools/"
                    class="<?php echo $current_page == 'Tools' ? 'active' : ''; ?>">
                    <span class="nav-text">Tools</span>
                </a>
                <a href="<?php echo BASE_URL; ?>/paginas/Experiences/"
                    class="<?php echo $current_page == 'Experiences' ? 'active' : ''; ?>">
                    <span class="nav-text">Experiences</span>
                </a>
                <a href="<?php echo BASE_URL; ?>/paginas/Services/"
                    class="<?php echo $current_page == 'Services' ? 'active' : ''; ?>">
                    <span class="nav-text">Services</span>
                </a>
                <a href="<?php echo BASE_URL; ?>/paginas/Projects/"
                    class="<?php echo $current_page == 'Projects' ? 'active' : ''; ?>">
                    <span class="nav-text">Projects</span>
                </a>
                <a href="<?php echo BASE_URL; ?>/paginas/Knowledge/"
                    class="<?php echo $current_page == 'Knowledge' ? 'active' : ''; ?>">
                    <span class="nav-text">Knowledge</span>
                </a>
                <a href="<?php echo BASE_URL; ?>/paginas/VideoGames/"
                    class="<?php echo $current_page == 'VideoGames' ? 'active' : ''; ?>">
                    <span class="nav-text">Video Experiences</span>
                </a>
                <a href="<?php echo BASE_URL; ?>/paginas/About-Me/"
                    class="<?php echo $current_page == 'About-Me' ? 'active' : ''; ?>">
                    <span class="nav-text">About Me</span>
                </a>
            </nav>
        </header>

        <!-- Main Landmark Start -->
        <main id="main-content" role="main">