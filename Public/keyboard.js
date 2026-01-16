let currentInput = "";
let isBlocked = false; // For AI suggestion popup
let isBanned = false;  // For the 10-second cooldown
let strikes = 0;       // Counts consecutive "Send Anyway" clicks

// --- 1. KEYBOARD CONTROLS ---
document.addEventListener('keydown', (e) => {
    if (isBlocked || isBanned) return; // Full stop if blocked or banned

    if (e.key === 'Backspace') {
        currentInput = currentInput.slice(0, -1);
    } else if (e.key === 'Enter') {
        e.preventDefault();
        checkContent();
    } else if (e.key.length === 1) {
        currentInput += e.key;
    }
    updateInputDisplay();
});

// Virtual keys
document.querySelectorAll('.key').forEach(btn => {
    btn.onclick = () => {
        if (isBlocked || isBanned) return;
        const key = btn.getAttribute('data-key');
        if (btn.id === 'backspace') currentInput = currentInput.slice(0, -1);
        else if (key) currentInput += key;
        updateInputDisplay();
    };
});

function updateInputDisplay() {
    const display = document.getElementById('typed-text');
    if (display) display.textContent = currentInput;
}

// --- 2. AI MODERATION & STRIKES ---
async function checkContent() {
    if (!currentInput.trim() || isBlocked || isBanned) return;

    try {
        const res = await fetch('http://localhost:5000/analyze-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: currentInput })
        });
        const data = await res.json();

        if (data.label !== "Safe") {
            showAiPopup(data);
        } else {
            strikes = 0; // User sent a clean message, reset the streak
            sendFinal();
        }
    } catch { sendFinal(); }
}

function showAiPopup(data) {
    isBlocked = true;
    const popup = document.getElementById('moderation-popup');
    const box = document.getElementById('suggestion-box');
    
    document.getElementById('mod-message-body').textContent = data.message;
    box.innerHTML = "";

    data.suggestions.forEach(text => {
        const b = document.createElement('button');
        b.className = "suggestion-btn";
        b.textContent = text;
        b.onclick = () => {
            currentInput = text;
            strikes = 0; // RESET STRIKES: They chose kindness!
            updateInputDisplay();
            triggerConfetti();
            unlockKeyboard();
        };
        box.appendChild(b);
    });
    popup.style.display = 'flex';
}

// --- 3. THE 10-SECOND TIMEOUT SYSTEM ---
function sendAnyway() {
    strikes++; 
    
    if (strikes >= 3) {
        startTimeout();
    } else {
        sendFinal();
        unlockKeyboard();
    }
}

function startTimeout() {
    isBanned = true; // LOCK EVERYTHING
    unlockKeyboard(); // Close the AI popup first
    
    const timeoutPopup = document.getElementById('timeout-popup');
    const countdownEl = document.getElementById('countdown');
    let timeLeft = 10;
    
    timeoutPopup.style.display = 'flex';
    countdownEl.textContent = timeLeft;

    // The Countdown Loop
    const timer = setInterval(() => {
        timeLeft--;
        countdownEl.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            clearInterval(timer);
            // --- THE UNBLOCKING ---
            isBanned = false; 
            strikes = 0; // Wipe the slate clean
            timeoutPopup.style.display = 'none'; // Hide the timer popup
            currentInput = ""; // Clear the bad message
            updateInputDisplay();
            console.log("User Unblocked");
        }
    }, 1000);
}

// --- 4. THEMES & SOCKETS ---
function setTheme(name) {
    document.body.className = name;
    document.getElementById('theme-menu').classList.add('hidden');
    localStorage.setItem('theme', name);
}

function toggleThemeMenu() {
    document.getElementById('theme-menu').classList.toggle('hidden');
}

function sendFinal() {
    window.dispatchEvent(new CustomEvent('safeMessageReady', { detail: { message: currentInput } }));
    currentInput = "";
    updateInputDisplay();
}

function unlockKeyboard() {
    isBlocked = false;
    document.getElementById('moderation-popup').style.display = 'none';
}

function triggerConfetti() {
    for (let i = 0; i < 30; i++) {
        const c = document.createElement('div');
        c.className = 'confetti';
        c.style.left = Math.random() * 100 + 'vw';
        c.style.backgroundColor = ['#a855f7', '#3b82f6', '#10b981'][Math.floor(Math.random() * 3)];
        document.body.appendChild(c);
        setTimeout(() => c.remove(), 2000);
    }
}