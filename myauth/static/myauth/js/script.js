document.addEventListener('DOMContentLoaded', function() {
        const loginForm = document.getElementById('login-box');
        const registerForm = document.getElementById('register-box');
        const switchLinks = document.querySelectorAll('.register');

        switchLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();

                if (loginForm.style.display !== 'none') {
                    loginForm.style.display = 'none';
                    registerForm.style.display = 'block';
                } else {
                    registerForm.style.display = 'none';
                    loginForm.style.display = 'block';
                }
            });
        });
    });