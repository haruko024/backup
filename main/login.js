document.getElementById("loginForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    const encodedUsername = "YWRtaW4="; 
    const encodedPassword = "ZmFsY29ud2l6YXJk"; 

    if (
      btoa(username) === encodedUsername &&
      btoa(password) === encodedPassword
    ) {
      sessionStorage.setItem("loggedIn", "true");
      window.location.href = "downloads.html";
    } else {
      alert("Invalid username or password.");
    }
  });
