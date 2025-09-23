/**
 * Admin Panel JavaScript Functions
 * Handles sidebar toggle, responsive behavior, and admin-specific functionality
 */

$(document).ready(function() {
    let isMobile = $(window).width() < 768;
    
    // Initialize admin panel
    initializeAdminPanel();
    
    /**
     * Initialize admin panel functionality
     */
    function initializeAdminPanel() {
        // Setup sidebar toggle
        setupSidebarToggle();
        
        // Setup responsive behavior
        setupResponsiveBehavior();
        
        // Restore saved state
        restoreSidebarState();
        
        // Setup other admin features
        setupAdminFeatures();
    }
    
    /**
     * Setup sidebar toggle functionality
     */
    function setupSidebarToggle() {
        // Toggle sidebar on button click
        $('#sidebarToggle').click(function() {
            toggleSidebar();
        });
        
        // Close sidebar when clicking overlay (mobile)
        $('#sidebarOverlay').click(function() {
            if (isMobile) {
                closeSidebar();
            }
        });
        
        // Close sidebar on ESC key (mobile)
        $(document).keydown(function(e) {
            if (e.key === 'Escape' && isMobile && !$('#adminSidebar').hasClass('collapsed')) {
                closeSidebar();
            }
        });
    }
    
    /**
     * Toggle sidebar state
     */
    function toggleSidebar() {
        const sidebar = $('#adminSidebar');
        const content = $('#adminContent');
        const overlay = $('#sidebarOverlay');
        const toggleBtn = $('#sidebarToggle');
        const icon = toggleBtn.find('i');
        
        if (isMobile) {
            // Mobile behavior
            if (sidebar.hasClass('collapsed')) {
                // Show sidebar
                sidebar.removeClass('collapsed');
                overlay.addClass('show');
                icon.removeClass('fa-arrow-right fa-bars').addClass('fa-times');
                toggleBtn.attr('title', 'Đóng menu');
                
                // Prevent body scrolling when sidebar is open
                $('body').addClass('overflow-hidden');
            } else {
                // Hide sidebar
                closeSidebar();
            }
        } else {
            // Desktop behavior
            sidebar.toggleClass('collapsed');
            content.toggleClass('expanded');
            
            if (sidebar.hasClass('collapsed')) {
                icon.removeClass('fa-bars').addClass('fa-arrow-right');
                toggleBtn.attr('title', 'Hiện menu');
            } else {
                icon.removeClass('fa-arrow-right').addClass('fa-bars');
                toggleBtn.attr('title', 'Ẩn menu');
            }
            
            // Save state to localStorage (only for desktop)
            localStorage.setItem('sidebarCollapsed', sidebar.hasClass('collapsed'));
        }
    }
    
    /**
     * Close sidebar (mobile)
     */
    function closeSidebar() {
        const sidebar = $('#adminSidebar');
        const overlay = $('#sidebarOverlay');
        const toggleBtn = $('#sidebarToggle');
        const icon = toggleBtn.find('i');
        
        sidebar.addClass('collapsed');
        overlay.removeClass('show');
        icon.removeClass('fa-times').addClass('fa-bars');
        toggleBtn.attr('title', 'Hiện menu');
        
        // Restore body scrolling
        $('body').removeClass('overflow-hidden');
    }
    
    /**
     * Setup responsive behavior
     */
    function setupResponsiveBehavior() {
        $(window).resize(function() {
            handleResize();
        });
        
        // Initial check
        handleResize();
    }
    
    /**
     * Handle window resize
     */
    function handleResize() {
        const newIsMobile = $(window).width() < 768;
        
        if (newIsMobile !== isMobile) {
            isMobile = newIsMobile;
            const sidebar = $('#adminSidebar');
            const content = $('#adminContent');
            const overlay = $('#sidebarOverlay');
            const toggleBtn = $('#sidebarToggle');
            const icon = toggleBtn.find('i');
            
            if (isMobile) {
                // Switch to mobile
                sidebar.addClass('collapsed');
                content.removeClass('expanded');
                overlay.removeClass('show');
                icon.removeClass('fa-arrow-right fa-times').addClass('fa-bars');
                toggleBtn.attr('title', 'Hiện menu');
                $('body').removeClass('overflow-hidden');
            } else {
                // Switch to desktop
                overlay.removeClass('show');
                icon.removeClass('fa-times');
                $('body').removeClass('overflow-hidden');
                
                // Restore desktop state from localStorage
                restoreSidebarState();
            }
        }
    }
    
    /**
     * Restore sidebar state from localStorage (desktop only)
     */
    function restoreSidebarState() {
        if (!isMobile) {
            const sidebarCollapsed = localStorage.getItem('sidebarCollapsed');
            const sidebar = $('#adminSidebar');
            const content = $('#adminContent');
            const toggleBtn = $('#sidebarToggle');
            const icon = toggleBtn.find('i');
            
            if (sidebarCollapsed === 'true') {
                sidebar.addClass('collapsed');
                content.addClass('expanded');
                icon.removeClass('fa-bars').addClass('fa-arrow-right');
                toggleBtn.attr('title', 'Hiện menu');
            } else {
                sidebar.removeClass('collapsed');
                content.removeClass('expanded');
                icon.removeClass('fa-arrow-right').addClass('fa-bars');
                toggleBtn.attr('title', 'Ẩn menu');
            }
        }
    }
    
    /**
     * Setup additional admin features
     */
    function setupAdminFeatures() {
        // Auto-hide flash messages after 5 seconds
        setTimeout(function() {
            $('.alert.alert-dismissible').each(function() {
                $(this).fadeOut('slow');
            });
        }, 5000);
        
        // Add loading state to forms
        $('form').on('submit', function() {
            const submitBtn = $(this).find('button[type="submit"]');
            if (submitBtn.length) {
                submitBtn.prop('disabled', true);
                submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Đang xử lý...');
            }
        });
        
        // Confirm delete actions
        $('.btn-delete, .delete-btn, [data-confirm-delete]').on('click', function(e) {
            const message = $(this).data('confirm-message') || 'Bạn có chắc chắn muốn xóa?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
        
        // Initialize tooltips
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
        
        // Initialize popovers
        if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
            var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
            var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl);
            });
        }
    }
    
    /**
     * Utility function to show notifications
     */
    window.showNotification = function(message, type = 'info') {
        const alertClass = type === 'error' ? 'danger' : type;
        const notification = $(`
            <div class="alert alert-${alertClass} alert-custom alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(notification);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            notification.fadeOut('slow', function() {
                $(this).remove();
            });
        }, 5000);
    };
    
    /**
     * Utility function to format numbers
     */
    window.formatNumber = function(num) {
        return new Intl.NumberFormat('vi-VN').format(num);
    };
    
    /**
     * Utility function to format currency
     */
    window.formatCurrency = function(amount) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND'
        }).format(amount);
    };
});

/**
 * Global functions that can be called from anywhere
 */

// Refresh page data without full reload
function refreshData() {
    // This can be overridden in specific pages
    location.reload();
}

// Show loading overlay
function showLoading() {
    if ($('#loadingOverlay').length === 0) {
        $('body').append(`
            <div id="loadingOverlay" class="position-fixed w-100 h-100 d-flex align-items-center justify-content-center" 
                 style="top: 0; left: 0; background: rgba(0,0,0,0.5); z-index: 9999;">
                <div class="text-center text-white">
                    <div class="spinner-border mb-3" role="status">
                        <span class="visually-hidden">Đang tải...</span>
                    </div>
                    <div>Đang xử lý...</div>
                </div>
            </div>
        `);
    }
}

// Hide loading overlay
function hideLoading() {
    $('#loadingOverlay').remove();
}