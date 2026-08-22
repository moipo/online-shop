document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.getElementById('navDrawerToggle');
    var drawer = document.getElementById('navbarCollapse');
    var overlay = document.getElementById('navOverlay');
    var closeBtn = document.getElementById('navDrawerClose');

    if (!toggle || !drawer) {
        return;
    }

    function openDrawer() {
        drawer.classList.add('open');
        if (overlay) {
            overlay.classList.add('open');
        }
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        drawer.classList.remove('open');
        if (overlay) {
            overlay.classList.remove('open');
        }
        document.body.style.overflow = '';
    }

    toggle.addEventListener('click', function (e) {
        e.preventDefault();
        if (drawer.classList.contains('open')) {
            closeDrawer();
        } else {
            openDrawer();
        }
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', closeDrawer);
    }

    if (overlay) {
        overlay.addEventListener('click', closeDrawer);
    }

    drawer.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeDrawer);
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closeDrawer();
        }
    });
});
