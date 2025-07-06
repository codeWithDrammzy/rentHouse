document.addEventListener("DOMContentLoaded", function () {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeMobileMenuButton = document.getElementById('close-mobile-menu');

    if (mobileMenuButton && mobileMenu && closeMobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.remove('-translate-x-full');
        });

        closeMobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.add('-translate-x-full');
        });

        // Close mobile menu when clicking a link inside it
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('-translate-x-full');
            });
        });
    }

    // Set current year in footer
    const yearEl = document.getElementById('current-year');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }
});


document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById('hamburger');
  const mobileSidebar = document.getElementById('mobile-sidebar');
  const overlay = document.getElementById('overlay');

  if (hamburger && mobileSidebar && overlay) {
    hamburger.addEventListener('click', () => {
      mobileSidebar.classList.remove('-translate-x-full');
      overlay.classList.remove('hidden');
    });

    overlay.addEventListener('click', () => {
      mobileSidebar.classList.add('-translate-x-full');
      overlay.classList.add('hidden');
    });
  }

  // Profile dropdown
  const userBtn = document.getElementById('user-btn');
  const profileDropdown = document.getElementById('profile-dropdown');
  const profileWrapper = document.getElementById('profile-wrapper');

  if (userBtn && profileDropdown && profileWrapper) {
    userBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      profileDropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', (e) => {
      if (!profileWrapper.contains(e.target)) {
        profileDropdown.classList.add('hidden');
      }
    });
  }
});
