document.addEventListener("DOMContentLoaded", function () {
        const isMobile = () => window.innerWidth < 992;

        // Для всіх підменю
        document.querySelectorAll('.dropdown-submenu > .dropdown-toggle').forEach(function (toggleLink) {
            toggleLink.addEventListener('click', function (e) {
                if (isMobile()) {
                    const submenu = toggleLink.parentElement;
                    const dropdown = submenu.querySelector('.dropdown-menu');

                    // Якщо не відкрито — показати і зупинити Bootstrap-дію
                    if (!dropdown.classList.contains('show')) {
                        e.preventDefault(); // блокує перехід
                        e.stopPropagation(); // блокує схлопування Bootstrap

                        // Закриваємо інші підменю
                        document.querySelectorAll('.dropdown-submenu .dropdown-menu.show').forEach(function (openMenu) {
                            if (openMenu !== dropdown) {
                                openMenu.classList.remove('show');
                            }
                        });

                        dropdown.classList.add('show');
                    } else {
                        // Дозволити стандартний перехід по посиланню
                    }
                }
            });
        });

        // Десктопна поведінка — hover
        document.querySelectorAll('.dropdown-submenu').forEach(function (submenu) {
            submenu.addEventListener('mouseenter', function () {
                if (!isMobile()) {
                    submenu.querySelector('.dropdown-menu')?.classList.add('show');
                }
            });
            submenu.addEventListener('mouseleave', function () {
                if (!isMobile()) {
                    submenu.querySelector('.dropdown-menu')?.classList.remove('show');
                }
            });
        });

        // Закриття підменю при кліку поза меню
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.navbar')) {
                document.querySelectorAll('.dropdown-submenu .dropdown-menu').forEach(function (dropdown) {
                    dropdown.classList.remove('show');
                });
            }
        });
    });