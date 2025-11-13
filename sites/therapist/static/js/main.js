/**
 * Therapist Site JavaScript
 * Interactive features and enhancements
 */

(function() {
    'use strict';

    // DOM Ready
    document.addEventListener('DOMContentLoaded', function() {
        initSmoothScrolling();
        initFormValidation();
        initAlertAutoDismiss();
        initScrollTopButton();
    });

    /**
     * Smooth scrolling for anchor links
     */
    function initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    const offsetTop = target.getBoundingClientRect().top + window.pageYOffset;
                    const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 0;

                    window.scrollTo({
                        top: offsetTop - navbarHeight - 20,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Enhanced form validation
     */
    function initFormValidation() {
        const forms = document.querySelectorAll('form[novalidate]');

        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }

                form.classList.add('was-validated');

                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            });

            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    if (form.classList.contains('was-validated')) {
                        validateField(this);
                    }
                });

                input.addEventListener('input', function() {
                    if (form.classList.contains('was-validated')) {
                        validateField(this);
                    }
                });
            });
        });
    }

    /**
     * Validate individual form field
     */
    function validateField(field) {
        if (field.checkValidity()) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
        }
    }

    /**
     * Auto-dismiss alerts after 5 seconds
     */
    function initAlertAutoDismiss() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');

        alerts.forEach(alert => {
            // Don't auto-dismiss error alerts
            if (alert.classList.contains('alert-danger') ||
                alert.classList.contains('alert-error')) {
                return;
            }

            setTimeout(() => {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    /**
     * Scroll to top button
     */
    function initScrollTopButton() {
        // Create scroll to top button
        const scrollBtn = document.createElement('button');
        scrollBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
        scrollBtn.className = 'btn btn-primary scroll-top-btn';
        scrollBtn.setAttribute('aria-label', 'Scroll to top');
        scrollBtn.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: none;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        `;

        document.body.appendChild(scrollBtn);

        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollBtn.style.display = 'flex';
                scrollBtn.style.alignItems = 'center';
                scrollBtn.style.justifyContent = 'center';
            } else {
                scrollBtn.style.display = 'none';
            }
        });

        // Scroll to top on click
        scrollBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Hover effect
        scrollBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });

        scrollBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    }

    /**
     * Phone number formatting (optional enhancement)
     */
    function formatPhoneNumber(input) {
        const phoneInput = document.querySelector(input);
        if (!phoneInput) return;

        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length > 10) {
                value = value.slice(0, 10);
            }

            if (value.length >= 6) {
                e.target.value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
            } else if (value.length >= 3) {
                e.target.value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
            } else {
                e.target.value = value;
            }
        });
    }

    // Initialize phone formatting for contact form if present
    formatPhoneNumber('#phone');

})();
