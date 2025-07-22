// Future: Toggle navbar on small screens
document.addEventListener('DOMContentLoaded', () => {
  const menu = document.querySelector('.nav-menu');
  const toggle = document.querySelector('.nav-toggle');

  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      menu.classList.toggle('active');
    });
  }
});
