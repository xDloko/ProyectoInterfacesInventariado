const toggleButton = document.getElementById('toggle');

toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');

    // Opcional: guardar preferencia en localStorage
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('modo', 'oscuro');
    } else {
        localStorage.setItem('modo', 'claro');
    }
});

// Cargar preferencia al iniciar
window.addEventListener('load', () => {
    const modo = localStorage.getItem('modo');
    if (modo === 'oscuro') {
        document.body.classList.add('dark-mode');
    }
});