document.addEventListener('DOMContentLoaded', function () {
    var token = window.location.hash.slice(1);
    if (!token) return;

    var form = document.getElementById('roomAccessForm');
    var input = document.getElementById('token');
    if (!form || !input) return;

    window.history.replaceState(null, document.title, window.location.pathname);
    input.value = token;
    form.requestSubmit();
});
