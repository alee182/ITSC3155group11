document.addEventListener("DOMContentLoaded", function() {
    const loginBtn = document.getElementById('show-login');
    const signupBtn = document.getElementById('show-signup');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (loginBtn && signupBtn && loginForm && signupForm) {
        loginBtn.addEventListener('click', function() {
            loginBtn.classList.add('active');
            signupBtn.classList.remove('active');
            loginForm.classList.remove('hidden');
            signupForm.classList.add('hidden');
            
            history.pushState(null, '', '/auth/?page=login');
        });

        signupBtn.addEventListener('click', function() {
            signupBtn.classList.add('active');
            loginBtn.classList.remove('active');
            signupForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
            
            history.pushState(null, '', '/auth/?page=register');
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('show-login');
  const signupBtn = document.getElementById('show-signup');
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  loginBtn.addEventListener('click', () => {
    loginForm.classList.remove('hidden');
    signupForm.classList.add('hidden');
    loginBtn.classList.add('active');
    signupBtn.classList.remove('active');
  });

  signupBtn.addEventListener('click', () => {
    signupForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
    signupBtn.classList.add('active');
    loginBtn.classList.remove('active');
  });
});
