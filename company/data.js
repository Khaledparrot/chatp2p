document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById('investmentChart').getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Growth',
        data: [1000, 1500, 2000, 2500, 3000, 4000],
        backgroundColor: 'rgba(40, 167, 69, 0.2)',
        borderColor: 'rgba(40, 167, 69, 1)',
        borderWidth: 2
      }]
    }
  });
  const username = localStorage.getItem('user') || 'Guest';
  document.getElementById('usernameDisplay').innerText = username;
});