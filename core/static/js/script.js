setTimeout(function() {
    let alerts = document.querySelectorAll('.error-success-massage');
    alerts.forEach(function(alert) {
        alert.style.transition = "opacity 0.5s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 500); // Remove after fade out
    });
}, 2000);