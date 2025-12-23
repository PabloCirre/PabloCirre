<?php
/**
 * 404 Error Page - Pablo Cirre
 * Theme: "Lost Astronaut" - Friendly & Modern
 */

http_response_code(404);
$page_title = "404 - ¿Te has perdido? | Pablo Cirre";
$page_description = "Parece que esta página no existe. Vuelve a una zona segura.";
include 'Components/header.php';
?>

<div class="container" style="padding: 100px 20px; max-width: 1000px; text-align: center; display: block;">

    <div style="display: flex; flex-direction: column; align-items: center; gap: 40px;">

        <!-- Astronaut Image -->
        <div style="
            width: 300px; 
            height: 300px; 
            border-radius: 20px; 
            overflow: hidden; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            transform: rotate(-3deg);
            transition: transform 0.3s ease;
        " onmouseover="this.style.transform='rotate(0deg) scale(1.02)'"
            onmouseout="this.style.transform='rotate(-3deg)'">
            <img src="<?php echo BASE_URL; ?>/assets/img/404-astro.jpg" alt="Lost Astronaut"
                style="width: 100%; height: 100%; object-fit: cover;" loading="lazy" width="300" height="300">
        </div>

        <!-- Text Content -->
        <div style="max-width: 600px;">
            <h1 style="
                font-size: 3.5rem; 
                margin-bottom: 20px; 
                font-family: 'Space Grotesk', sans-serif;
                letter-spacing: -1px;
            ">
                ¿Te has perdido?
            </h1>

            <p style="
                font-size: 1.2rem; 
                color: var(--text-secondary); 
                line-height: 1.6; 
                margin-bottom: 40px;
            ">
                No te preocupes. Incluso los mejores exploradores pierden el rumbo a veces.
                <br>Esta página no existe, pero hay mucho más por descubrir.
            </p>

            <!-- Action Buttons -->
            <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
                <a href="<?php echo BASE_URL; ?>/" class="btn-primary" style="border-radius: 50px; padding: 15px 40px;">
                    Volver al Inicio
                </a>
                <a href="<?php echo BASE_URL; ?>/paginas/Projects/" style="
                    display: inline-block; 
                    padding: 15px 40px; 
                    text-decoration: none; 
                    color: var(--text-color); 
                    border: 1px solid var(--border-color); 
                    border-radius: 50px; 
                    transition: all 0.2s ease;
                " onmouseover="this.style.background='var(--text-color)'; this.style.color='var(--bg-color)'"
                    onmouseout="this.style.background='transparent'; this.style.color='var(--text-color)'">
                    Ver Proyectos
                </a>
            </div>
        </div>

    </div>

    <!-- Quick Links Footer -->
    <div style="
        margin-top: 100px; 
        padding-top: 40px; 
        border-top: 1px solid var(--border-color); /* Corrected from grid-line to border-color for reliability */
        display: flex; 
        justify-content: center; 
        gap: 40px; 
        font-size: 0.9rem;
        color: var(--text-secondary);
    ">
        <a href="<?php echo BASE_URL; ?>/paginas/Contact/" style="color: inherit;">Contacto</a>
        <a href="<?php echo BASE_URL; ?>/paginas/About-Me/" style="color: inherit;">Sobre Mí</a>
        <a href="<?php echo BASE_URL; ?>/paginas/OpenData/" style="color: inherit;">OpenData</a>
    </div>

</div>

<?php include 'Components/footer.php'; ?>