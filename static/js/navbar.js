document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.getElementById("hamburger");
    const navMenu = document.getElementById("navMenu");
    const navbar = document.querySelector(".navbar");
    const navLinks = document.querySelectorAll(".nav-icons a");
    let lastScrollTop = 0;

    // Toggle mobile menu
    hamburger.addEventListener("click", function () {
        hamburger.classList.toggle("active");
        navMenu.classList.toggle("active");
        
        // If menu is active, prevent scrolling on the body
        if (navMenu.classList.contains("active")) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "";
        }
    });

    // Close mobile menu when clicking outside
    document.addEventListener("click", function(e) {
        if (navMenu.classList.contains("active") && 
            !navMenu.contains(e.target) && 
            !hamburger.contains(e.target)) {
            hamburger.classList.remove("active");
            navMenu.classList.remove("active");
            document.body.style.overflow = "";
        }
    });

    // Smooth scroll on logo click
    document.querySelector('.logo').addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });


    // Add hover animations for nav links
    navLinks.forEach(link => {
        link.addEventListener("mouseenter", function() {
            const img = this.querySelector("img");
            if (img) {
                img.style.transition = "transform 0.3s ease";
                img.style.transform = "scale(1.15) rotate(5deg)";
            }
        });

        link.addEventListener("mouseleave", function() {
            const img = this.querySelector("img");
            if (img) {
                img.style.transform = "scale(1) rotate(0deg)";
            }
        });
    });

    // Detect current page and highlight active nav item
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        const linkPath = link.getAttribute("href");
        if (linkPath && currentPath.includes(linkPath) && linkPath !== '/') {
            link.classList.add("active");
        }
    });
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll(".desktop-login, .mobile-login");
    
    buttons.forEach(button => {
        button.addEventListener("click", function(e) {
            const x = e.clientX - e.target.getBoundingClientRect().left;
            const y = e.clientY - e.target.getBoundingClientRect().top;
            
            const ripple = document.createElement("span");
            ripple.className = "ripple";
            ripple.style.cssText = `
                position: absolute;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 50%;
                pointer-events: none;
                width: 0;
                height: 0;
                left: ${x}px;
                top: ${y}px;
                transform: translate(-50%, -50%);
                animation: rippleEffect 0.6s linear;
            `;
            
            button.style.position = "relative";
            button.style.overflow = "hidden";
            button.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add the ripple keyframes
    const style = document.createElement("style");
    style.textContent = `
        @keyframes rippleEffect {
            0% {
                width: 0;
                height: 0;
                opacity: 0.5;
            }
            100% {
                width: 500px;
                height: 500px;
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});