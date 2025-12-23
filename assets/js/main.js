// Main JavaScript for Pablo Cirre Portfolio
// Core functionality only - specific modules are in separate files

document.addEventListener('DOMContentLoaded', function () {
    console.log('Pablo Cirre Portfolio - Sistema Iniciado');

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Animate indicator lights (Class-based to avoid Reflow)
    const lights = document.querySelectorAll('.light.on');
    lights.forEach(light => {
        setInterval(() => {
            light.classList.toggle('dimmed');
        }, 1500);
    });

    // Add hover effect to knobs
    const knobs = document.querySelectorAll('.knob');
    knobs.forEach(knob => {
        knob.addEventListener('mouseenter', function () {
            this.style.transform = 'rotate(45deg)';
        });
        knob.addEventListener('mouseleave', function () {
            this.style.transform = 'rotate(0deg)';
        });
    });

    // Console log with 60s style
    console.log('%c SISTEMA OPERATIVO PABLO CIRRE v2.0 ', 'background: #ff4400; color: #fff; font-family: monospace; padding: 5px;');
    console.log('%c [✓] Big Data Module: ONLINE ', 'color: #00ccaa; font-family: monospace;');
    console.log('%c [✓] Email Verifier: ACTIVE ', 'color: #00ccaa; font-family: monospace;');
    console.log('%c [✓] Game Dev Engine: RUNNING ', 'color: #00ccaa; font-family: monospace;');

    // Timeline Pulse Logic: Activate point closest to screen center
    const timelinePoints = document.querySelectorAll('.timeline-point');
    if (timelinePoints.length > 0) {
        const updateTimeline = () => {
            const centerY = window.innerHeight / 2;
            let closestPoint = null;
            let minDistance = Infinity;

            timelinePoints.forEach(point => {
                const rect = point.getBoundingClientRect();
                const pointCenter = rect.top + (rect.height / 2);
                const distance = Math.abs(centerY - pointCenter);

                if (distance < minDistance) {
                    minDistance = distance;
                    closestPoint = point;
                }
                point.classList.remove('active');
            });

            // Increased threshold to 350px to avoid "dead zones"
            // and ensure visual continuity
            if (closestPoint && minDistance < 350) {
                closestPoint.classList.add('active');
            }
        };

        // Use passive scroll listener for performance
        window.addEventListener('scroll', updateTimeline, { passive: true });
        updateTimeline(); // Initial check
    }
});

// Theme Toggle Function
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
