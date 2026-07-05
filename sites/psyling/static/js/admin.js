/**
 * Admin Panel JavaScript
 * Interactive features for the WebGarden admin interface
 */

(function() {
    'use strict';

    // DOM Ready
    document.addEventListener('DOMContentLoaded', function() {
        initTooltips();
        initConfirmations();
        initAutoSave();
        initTableSorting();
        initSearchFilters();
    });

    /**
     * Initialize Bootstrap tooltips
     */
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    /**
     * Initialize confirmation dialogs for destructive actions
     */
    function initConfirmations() {
        const deleteButtons = document.querySelectorAll('[data-confirm]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                const message = this.getAttribute('data-confirm') || 'Are you sure?';
                if (!confirm(message)) {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }

    /**
     * Auto-save draft functionality for forms
     * Saves to localStorage every 30 seconds
     */
    function initAutoSave() {
        const forms = document.querySelectorAll('[data-autosave]');

        forms.forEach(form => {
            const formId = form.getAttribute('id') || 'form';
            const saveKey = `autosave_${formId}`;

            // Load saved data on page load
            loadFormData(form, saveKey);

            // Save periodically
            setInterval(() => {
                saveFormData(form, saveKey);
            }, 30000); // Every 30 seconds

            // Save on form change
            form.addEventListener('change', () => {
                saveFormData(form, saveKey);
            });

            // Clear saved data on successful submit
            form.addEventListener('submit', () => {
                localStorage.removeItem(saveKey);
            });
        });
    }

    /**
     * Save form data to localStorage
     */
    function saveFormData(form, key) {
        const formData = {};
        const inputs = form.querySelectorAll('input, textarea, select');

        inputs.forEach(input => {
            if (input.name && input.type !== 'password' && input.name !== 'csrf_token') {
                if (input.type === 'checkbox') {
                    formData[input.name] = input.checked;
                } else {
                    formData[input.name] = input.value;
                }
            }
        });

        try {
            localStorage.setItem(key, JSON.stringify(formData));
            showNotification('Draft saved', 'success', 2000);
        } catch (e) {
            console.error('Error saving form data:', e);
        }
    }

    /**
     * Load form data from localStorage
     */
    function loadFormData(form, key) {
        try {
            const savedData = localStorage.getItem(key);
            if (!savedData) return;

            const formData = JSON.parse(savedData);

            // Ask user if they want to restore
            if (confirm('Restore unsaved changes?')) {
                Object.keys(formData).forEach(name => {
                    const input = form.querySelector(`[name="${name}"]`);
                    if (input) {
                        if (input.type === 'checkbox') {
                            input.checked = formData[name];
                        } else {
                            input.value = formData[name];
                        }
                    }
                });
                showNotification('Draft restored', 'info', 3000);
            } else {
                localStorage.removeItem(key);
            }
        } catch (e) {
            console.error('Error loading form data:', e);
        }
    }

    /**
     * Show temporary notification
     */
    function showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} position-fixed bottom-0 end-0 m-3`;
        notification.style.zIndex = '9999';
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, duration);
    }

    /**
     * Initialize table sorting
     */
    function initTableSorting() {
        const sortableHeaders = document.querySelectorAll('th[data-sortable]');

        sortableHeaders.forEach(header => {
            header.style.cursor = 'pointer';
            header.innerHTML += ' <i class="bi bi-chevron-expand text-muted small"></i>';

            header.addEventListener('click', function() {
                const table = this.closest('table');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const columnIndex = Array.from(this.parentElement.children).indexOf(this);
                const currentOrder = this.getAttribute('data-order') || 'asc';
                const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';

                // Sort rows
                rows.sort((a, b) => {
                    const aValue = a.children[columnIndex].textContent.trim();
                    const bValue = b.children[columnIndex].textContent.trim();

                    if (newOrder === 'asc') {
                        return aValue.localeCompare(bValue);
                    } else {
                        return bValue.localeCompare(aValue);
                    }
                });

                // Update DOM
                rows.forEach(row => tbody.appendChild(row));

                // Update header
                this.setAttribute('data-order', newOrder);
                const icon = this.querySelector('i');
                icon.className = `bi bi-chevron-${newOrder === 'asc' ? 'up' : 'down'} text-primary small`;
            });
        });
    }

    /**
     * Initialize search/filter functionality
     */
    function initSearchFilters() {
        const searchInputs = document.querySelectorAll('[data-search-target]');

        searchInputs.forEach(input => {
            const targetSelector = input.getAttribute('data-search-target');
            const targets = document.querySelectorAll(targetSelector);

            input.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();

                targets.forEach(target => {
                    const text = target.textContent.toLowerCase();
                    const shouldShow = text.includes(searchTerm);

                    target.style.display = shouldShow ? '' : 'none';
                });
            });
        });
    }

    /**
     * AJAX form submission helper
     */
    window.submitAjaxForm = function(form, callback) {
        const formData = new FormData(form);

        fetch(form.action, {
            method: form.method || 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (callback) callback(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred', 'danger', 5000);
        });
    };

    /**
     * Confirmation modal helper
     */
    window.confirmAction = function(message, callback) {
        if (confirm(message)) {
            if (callback) callback();
        }
    };

    /**
     * Copy to clipboard helper
     */
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success', 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            showNotification('Failed to copy', 'danger', 3000);
        });
    };

    /**
     * Format date helper
     */
    window.formatDate = function(dateString, format = 'short') {
        const date = new Date(dateString);
        const options = format === 'short'
            ? { year: 'numeric', month: 'short', day: 'numeric' }
            : { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };

        return date.toLocaleDateString('en-US', options);
    };

})();
