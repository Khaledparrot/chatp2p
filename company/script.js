function login() {
  const user = document.getElementById('username').value;
  const pass = document.getElementById('password').value;
  if (user && pass) {
    localStorage.setItem('user', user);
    window.location.href = 'dashboard.html';
  } else {
    alert('Enter credentials');
  }
}

function register() {
  const user = document.getElementById('regUsername').value;
  const pass = document.getElementById('regPassword').value;
  if (user && pass) {
    alert('Registered! Please login.');
    window.location.href = 'login.html';
  } else {
    alert('Fill all fields');
  }
}