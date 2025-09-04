// const API = "http://localhost:5000/api";
const API = `${location.origin}/api`;
let currentUser = null;
let qrSecret = null;

document.getElementById("btnRegister").addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !email || !password) {
    showMessage("authMsg", "All fields required!", "error");
    return;
  }

  try {
    const res = await fetch(`${API}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await res.json();
    showMessage(
      "authMsg",
      data.error || data.msg || "",
      data.ok ? "success" : "error"
    );

    if (data.ok) {
      document.getElementById("otpSection").style.display = "block";
    }
  } catch (error) {
    showMessage("authMsg", "Network error: " + error.message, "error");
  }
});

document.getElementById("btnVerifyOtp").addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const otp = document.getElementById("otpInput").value.trim();

  if (!otp) {
    showMessage("authMsg", "Enter OTP!", "error");
    return;
  }

  try {
    const res = await fetch(`${API}/verify-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, otp }),
    });

    const data = await res.json();
    showMessage(
      "authMsg",
      data.error || "OTP verified!",
      data.ok ? "success" : "error"
    );

    if (data.ok) {
      qrSecret = data.qr_secret;
      document.getElementById("otpSection").style.display = "none";
      showFileUI();
      displayUserQRCode(qrSecret);
    }
  } catch (error) {
    showMessage("authMsg", "Network error: " + error.message, "error");
  }
});

function displayUserQRCode(secret) {
  const qrContainer = document.getElementById("userQRCode");
  qrContainer.innerHTML = "";
  new QRCode(qrContainer, {
    text: secret,
    width: 200,
    height: 200,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.H,
  });

  document.getElementById("qrDisplay").style.display = "block";
}

document.getElementById("btnDownloadUserQR").addEventListener("click", () => {
  const canvas = document.querySelector("#userQRCode canvas");
  if (!canvas) {
    showMessage("authMsg", "QR code not generated yet", "error");
    return;
  }

  const link = document.createElement("a");
  link.download = "securefile-login-qrcode.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
});

document.getElementById("btnLogin").addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    showMessage("authMsg", "Username and password required!", "error");
    return;
  }

  try {
    const res = await fetch(`${API}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    showMessage(
      "authMsg",
      data.error || "Login successful!",
      data.ok ? "success" : "error"
    );

    if (data.ok) {
      currentUser = data;
      qrSecret = data.qr_secret;
      showFileUI();
      displayUserQRCode(qrSecret);
    }
  } catch (error) {
    showMessage("authMsg", "Network error: " + error.message, "error");
  }
});

document.getElementById("btnQrLogin").addEventListener("click", async () => {
  const fileInput = document.getElementById("qrFileInput");
  if (!fileInput.files.length) {
    showMessage("qrLoginMsg", "Please select a QR code image", "error");
    return;
  }

  try {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const img = new Image();
      img.src = e.target.result;
      img.onload = async () => {
        const canvas = document.createElement("canvas");
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const qrCode = jsQR(imageData.data, canvas.width, canvas.height);

        if (!qrCode) {
          showMessage("qrLoginMsg", "Invalid QR code", "error");
          return;
        }

        const res = await fetch(`${API}/login-qr`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ qr_secret: qrCode.data }),
        });

        const data = await res.json();
        showMessage(
          "qrLoginMsg",
          data.error || "QR login successful!",
          data.ok ? "success" : "error"
        );

        if (data.ok) {
          currentUser = data;
          qrSecret = data.qr_secret;
          showFileUI();
          displayUserQRCode(qrSecret);
        }
      };
    };
    reader.readAsDataURL(fileInput.files[0]);
  } catch (error) {
    showMessage("qrLoginMsg", "Error: " + error.message, "error");
  }
});

document.getElementById("btnUpload").addEventListener("click", async () => {
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) {
    showMessage("uploadMsg", "Select a file!", "error");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("user_id", currentUser.user_id);

  try {
    const res = await fetch(`${API}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    showMessage(
      "uploadMsg",
      data.error || "Uploaded!",
      data.ok ? "success" : "error"
    );

    if (data.ok) {
      fileInput.value = "";
      loadFiles();
    }
  } catch (error) {
    showMessage("uploadMsg", "Upload error: " + error.message, "error");
  }
});

document.getElementById("btnLogout").addEventListener("click", () => {
  currentUser = null;
  qrSecret = null;
  document.getElementById("auth").style.display = "block";
  document.getElementById("qrLogin").style.display = "block";
  document.getElementById("uploader").style.display = "none";
  document.getElementById("files").style.display = "none";
  document.getElementById("qrDisplay").style.display = "none";
  document.getElementById("authMsg").textContent = "";
  document.getElementById("uploadMsg").textContent = "";
  document.getElementById("qrLoginMsg").textContent = "";
  document.getElementById("username").value = "";
  document.getElementById("email").value = "";
  document.getElementById("password").value = "";
  document.getElementById("otpInput").value = "";
  document.getElementById("fileInput").value = "";
  document.getElementById("qrFileInput").value = "";
});

function showFileUI() {
  document.getElementById("auth").style.display = "none";
  document.getElementById("qrLogin").style.display = "none";
  document.getElementById("uploader").style.display = "block";
  document.getElementById("files").style.display = "block";
  loadFiles();
}

async function loadFiles() {
  if (!currentUser) return;

  try {
    const res = await fetch(`${API}/list?user_id=${currentUser.user_id}`);
    const data = await res.json();

    if (!data.ok) {
      showMessage("uploadMsg", data.error || "Failed to load files", "error");
      return;
    }

    const ul = document.getElementById("fileList");
    ul.innerHTML = "";

    if (data.files.length === 0) {
      ul.innerHTML = "<li>No files uploaded yet</li>";
      return;
    }

    data.files.forEach((f) => {
      const li = document.createElement("li");
      const fileSize = formatFileSize(f.size);
      const date = new Date(f.created_at).toLocaleString();

      li.innerHTML = `
        <div class="file-item">
          <span class="filename">${f.filename}</span>
          <span class="file-info">${fileSize} - ${date}</span>
          <a class="download" href="${API}/download/${f.id}" target="_blank">Download</a>
        </div>
      `;
      ul.appendChild(li);
    });
  } catch (error) {
    showMessage("uploadMsg", "Load error: " + error.message, "error");
  }
}

function showMessage(elementId, message, type = "info") {
  const element = document.getElementById(elementId);
  element.textContent = message;
  element.className = `msg ${type}`;
}

function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}
