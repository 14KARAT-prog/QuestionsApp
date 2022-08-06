"use strict";

document.addEventListener('DOMContentLoaded', () => {
    const onScrollNav = () => {
        const nav = document.querySelector('nav');

        let prevScroll = window.pageYOffset;
        let currentScroll;

        window.addEventListener('scroll', () => {
            currentScroll = window.pageYOffset;
            console.dir(nav);
            const navHidden = () => nav.classList.contains('nav_hidden');

            if (currentScroll > prevScroll && !navHidden()) {
                nav.classList.add('nav_hidden');
            } else if (currentScroll < prevScroll && navHidden()) {
                nav.classList.remove('nav_hidden');
            }

            prevScroll = currentScroll;
        })
    }

    onScrollNav();
})
