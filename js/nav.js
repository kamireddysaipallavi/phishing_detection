function buildNavbar() {
  const user = localStorage.getItem('currentUser');
  const nav = document.getElementById('navbar');
  if (!nav) return;

  if (user) {
    nav.innerHTML = `
      <a href="index.html">Home</a>
      <a href="url.html">URL Analysis</a>
      <a href="email.html">Email Analysis</a>
      <a href="sms.html">SMS Analysis</a>
      <a href="bulk.html">Bulk Checker</a>
      <a href="result.html">Explainable Result</a>
      
      <a href="quiz.html">Quiz</a>
     
      <a href="password.html">Password Checker</a>
      <a href="userdashboard.html">👤 Dashboard</a>
      <a href="#" onclick="logout()">🚪 Logout</a>
    `;
  } else {
    nav.innerHTML = `
      <a href="index.html">Home</a>
      <a href="register.html">Register</a>
      <a href="login.html">Login</a>
      
      <a href="quiz.html">Quiz</a>
      
      <a href="password.html">Password Checker</a>
    `;
  }
}

function logout() {
  localStorage.removeItem('currentUser');
  localStorage.removeItem('currentUserData');
  window.location.href = 'index.html';
}

function requireLogin() {
  if (!localStorage.getItem('currentUser')) {
    alert('🔒 Please login to use this feature.');
    window.location.href = 'login.html';
    return false;
  }
  return true;
}

function initPage(requireAuth) {
  if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light-mode');
  }

  buildNavbar();

  if (requireAuth && !requireLogin()) return false;

  return true;
}