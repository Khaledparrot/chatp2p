function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;
  if (user && pass) {
    localStorage.setItem("user", user);
    window.location.href = "home.html";
  } else {
    alert("Please fill all fields.");
  }
}
function register() {
  const user = document.getElementById("regUsername").value;
  const pass = document.getElementById("regPassword").value;
  if (user && pass) {
    alert("Registration successful.");
    window.location.href = "login.html";
  } else {
    alert("Fill all fields.");
  }
}
function logout() {
  localStorage.clear();
}
function toggleMenu() {
  const menu = document.getElementById("dropdownMenu");
  menu.classList.toggle("show");
}
document.addEventListener("DOMContentLoaded", () => {
  const user = localStorage.getItem("user") || "Guest";
  const userHome = document.getElementById("userHome");
  const usernameDisplay = document.getElementById("usernameDisplay");
  if (userHome) userHome.textContent = user;
  if (usernameDisplay) usernameDisplay.textContent = user;
});
