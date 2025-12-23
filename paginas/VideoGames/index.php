<?php
/**
 * Verne Games - Portfolio Oficial
 * R&D Lab & Indie Studio
 */

$page_title = "Verne Games | R&D Indie Lab | Unity & Narrative Tech";
$page_description = "Verne Games: El laboratorio de desarrollo indie de Pablo Cirre. Investigación en narrativa interactiva, Unity y atmósferas de terror desde Granada.";
$page_keywords = "verne games, r&d videojuegos, unity arquitectura, narrativa interactiva, granada indie dev, realidad virtual andalucia";

include '../../Components/header.php';
?>

<!-- Hero Section: R&D Identity -->
<section class="hero-section" style="padding: 100px 0 60px;">
    <h1 class="hero-title" style="font-size: 5rem; line-height: 1;">
        Verne Games<br>
        <span style="color: var(--accent-color);">R&D</span> Lab.
    </h1>
    <p class="hero-subtitle" style="font-size: 1.5rem; margin-top: 30px; opacity: 0.9;">
        Donde la ingeniería de software colisiona con la narrativa interactiva.
        Un espacio de experimentación técnica y artística alojado en el núcleo de
        <strong style="color: var(--text-color);">PabloCirre.es</strong>.
    </p>
</section>

<!-- 1. TECH STACK & JUSTIFICATION (WHY HERE?) -->
<div class="about-section" style="margin-bottom: 100px;">
    <h2 class="section-title">Ingeniería & Arte: El Stack</h2>
    <div class="about-text" style="grid-column: 1 / -1; font-size: 1.1rem; columns: 2; gap: 40px;">
        <p>
            Verne Games no es solo un sello de videojuegos; es el <strong>Laboratorio de I+D</strong> donde valido
            arquitecturas de software complejas antes de aplicarlas en entornos empresariales.
            ¿Por qué reside este proyecto en mi portfolio personal? Porque cada línea de código escrita para
            <em>La Semana del Cometa</em> o <em>Shadow Over Innsmouth</em> es un ejercicio de optimización, patrones de
            diseño y gestión de recursos en tiempo real.
        </p>
        <p>
            Aquí, la teoría del "Clean Code" se enfrenta al caos del desarrollo de videojuegos indie.
            Utilizamos un stack tecnológico robusto para construir sistemas escalables, desde máquinas de estados
            finitos
            para la IA hasta shaders personalizados para la atmósfera visual.
        </p>
    </div>
</div>

<div class="metrics-grid" style="grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 120px;">
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">CORE ENGINE</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 1.2rem; font-weight: 700;">Unity LTS</p>
        <p class="metric-desc">C# Architecture</p>
    </div>
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">AI SYSTEMS</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 1.2rem; font-weight: 700;">Behavior Trees</p>
        <p class="metric-desc">Lógica de Enemigos</p>
    </div>
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">RENDERING</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 1.2rem; font-weight: 700;">URP / HLSL</p>
        <p class="metric-desc">Shaders Custom</p>
    </div>
    <div class="data-panel">
        <div class="panel-header">
            <span class="panel-label">AUDIO</span>
            <div class="light on"></div>
        </div>
        <p style="font-size: 1.2rem; font-weight: 700;">FMOD</p>
        <p class="metric-desc">Audio Adaptativo</p>
    </div>
</div>

<!-- 2. PHILOSOPHY (NEW HEADLINE) -->
<section class="about-section"
    style="margin-bottom: 120px; background: var(--panel-bg); padding: 60px; border: 1px solid var(--border-color);">
    <h2 class="about-title" style="margin-bottom: 20px; font-size: 2.2rem;">I+D e Interactividad<br>Aplicada</h2>
    <div class="about-text" style="grid-column: 5 / -1;">
        <h3 style="margin-bottom: 20px; color: var(--accent-color);">Creatividad sobre Presupuesto</h3>
        <p>
            Nuestra identidad se forja en <strong>Granada</strong>, bajo el mantra del "Carácter Andaluz": hacer mucho
            con poco, pero hacerlo con alma.
            No competimos con gráficos hiperrealistas; competimos con atmósferas que se quedan bajo la piel.
        </p>
        <p>
            Creemos en el videojuego como el medio narrativo definitivo. Nuestras historias no se cuentan, se juegan.
            Cada limitación presupuestaria es una oportunidad para una solución de diseño elegante.
            Somos artesanos digitales en una era de producción en masa.
        </p>
    </div>
</section>

<!-- 3. PROJECTS -->
<h2 class="section-title">Catálogo de Proyectos</h2>

<!-- Project 1: La Semana del Cometa -->
<div class="contact-section"
    style="text-align: left; grid-column: 1 / -1; padding: 0; background: transparent; border: none; box-shadow: none; margin-bottom: 40px;">
    <div
        style="background: var(--panel-bg); border: 1px solid var(--border-color); padding: 50px; position: relative; overflow: hidden;">
        <div
            style="position: absolute; top: -20px; right: -20px; width: 100px; height: 100px; background: var(--accent-color); opacity: 0.1; transform: rotate(45deg);">
        </div>

        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
            <div>
                <span class="panel-label"
                    style="color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 10px;">BETA
                    DEMO DISPONIBLE</span>
                <h3 style="font-size: 3rem; margin: 20px 0 10px; font-family: 'Space Grotesk';">La Semana del Cometa
                </h3>
                <p style="font-family: 'IBM Plex Mono'; opacity: 0.6;">THE WEEK OF THE COMET</p>
            </div>
            <div class="light on"></div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px;">
            <div>
                <p style="margin-bottom: 20px; font-size: 1.1rem; line-height: 1.6;">
                    <strong>Sinopsis:</strong> Tras el paso del Cometa Halley, una niebla sobrenatural aísla el "Centro
                    Comercial Flamingo".
                    Tú eres Alex. Estás solo, atrapado en una reliquia de neón de los 80s, y algo camina entre los
                    maniquíes.
                </p>
                <p style="margin-bottom: 20px;">
                    Inspirado en el cine de serie B de culto (<em>Dawn of the Dead</em>, <em>Night of the Comet</em>),
                    este título mezcla
                    la tensión del survival horror clásico con mecánicas de aventura moderna.
                </p>
                <a href="https://vernegames.com/" target="_blank" class="btn-primary" style="margin-top: 20px;">Ficha
                    Oficial en VerneGames</a>
                <a href="https://vernegames.itch.io/the-week-of-the-comet" target="_blank" class="link-secondary">Jugar
                    en Itch.io</a>
            </div>

            <div style="background: var(--bg-color); padding: 30px; border: 1px solid var(--border-color);">
                <h4 style="margin-bottom: 20px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;">
                    Mecánicas Clave</h4>
                <ul style="list-style: none;">
                    <li style="margin-bottom: 15px; display: flex; align-items: center;">
                        <span style="color: var(--accent-color); margin-right: 10px; font-size: 1.2rem;">🎥</span>
                        <div>
                            <strong>Cámara Cinematográfica:</strong><br>
                            <span style="font-size: 0.9rem; opacity: 0.8;">Sistema dinámico de ángulos que potencia la
                                tensión narrativa.</span>
                        </div>
                    </li>
                    <li style="margin-bottom: 15px; display: flex; align-items: center;">
                        <span style="color: var(--accent-color); margin-right: 10px; font-size: 1.2rem;">⛽</span>
                        <div>
                            <strong>Gestión de Recursos:</strong><br>
                            <span style="font-size: 0.9rem; opacity: 0.8;">La gasolina es vida. Úsala para vehículos o
                                generadores.</span>
                        </div>
                    </li>
                    <li style="margin-bottom: 15px; display: flex; align-items: center;">
                        <span style="color: var(--accent-color); margin-right: 10px; font-size: 1.2rem;">👻</span>
                        <div>
                            <strong>Sigilo Improvisado:</strong><br>
                            <span style="font-size: 0.9rem; opacity: 0.8;">El combate es la última opción. Escóndete.
                                Huye.</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- VR Section: NOW UNDER PROJECT 1 MECHANICS -->
<section class="about-section"
    style="margin-bottom: 100px; padding: 60px; border: 1px solid var(--border-color); border-left: 5px solid var(--accent-color); background: var(--panel-bg);">
    <h2 class="about-title" style="margin-bottom: 20px; font-size: 2rem;">Realidad Virtual & I+D</h2>
    <div class="about-text" style="grid-column: 5 / -1;">
        <h3 style="margin-bottom: 20px; color: var(--text-color);">Pioneros en Andalucía</h3>
        <p>
            Somos de los pocos desarrolladores especializados en <strong>Realidad Virtual</strong> en Andalucía.
            Más allá del ocio, exploramos el potencial de las experiencias inmersivas 3D para formación,
            simulación industrial y narrativa experimental.
        </p>
        <p>
            Nuestro laboratorio de I+D investiga la frontera entre lo físico y lo digital,
            creando mundos donde la presencia del usuario es total.
        </p>
        <div class="metrics-grid"
            style="grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; border:none; padding:0; box-shadow:none; background:transparent; margin-bottom: 0;">
            <div class="data-panel" style="background: var(--bg-color);">
                <div class="panel-header"><span class="panel-label">PLATFORM</span></div>
                <p style="font-weight:700;">Meta Quest</p>
            </div>
            <div class="data-panel" style="background: var(--bg-color);">
                <div class="panel-header"><span class="panel-label">ENGINE</span></div>
                <p style="font-weight:700;">XR Interaction</p>
            </div>
            <div class="data-panel" style="background: var(--bg-color);">
                <div class="panel-header"><span class="panel-label">FOCUS</span></div>
                <p style="font-weight:700;">Inmersión</p>
            </div>
        </div>
    </div>
</section>

<!-- Project 2: Shadow Over Innsmouth -->
<div class="projects-grid" style="grid-template-columns: 1fr; margin-bottom: 120px;">
    <div class="project-card">
        <div class="panel-header">
            <span class="panel-label">EN DESARROLLO</span>
            <div class="light on dimmed"></div>
        </div>
        <div style="display: grid; grid-template-columns: 2fr 1.2fr; gap: 40px;">
            <div>
                <h3 class="project-title">Shadow Over Innsmouth</h3>
                <p class="project-desc">
                    Una inmersión profunda en el horror cósmico. No es solo un juego, es una atmósfera.
                    Utilizando técnicas de renderizado low-poly avanzadas, recreamos la opresiva ciudad costera donde
                    los secretos de las profundidades emergen.
                    <br><br>
                    Exploración, investigación y terror psicológico en su estado más puro.
                </p>
                <div class="project-metrics">
                    <div class="p-metric">
                        <span class="pm-label">Atmósfera</span>
                        <span class="pm-value">Lovecraft</span>
                    </div>
                    <div class="p-metric">
                        <span class="pm-label">Estilo</span>
                        <span class="pm-value">Low-Poly</span>
                    </div>
                </div>
                <div style="margin-top: 30px; display: flex; gap: 20px; align-items: center;">
                    <a href="https://vernegames.com/" target="_blank" class="btn-primary">Ficha Oficial (VerneGames)</a>
                    <a href="https://vernegames.com/" target="_blank" class="link-secondary">Jugar (Web Oficial)</a>
                </div>

                <div style="margin-top: 20px;">
                    <a href="https://www.instagram.com/reel/DMs30-fsgCJ/?utm_source=ig_embed" target="_blank"
                        style="display: inline-flex; align-items: center; color: var(--accent-color); border: 1px solid var(--accent-color); padding: 5px 15px; font-size: 0.9rem;">
                        <span style="margin-right: 10px;">📸</span> Ver Teaser en Instagram
                    </a>
                </div>
            </div>

            <!-- Shadow Over Innsmouth: Key Mechanics -->
            <div style="background: var(--bg-color); padding: 25px; border: 1px solid var(--border-color);">
                <h4
                    style="margin-bottom: 20px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
                    Mecánicas Clave</h4>
                <ul style="list-style: none; font-size: 0.85rem;">
                    <li style="margin-bottom: 12px; display: flex; align-items: flex-start;">
                        <span style="color: var(--accent-color); margin-right: 8px;">🌑</span>
                        <span><strong>Terror Psicológico:</strong> Gestión de cordura y percepción ambiental
                            cambiante.</span>
                    </li>
                    <li style="margin-bottom: 12px; display: flex; align-items: flex-start;">
                        <span style="color: var(--accent-color); margin-right: 8px;">🔍</span>
                        <span><strong>Investigación:</strong> Recolección de evidencias y descifrado de cultos
                            antiguos.</span>
                    </li>
                    <li style="display: flex; align-items: flex-start;">
                        <span style="color: var(--accent-color); margin-right: 8px;">🌊</span>
                        <span><strong>Atmósfera Opulsiva:</strong> Sonido binaural y visuales low-poly de alta
                            fidelidad.</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- 4. CONTRIBUTORS -->
<h2 class="section-title">Colaboradores & Equipo</h2>
<p style="margin-bottom: 40px; font-size: 1.1rem; opacity: 0.8; max-width: 800px;">
    Verne Games es posible gracias a la pasión de un grupo de creadores que aportan su talento más allá de sus roles
    formales.
    Esta red de talento impulsa "la creatividad sobre el presupuesto".
</p>
<div class="metrics-grid" style="grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 100px;">
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Pablo Cirre</p>
        <p class="metric-desc">Dirección</p>
    </div>
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Julen</p>
        <p class="metric-desc">Arte 3D</p>
    </div>
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Lucas</p>
        <p class="metric-desc">Narrativa</p>
    </div>
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Christian</p>
        <p class="metric-desc">Gameplay</p>
    </div>
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Alex</p>
        <p class="metric-desc">Sistemas</p>
    </div>
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Mery</p>
        <p class="metric-desc">Ingeniería</p>
    </div>
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Juan</p>
        <p class="metric-desc">Modelado</p>
    </div>
    <div class="data-panel" style="padding: 20px;">
        <p style="font-weight: 700; font-size: 1.1rem;">Alberto</p>
        <p class="metric-desc">Marketing</p>
    </div>
</div>

<!-- Social Connectivity -->
<div class="contact-section" style="text-align: center;">
    <h3 style="margin-bottom: 30px; font-family: 'Space Grotesk';">Redes Oficiales Verne Games</h3>
    <div class="footer-links" style="justify-content: center; gap: 40px; font-size: 1.5rem;">
        <a href="https://vernegames.com/" target="_blank" aria-label="Website">🌐</a>
        <a href="https://www.instagram.com/vernegames/" target="_blank" aria-label="Instagram">📸</a>
        <a href="https://www.tiktok.com/@vernegamesoficial" target="_blank" aria-label="TikTok">🎵</a>
        <a href="https://www.youtube.com/@vernegames" target="_blank" aria-label="YouTube">▶️</a>
        <a href="https://www.linkedin.com/company/vernegames" target="_blank" aria-label="LinkedIn">💼</a>
        <a href="https://www.facebook.com/vernegames/" target="_blank" aria-label="Facebook">Ef</a>
    </div>
</div>

<?php include '../../Components/footer.php'; ?>