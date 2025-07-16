function showPage(id) {
  document.querySelectorAll(".page").forEach(p => p.style.display = "none");
  document.getElementById(id).style.display = "block";
}
showPage("landing-page");

// --- CAPTCHA Generation ---
let captchaCode = "";

function generateCaptchaText(length = 6) {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789";
  let code = "";
  for (let i = 0; i < length; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return code;
}

function drawCaptchaCanvas(text) {
  const canvas = document.getElementById("captcha-canvas");
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#f4f4f4";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < 10; i++) {
    ctx.strokeStyle = `rgba(0,0,0,${Math.random()})`;
    ctx.beginPath();
    ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
    ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
    ctx.stroke();
  }

  ctx.font = "bold 32px Arial";
  ctx.fillStyle = "#333";
  ctx.textBaseline = "middle";
  const spacing = canvas.width / (text.length + 1);

  for (let i = 0; i < text.length; i++) {
    const x = spacing * (i + 1) - 10;
    const y = canvas.height / 2 + (Math.random() * 10 - 5);
    const angle = Math.random() * 0.3 - 0.15;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.fillText(text[i], 0, 0);
    ctx.restore();
  }
}

function generateCaptcha() {
  captchaCode = generateCaptchaText();
  drawCaptchaCanvas(captchaCode);
  document.getElementById("captcha-input").value = "";
  document.getElementById("next-button").disabled = true;
}

document.getElementById("start-button").addEventListener("click", () => {
  generateCaptcha();
  showPage("captcha-page");
});

document.getElementById("captcha-input").addEventListener("input", function () {
  const entered = this.value.trim();
  document.getElementById("next-button").disabled = entered !== captchaCode;
});

document.getElementById("next-button").addEventListener("click", () => {
  showPage("review-page");
});

// --- Review Submission ---
document.getElementById("submit-button").addEventListener("click", async function () {
  const review = document.getElementById("review-text").value.trim();
  if (!review) {
    document.getElementById("result").innerHTML = "⚠ Please enter a review!";
    return;
  }

  document.getElementById("final-result").innerHTML = "🔍 Processing...";

  try {
    const res = await fetch("/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ review_text: review })
    });

    const data = await res.json();
    if (data.error) {
      document.getElementById("result").innerHTML = `❌ ${data.error}`;
    } else {
      document.getElementById("final-result").innerHTML = `🔹 ${data.classification}`;
      showPage("navigation-page");
    }
  } catch (error) {
    console.error(error);
    document.getElementById("result").innerHTML = "❌ Error contacting the server. Please try again!";
  }
});

document.getElementById("back-button").addEventListener("click", () => {
  showPage("review-page");
});
