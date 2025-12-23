/**
 * Cookie Consent Banner
 * Handles display, accept/reject, and localStorage persistence
 */

const cookieConsent = {
    cookieName: 'pc_cookie_consent',

    init() {
        // Check if consent already given
        const consent = localStorage.getItem(this.cookieName);
        if (!consent) {
            this.createBanner();
            // Show after small delay for smoother UX
            setTimeout(() => this.showBanner(), 1000);
        }
        console.log('%c 🍪 Cookie Consent: ' + (consent || 'PENDING'),
            'background: #ff9800; color: #000; font-family: monospace; padding: 5px;');
    },

    createBanner() {
        const banner = document.createElement('div');
        banner.id = 'cookie-banner';
        banner.className = 'cookie-banner';
        banner.innerHTML = `
            <div class="cookie-banner-text">
                Utilizamos cookies para mejorar tu experiencia. 
                <a href="${BASE_URL}/paginas/Legal/cookies.php">Más información sobre nuestra Política de Cookies</a>
            </div>
            <div class="cookie-banner-actions">
                <button class="cookie-btn cookie-btn-reject" onclick="cookieConsent.reject()">Rechazar</button>
                <button class="cookie-btn cookie-btn-accept" onclick="cookieConsent.accept()">Aceptar</button>
            </div>
        `;
        document.body.appendChild(banner);
    },

    showBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.add('visible');
        }
    },

    hideBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.remove('visible');
            setTimeout(() => banner.remove(), 500);
        }
    },

    accept() {
        localStorage.setItem(this.cookieName, 'accepted');
        this.hideBanner();
        console.log('%c 🍪 Cookies: ACCEPTED', 'color: #4CAF50; font-family: monospace;');
    },

    reject() {
        localStorage.setItem(this.cookieName, 'rejected');
        this.hideBanner();
        console.log('%c 🍪 Cookies: REJECTED', 'color: #f44336; font-family: monospace;');
    }
};

document.addEventListener('DOMContentLoaded', () => cookieConsent.init());
