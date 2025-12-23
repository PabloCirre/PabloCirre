<?php
/**
 * Lab 004 - TITAN Analytics Dashboard
 * Visualización de datos de Google Analytics
 */

$page_title = "TITAN Analytics - Lab 004";
$page_description = "Dashboard experimental de analítica web. Visualización de métricas de Google Analytics y tráfico en tiempo real.";
$page_keywords = "analytics, dashboard, google analytics, data visualization, pablo cirre";

include '../../Components/header.php';
?>

<style>
    :root {
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
        --accent-glow: rgba(0, 243, 255, 0.15);
    }

    [data-theme="light"] {
        --glass-bg: rgba(0, 0, 0, 0.03);
        --glass-border: rgba(0, 0, 0, 0.1);
        --accent-glow: rgba(0, 102, 255, 0.05);
    }

    .analytics-container {
        grid-column: 1 / -1;
        padding-top: 40px;
        padding-bottom: 80px;
    }

    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 40px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 20px;
    }

    .dashboard-id {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: var(--accent-color);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .dashboard-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        margin-top: 5px;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        padding: 24px;
        position: relative;
        overflow: hidden;
    }

    .stat-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 2px;
        height: 100%;
        background: var(--accent-color);
    }

    .stat-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        display: block;
    }

    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-color);
    }

    .stat-trend {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        margin-top: 10px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    .trend-up {
        color: #00ff88;
    }

    .trend-down {
        color: #ff4400;
    }

    .charts-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 30px;
    }

    .chart-container {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        padding: 24px;
        min-height: 400px;
    }

    .chart-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .live-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        color: var(--accent-color);
    }

    .pulse {
        width: 6px;
        height: 6px;
        background: var(--accent-color);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(0, 243, 255, 0.7);
        }

        70% {
            box-shadow: 0 0 0 10px rgba(0, 243, 255, 0);
        }

        100% {
            box-shadow: 0 0 0 0 rgba(0, 243, 255, 0);
        }
    }

    .info-panel {
        margin-top: 40px;
        background: rgba(var(--accent-color-rgb), 0.05);
        border: 1px dashed var(--accent-color);
        padding: 20px;
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    .info-panel strong {
        color: var(--accent-color);
    }

    @media (max-width: 1024px) {
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .charts-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 600px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
</style>

<div class="analytics-container">
    <header class="dashboard-header">
        <div>
            <div class="dashboard-id">Experimental Access // 004</div>
            <h1 class="dashboard-title">TITAN Central Analytics</h1>
        </div>
        <div class="live-indicator">
            <div class="pulse"></div>
            MONITORIZACIÓN EN VIVO // G-94NBJV4V0Z
        </div>
    </header>

    <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-label">Usuarios (Hoy)</span>
            <div class="stat-value" id="stats-users">0</div>
            <div class="stat-trend trend-up">
                <span>↑ 12%</span> vs ayer
            </div>
        </div>
        <div class="stat-card">
            <span class="stat-label">Sesiones</span>
            <div class="stat-value" id="stats-sessions">0</div>
            <div class="stat-trend trend-up">
                <span>↑ 8%</span> vs ayer
            </div>
        </div>
        <div class="stat-card">
            <span class="stat-label">Tasa de Rebote</span>
            <div class="stat-value" id="stats-bounce">0%</div>
            <div class="stat-trend trend-down">
                <span>↓ 2%</span> optimización
            </div>
        </div>
        <div class="stat-card">
            <span class="stat-label">Páginas / Sesión</span>
            <div class="stat-value" id="stats-pages">0.0</div>
            <div class="stat-trend trend-up">
                <span>↑ 0.4</span> engagement
            </div>
        </div>
    </div>

    <div class="charts-grid">
        <div class="chart-container">
            <div class="chart-title">
                Flujo de Tráfico por Hora
                <span style="font-size: 0.7rem; color: var(--text-tertiary);">DATOS DE CONJUNTO GLOBAL</span>
            </div>
            <canvas id="trafficChart" height="200"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Distribución de Origen</div>
            <canvas id="sourceChart"></canvas>
            <div style="margin-top: 30px; font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: var(--accent-color);">Directo</span>
                    <span>42%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #00ff88;">Orgánico</span>
                    <span>38%</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #ffcc00;">Referral</span>
                    <span>20%</span>
                </div>
            </div>
        </div>
    </div>

    <div class="info-panel">
        <strong>[SISTEMA]</strong> Esta es una visualización experimental basada en la ID <strong>G-94NBJV4V0Z</strong>.
        Para integrar datos 100% reales de tu consola de Google Analytics, el sistema requiere la activación de la
        <strong>API de GA4 Data</strong> y la carga de un archivo de credenciales de Service Account en el servidor.
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Configuration & Simulation
    const stats = {
        users: 142,
        sessions: 189,
        bounce: 34.2,
        pages: 2.8
    };

    function animateValue(id, start, end, duration, decimals = 0) {
        const obj = document.getElementById(id);
        const range = end - start;
        let current = start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / (range || 1)));

        const timer = setInterval(() => {
            current += (range / (duration / 10));
            if ((range > 0 && current >= end) || (range < 0 && current <= end)) {
                current = end;
                clearInterval(timer);
            }
            obj.innerText = decimals > 0 ? current.toFixed(decimals) : Math.floor(current);
        }, 10);
    }

    // Initialize Charts
    function initCharts() {
        const ctxTraffic = document.getElementById('trafficChart').getContext('2d');
        const accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim();

        new Chart(ctxTraffic, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', 'Ahora'],
                datasets: [{
                    label: 'Visitas',
                    data: [12, 5, 28, 45, 62, 58, 75],
                    borderColor: accentColor,
                    backgroundColor: accentColor + '20',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { display: false },
                    x: {
                        ticks: { color: 'rgba(255,255,255,0.3)', font: { family: 'IBM Plex Mono' } },
                        grid: { display: false }
                    }
                }
            }
        });

        const ctxSource = document.getElementById('sourceChart').getContext('2d');
        new Chart(ctxSource, {
            type: 'doughnut',
            data: {
                labels: ['Directo', 'Orgánico', 'Referral'],
                datasets: [{
                    data: [42, 38, 20],
                    backgroundColor: [accentColor, '#00ff88', '#ffcc00'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                cutout: '80%'
            }
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        initCharts();

        // Kick off animations
        setTimeout(() => {
            animateValue('stats-users', 0, stats.users, 1500);
            animateValue('stats-sessions', 0, stats.sessions, 1500);
            animateValue('stats-bounce', 0, stats.bounce, 1500, 1);
            animateValue('stats-pages', 0, stats.pages, 1500, 1);

            // Add suffix after animation
            setTimeout(() => {
                document.getElementById('stats-bounce').innerText += '%';
            }, 1600);
        }, 500);
    });
</script>

<?php include '../../Components/footer.php'; ?>