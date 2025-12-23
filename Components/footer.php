<?php
/**
 * Footer común para Pablo Cirre Portfolio
 */
?>

</main>
<!-- Footer -->
<footer class="main-footer">
    <div>
        <div>&copy; <?php echo date('Y'); ?> Pablo Cirre. Todos los sistemas nominales.</div>
        <div class="legal-links">
            <a href="<?php echo BASE_URL; ?>/paginas/Legal/aviso-legal.php">Aviso Legal</a>
            <span>·</span>
            <a href="<?php echo BASE_URL; ?>/paginas/Legal/privacidad.php">Privacidad</a>
            <span>·</span>
            <a href="<?php echo BASE_URL; ?>/paginas/Legal/cookies.php">Cookies</a>
        </div>
    </div>
    <div class="footer-links">
        <a href="<?php echo BASE_URL; ?>/Labs/">Labs</a>
        <?php
        $current_url_base = strtok($_SERVER["REQUEST_URI"], '?');
        $new_query_params = $_GET;

        // Define target state based on current session state ($is_raw_mode is set in header.php)
        if (isset($is_raw_mode) && $is_raw_mode) {
            $new_query_params['raw_mode'] = 'off';
            $link_text = "Normal";
        } else {
            $new_query_params['raw_mode'] = 'on';
            $link_text = "Raw";
        }

        $new_query_string = http_build_query($new_query_params);
        $toggle_url = $current_url_base . ($new_query_string ? '?' . $new_query_string : '');
        ?>
        <a href="<?php echo $toggle_url; ?>"
            style="opacity:0.5; font-size:0.9em; margin-left: 5px; margin-right: 15px;">[<?php echo $link_text; ?>]</a>

        <a href="https://es.linkedin.com/in/pablocirre" target="_blank" aria-label="LinkedIn">
            <span class="sr-only">LinkedIn</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path
                    d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
            </svg>
        </a>
        <a href="https://x.com/PabloCirre" target="_blank" aria-label="X">
            <span class="sr-only">X (Twitter)</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path
                    d="M13.6823 10.6218L20.2391 3H18.6854L12.9921 9.61788L8.44486 3H3.2002L10.0765 13.0074L3.2002 21H4.75404L10.7663 14.0113L15.5549 21H20.7996L13.6819 10.6218H13.6823ZM11.5541 13.0956L10.8574 12.0991L5.31391 4.16971H7.70053L12.1742 10.5689L12.8709 11.5655L18.6861 19.8835H16.2995L11.5541 13.096V13.0956Z" />
            </svg>
        </a>
        <a href="https://www.instagram.com/pablocirre/" target="_blank" aria-label="Instagram">
            <span class="sr-only">Instagram</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 448 512" fill="currentColor">
                <!-- FontAwesome Instagram Icon -->
                <path
                    d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z" />
            </svg>
        </a>
        <a href="https://github.com/branvan3000" target="_blank" aria-label="GitHub">
            <span class="sr-only">GitHub</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path
                    d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
        </a>
        <a href="<?php echo BASE_URL; ?>/paginas/Contact/">Contacto</a>
    </div>
</footer>

</div>

<?php if (!isset($is_raw_mode) || !$is_raw_mode): ?>
    <!-- JavaScript Modules -->
    <script defer src="<?php echo BASE_URL; ?>/assets/js/main.js"></script>
    <script defer src="<?php echo BASE_URL; ?>/assets/js/font-switcher.js"></script>
    <script defer src="<?php echo BASE_URL; ?>/assets/js/musical-knobs.js"></script>
    <script defer src="<?php echo BASE_URL; ?>/assets/js/mobile-nav.js"></script>
    <script defer src="<?php echo BASE_URL; ?>/assets/js/cookie-consent.js"></script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-94NBJV4V0Z"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());

        gtag('config', 'G-94NBJV4V0Z');
    </script>
<?php endif; ?>
</body>

</html>