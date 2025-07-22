// === NOVATRUST SCRIPT ===

// Load dark mode preference
window.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
  }
});

// Dark mode toggle
const darkToggle = document.getElementById('toggleDarkMode');
if (darkToggle) {
  darkToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const mode = document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled';
    localStorage.setItem('darkMode', mode);
  });
}

// Language switcher hover toggle (already handled with CSS hover, this is optional fallback)
const langBtn = document.getElementById('languageBtn');
const langOptions = document.querySelector('.lang-options');

if (langBtn && langOptions) {
  langBtn.addEventListener('click', () => {
    langOptions.style.display = langOptions.style.display === 'block' ? 'none' : 'block';
  });

  document.addEventListener('click', (e) => {
    if (!langBtn.contains(e.target) && !langOptions.contains(e.target)) {
      langOptions.style.display = 'none';
    }
  });
}

// Optional: handle language selection logic
const langLinks = document.querySelectorAll('.lang-options a');
langLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const lang = link.dataset.lang;
    alert('Language switched to: ' + lang + ' (logic à implémenter)');
    // Add language switching logic here if needed
  });
});
