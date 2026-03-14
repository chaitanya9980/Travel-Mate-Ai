/**
 * TravelMate AI - Main JavaScript File
 * Handles interactivity and dynamic functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSearchForm();
    initAnimations();
    initNotifications();
    initCopyButtons();
    initListFilters();
    initRatingSystem();
    initDatePickers();
    initSmoothScroll();
    initTooltips();
});

/**
 * Search Form Handler
 */
function initSearchForm() {
    const searchForm = document.querySelector('.hero-search-form') || document.querySelector('.hero-search form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (searchInput && searchInput.value.trim() === '') {
                e.preventDefault();
                searchInput.focus();
                showToast('Please enter a search term', 'warning');
            }
        });
    }
}

/**
 * Scroll Animations
 */
function initAnimations() {
    const autoTargets = document.querySelectorAll(
        '.section-header, .card, .feature-box, .review-card, .gallery-item, .stat-card, .auth-card, .trip-card, .hero-content, .hero-search'
    );

    autoTargets.forEach(el => {
        if (el.closest('.explore-actions')) return;
        if (el.classList.contains('sticky-top') || el.classList.contains('booking-summary')) return;
        el.classList.add('animate-on-scroll');
    });

    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    if (!animatedElements.length) return;
    if (typeof IntersectionObserver === 'undefined') {
        animatedElements.forEach(el => el.classList.add('animated'));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    animatedElements.forEach(el => observer.observe(el));
}

/**
 * Notification System
 */
function initNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Copy Buttons
 */
function initCopyButtons() {
    const buttons = document.querySelectorAll('[data-copy]');
    if (!buttons.length) return;

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const value = button.dataset.copy;
            if (!value) return;
            const message = button.dataset.copyMessage || 'Copied to clipboard!';
            copyToClipboard(value, message);
        });
    });
}

/**
 * List Filters (search + status)
 */
function initListFilters() {
    const filterInputs = document.querySelectorAll('[data-filter-input]');
    if (!filterInputs.length) return;

    filterInputs.forEach(input => {
        const targetSelector = input.dataset.filterTarget;
        if (!targetSelector) return;
        const container = document.querySelector(targetSelector);
        if (!container) return;

        const items = Array.from(container.querySelectorAll('[data-filter-item]'));
        const emptyState = container.querySelector('[data-filter-empty]');
        const countTarget = input.dataset.filterCount ? document.querySelector(input.dataset.filterCount) : null;

        const state = {
            query: '',
            status: 'all'
        };

        const update = () => {
            const query = state.query.toLowerCase();
            const status = state.status.toLowerCase();
            let visible = 0;

            items.forEach(item => {
                const text = (item.dataset.filterText || item.textContent || '').toLowerCase();
                const itemStatus = (item.dataset.status || '').toLowerCase();
                const matchesQuery = text.includes(query);
                const matchesStatus = status === 'all' || itemStatus === status;
                const isVisible = matchesQuery && matchesStatus;

                item.style.display = isVisible ? '' : 'none';
                if (isVisible) visible += 1;
            });

            if (emptyState) {
                emptyState.style.display = visible === 0 ? '' : 'none';
            }

            if (countTarget) {
                countTarget.textContent = visible;
            }
        };

        input.addEventListener('input', () => {
            state.query = input.value.trim();
            update();
        });

        const statusButtons = document.querySelectorAll(`[data-filter-status][data-filter-target=\"${targetSelector}\"]`);
        statusButtons.forEach(button => {
            button.addEventListener('click', () => {
                statusButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                state.status = button.dataset.status || 'all';
                update();
            });
        });

        update();
    });
}

/**
 * Toast Notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();

    const toast = document.createElement('div');
    const mappedType = type === 'warning' ? 'warning' : type === 'error' ? 'danger' : type === 'info' ? 'primary' : 'success';
    toast.className = `toast show align-items-center text-white bg-${mappedType} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

/**
 * Star Rating System
 */
function initRatingSystem() {
    const ratingContainers = document.querySelectorAll('.star-rating');

    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.star');
        const input = container.querySelector('input[type="hidden"]');

        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = index + 1;
                if (input) input.value = rating;

                // Update visual
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('active');
                        s.classList.remove('text-muted');
                    } else {
                        s.classList.remove('active');
                        s.classList.add('text-muted');
                    }
                });
            });

            star.addEventListener('mouseenter', function() {
                stars.forEach((s, i) => {
                    if (i <= index) {
                        s.classList.add('hover');
                    } else {
                        s.classList.remove('hover');
                    }
                });
            });

            star.addEventListener('mouseleave', function() {
                stars.forEach(s => s.classList.remove('hover'));
            });
        });
    });
}

/**
 * Date Picker Initialization
 */
function initDatePickers() {
    const datePickers = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];

    datePickers.forEach(picker => {
        picker.setAttribute('min', today);
    });
}

/**
 * Smooth Scroll
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Bootstrap Tooltips
 */
function initTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
}

/**
 * Favorite Toggle
 */
function toggleFavorite(destId, button) {
    const targetButton = button || document.querySelector(`[data-favorite-id="${destId}"]`);
    fetch(`/toggle-favorite/${destId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (!targetButton) return;
                const icon = targetButton.querySelector('i');
                if (data.action === 'added') {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                    targetButton.classList.add('active');
                    showToast('Added to favorites!', 'success');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                    targetButton.classList.remove('active');
                    showToast('Removed from favorites', 'info');
                }
            } else {
                showToast(data.message || 'Please login first', 'warning');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred', 'error');
        });
}

/**
 * Copy to Clipboard
 */
function copyToClipboard(text, message) {
    navigator.clipboard.writeText(text).then(() => {
        showToast(message || 'Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy', 'error');
    });
}

/**
 * Share functionality
 */
function shareOnFacebook(url) {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank', 'width=600,height=400');
}

function shareOnTwitter(url, text) {
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`, '_blank', 'width=600,height=400');
}

function shareOnWhatsApp(url, text) {
    window.open(`https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`, '_blank');
}

/**
 * Form Validation
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

/**
 * Image Lazy Loading
 */
document.addEventListener('DOMContentLoaded', function() {
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
});

/**
 * Navbar Scroll Effect
 */
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

/**
 * Counter Animation
 */
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);

    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

/**
 * Search Suggestions
 */
const searchInput = document.querySelector('input[name="q"]');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function() {
        const query = this.value.toLowerCase();
        if (query.length >= 2) {
            // Could implement search suggestions here
            console.log('Search query:', query);
        }
    }, 300));
}

/**
 * Debounce Helper
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Print Booking
 */
function printBooking() {
    window.print();
}

/**
 * Confirm Delete
 */
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}
