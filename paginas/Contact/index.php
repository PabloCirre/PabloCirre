<?php
/**
 * Contact Page - Pablo Cirre
 * Theme: Sci-Fi / Communication Terminal (Matches Home)
 * Layout: Fixed 2-column grid with custom container
 */

$page_title = "Contacto | Pablo Cirre";
include '../../Components/header.php';

// Logic to load keys securely
$site_key = '';
$secret_key = '';
$keys_file = __DIR__ . '/../../Components/recaptcha_keys.php';

if (file_exists($keys_file)) {
    include $keys_file;
    if (defined('RECAPTCHA_SITE_KEY'))
        $site_key = RECAPTCHA_SITE_KEY;
    if (defined('RECAPTCHA_SECRET_KEY'))
        $secret_key = RECAPTCHA_SECRET_KEY;
}

// Fallback if file read fails (for dev, using user provided keys)
if (empty($site_key))
    $site_key = '';
if (empty($secret_key))
    $secret_key = '';

$message_sent = false;
$error_message = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $recaptcha_response = $_POST['g-recaptcha-response'];

    // Verify Recaptcha
    $verify_url = 'https://www.google.com/recaptcha/api/siteverify';
    $data = array(
        'secret' => $secret_key,
        'response' => $recaptcha_response
    );

    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
            'method' => 'POST',
            'content' => http_build_query($data)
        )
    );
    $context = stream_context_create($options);
    $verify_result = file_get_contents($verify_url, false, $context);
    $json_data = json_decode($verify_result);

    if ($json_data->success) {
        // Success
        // Success
        $message_sent = true;

        // Send Email
        $to = "pablo@centraldecomunicacion.es";
        $subject = "WEB CONTACTO: " . $_POST['name']; // Subject prefix for filtering

        $email_content = "Has recibido un nuevo mensaje desde el formulario web:\n\n";
        $email_content .= "Nombre: " . $_POST['name'] . "\n";
        $email_content .= "Email: " . $_POST['email'] . "\n\n";
        $email_content .= "Mensaje:\n" . $_POST['message'] . "\n";

        $headers = "From: noreply@pablocirre.es\r\n";
        $headers .= "Reply-To: " . $_POST['email'] . "\r\n";
        $headers .= "X-Mailer: PHP/" . phpversion();

        @mail($to, $subject, $email_content, $headers);
    } else {
        $error_message = 'Error de Verificación: Por favor certifique que no es un robot.';
    }
}
?>

<script src="https://www.google.com/recaptcha/api.js?render=<?php echo $site_key; ?>"></script>

<!-- WRAPPER GLOBAL PARA AISLAR EL LAYOUT -->
<div class="custom-contact-container">

    <!-- GRID PRINCIPAL -->
    <div class="contact-grid">

        <!-- Header Panel: STATUS -->
        <div class="contact-header">
            <div
                style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid var(--text-color); padding-bottom: 20px;">
                <h1 style="font-size: 3.5rem; margin: 0; line-height: 1; font-family: 'Space Grotesk', sans-serif;">
                    CONTACTO</h1>
                <div style="font-family: monospace; font-size: 0.9rem; opacity: 0.7;">
                    ESTADO:
                    <?php echo $message_sent ? '<span style="color: #00ccaa;">ENVIADO</span>' : '<span style="color: var(--accent-color);">DISPONIBLE</span>'; ?>
                </div>
            </div>
        </div>

        <!-- Left Column: THE FORM -->
        <div class="contact-form-col">

            <?php if ($message_sent): ?>
                <div class="data-panel"
                    style="background: rgba(0, 204, 170, 0.1); border-color: #00ccaa; text-align: center; padding: 60px;">
                    <div class="panel-header" style="justify-content: center; border-bottom: none;">
                        <span class="panel-label" style="font-size: 1.2rem; color: #00ccaa;">MENSAJE ENVIADO</span>
                    </div>
                    <div class="panel-content">
                        <p style="font-size: 1.2rem; margin-bottom: 20px;">Gracias por contactar. Recibirás una respuesta en
                            breve.</p>
                        <p style="font-family: monospace;">Ref: <?php echo strtoupper(uniqid()); ?></p>
                        <a href="<?php echo BASE_URL; ?>" class="btn-primary"
                            style="margin-top: 30px; display: inline-block;">VOLVER AL INICIO</a>
                    </div>
                </div>
            <?php else: ?>

                <form action="" method="POST" class="contact-terminal">

                    <?php if ($error_message): ?>
                        <div
                            style="background: rgba(255, 68, 0, 0.1); border: 1px solid var(--accent-color); color: var(--accent-color); padding: 15px; margin-bottom: 20px; font-family: monospace;">
                            [!] <?php echo $error_message; ?>
                        </div>
                    <?php endif; ?>

                    <div class="form-group">
                        <label for="name">NOMBRE COMPLETO</label>
                        <input type="text" id="name" name="name" required placeholder="Tu nombre...">
                    </div>

                    <div class="form-group">
                        <label for="email">CORREO ELECTRÓNICO</label>
                        <input type="email" id="email" name="email" required placeholder="tu@email.com" value="<?php echo isset($_GET['email']) ? htmlspecialchars($_GET['email']) : ''; ?>">
                    </div>

                    <div class="form-group">
                        <label for="message">MENSAJE O PROYECTO</label>
                        <textarea id="message" name="message" required rows="6"
                            placeholder="Cuéntame sobre tu proyecto..."></textarea>
                    </div>

                    <!-- Recaptcha v3 Hidden Input -->
                    <input type="hidden" id="g-recaptcha-response" name="g-recaptcha-response">
            </div>

            <button type="submit" class="submit-btn" style="width: 100%;">
                <span class="btn-text">ENVIAR MENSAJE</span>
                <div class="btn-glitch"></div>
            </button>

            <script>
                document.querySelector('.contact-terminal').addEventListener('submit', function (e) {
                    e.preventDefault();
                    grecaptcha.ready(function () {
                        grecaptcha.execute('<?php echo $site_key; ?>', { action: 'submit' }).then(function (token) {
                            document.getElementById('g-recaptcha-response').value = token;
                            document.querySelector('.contact-terminal').submit();
                        });
                    });
                });
            </script>

            </form>
        <?php endif; ?>

    </div>

    <!-- Right Column: Direct Channels -->
    <div class="contact-channels-col">

        <!-- Email Panel -->
        <a href="mailto:pablo@centraldecomunicacion.es" class="data-panel"
            style="text-decoration: none; cursor: pointer; transition: all 0.3s;">
            <div class="panel-header">
                <span class="panel-label">EMAIL DIRECTO</span>
                <div class="light on"></div>
            </div>
            <div class="panel-content" style="align-items: flex-start; text-align: left;">
                <div class="metric-value" style="font-size: 1.5rem;">EMAIL</div>
                <div class="metric-desc" style="font-family: monospace; color: var(--accent-color);">
                    pablo@centraldecomunicacion.es</div>
            </div>
            <div class="panel-footer">
                <span>RESPUESTA: &lt;24H</span>
            </div>
        </a>

        <!-- WhatsApp Panel -->
        <a href="https://wa.me/34657089081" target="_blank" class="data-panel"
            style="text-decoration: none; cursor: pointer; transition: all 0.3s;">
            <div class="panel-header">
                <span class="panel-label">WHATSAPP PROFESIONAL</span>
                <div class="light on"></div>
            </div>
            <div class="panel-content" style="align-items: flex-start; text-align: left;">
                <div class="metric-value" style="font-size: 1.5rem;">WHATSAPP</div>
                <div class="metric-desc" style="font-family: monospace; color: var(--accent-color);">+34 657 089 081
                </div>
            </div>
            <div class="panel-footer">
                <span>DISPONIBLE</span>
            </div>
        </a>

        <!-- Info Panel -->
        <div class="data-panel" style="min-height: auto;">
            <div class="panel-content" style="align-items: flex-start; text-align: left;">
                <p style="font-size: 0.9rem; line-height: 1.6; opacity: 0.8;">
                    "La comunicación efectiva es el puente entre la confusión y la claridad."
                </p>
            </div>
        </div>

    </div>

</div>

</div>

<style>
    /* 
     * ESTRUCTURA DE LAYOUT ROBUSTA
     * Basada en test visual exitoso: Grid de 2 columnas + Contenedor de 1200px
     */

    .custom-contact-container {
        display: block !important;
        width: 100%;
        max-width: 100%;
        /* Permitir full width para el background si se quisiera */
        margin: 0;
        padding-top: 80px;
        padding-bottom: 80px;
        background: transparent;
    }

    .contact-grid {
        display: grid !important;
        grid-template-columns: 1.2fr 1fr !important;
        /* Proporción áurea aproximada */
        gap: 80px !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: 60px !important;

        /* Visuals del contenedor "Terminal" */
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        box-sizing: border-box;
    }

    .contact-header {
        grid-column: 1 / -1 !important;
        margin-bottom: 40px !important;
    }

    .contact-form-col {
        grid-column: 1 / 2 !important;
        display: flex;
        flex-direction: column;
        gap: 30px;
        min-width: 0;
    }

    .contact-channels-col {
        grid-column: 2 / 3 !important;
        display: flex;
        flex-direction: column;
        gap: 20px;
        min-width: 0;
    }

    /* Terminal Form Styles */
    .contact-terminal .form-group {
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
    }

    .contact-terminal label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: var(--text-color);
        margin-bottom: 10px;
        opacity: 0.8;
        letter-spacing: 1px;
    }

    .contact-terminal input,
    .contact-terminal textarea {
        background: rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
        padding: 15px;
        color: var(--text-color);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }

    [data-theme="dark"] .contact-terminal input,
    [data-theme="dark"] .contact-terminal textarea {
        background: rgba(0, 0, 0, 0.3);
    }

    .contact-terminal input:focus,
    .contact-terminal textarea:focus {
        border-color: var(--indicator-color);
        outline: none;
        box-shadow: 0 0 15px rgba(0, 204, 170, 0.2);
    }

    /* Submit Button Sci-Fi */
    .submit-btn {
        background: var(--text-color);
        color: var(--bg-color);
        border: none;
        padding: 20px 40px;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: bold;
        font-size: 1rem;
        letter-spacing: 2px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        width: 100%;
        transition: all 0.3s;
        text-transform: uppercase;
    }

    .submit-btn:hover {
        background: var(--accent-color);
        color: #fff;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .data-panel {
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        padding: 25px;
        position: relative;
        transition: transform 0.3s, box-shadow 0.3s;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 220px;
        /* Restauramos altura consistente para los paneles */
    }

    .data-panel:hover {
        transform: translateY(-5px);
        border-color: var(--accent-color);
    }

    /* Recaptcha Dark Mode Tweak */
    [data-theme="dark"] .g-recaptcha {
        filter: invert(0.9) hue-rotate(180deg);
    }

    /* RESPONSIVE */
    @media (max-width: 900px) {
        .contact-grid {
            display: flex !important;
            flex-direction: column;
            padding: 20px !important;
            gap: 40px !important;
            width: 95% !important;
        }

        .contact-form-col,
        .contact-channels-col {
            width: 100%;
            grid-column: 1 / -1 !important;
        }

        .contact-header h1 {
            font-size: 2.5rem !important;
        }
    }
</style>

<?php include '../../Components/footer.php'; ?>