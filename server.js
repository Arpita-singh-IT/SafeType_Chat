// keyboard.js - FULL AI BACKEND INTEGRATION

document.addEventListener('DOMContentLoaded', () => {
    console.log("keyboard.js loaded - connected to real AI backend");

    const display = document.getElementById('typed-text');
    const keys = document.querySelectorAll('.key:not(#send-btn)');
    const backspaceBtn = document.getElementById('backspace');
    const sendBtn = document.getElementById('send-btn');

    let currentText = '';

    function updateDisplay() {
        display.textContent = currentText;
    }

    // On-screen keyboard
    keys.forEach(key => {
        key.addEventListener('click', () => {
            const char = key.dataset.key;
            if (char !== undefined) {
                currentText += char;
                updateDisplay();
            }
        });
    });

    backspaceBtn?.addEventListener('click', () => {
        currentText = currentText.slice(0, -1);
        updateDisplay();
    });

    // Send → call real AI backend
    sendBtn.addEventListener('click', async () => {
        const message = currentText.trim();
        if (!message) return;

        try {
            const response = await fetch('http://localhost:5000/analyze-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: message })
            });

            const result = await response.json();
            console.log("AI response:", result);  // Check console for confirmation

            if (result.label === "Safe") {
                // Safe → send to chat
                window.dispatchEvent(
                    new CustomEvent('safeMessageReady', { detail: { message } })
                );
                currentText = '';
                updateDisplay();
            } else {
                // Toxic/Warning → show AI's friendly message
                showWarningPopup(result.label, result.message);
            }
        } catch (err) {
            console.error("Backend error:", err);
            alert("AI backend not running! Keep 'python app.py' open in terminal");
        }
    });

    // Popup with AI's message
    function showWarningPopup(level, aiMessage) {
        document.querySelector('.warning-popup')?.remove();
        document.querySelector('.warning-overlay')?.remove();

        const overlay = document.createElement('div');
        overlay.className = 'warning-overlay';
        document.body.appendChild(overlay);

        const popup = document.createElement('div');
        popup.className = 'warning-popup';
        popup.innerHTML = `
            <h3>${level === 'Toxic' ? "Let's keep it positive!" : "A kinder way?"}</h3>
            <p>${aiMessage}</p>
            <button id="rephrase-btn">OK, I'll rephrase</button>
        `;

        document.querySelector('.keyboard-container').appendChild(popup);

        popup.querySelector('#rephrase-btn').onclick = () => {
            popup.remove();
            overlay.remove();
        };
    }

    // Physical laptop keyboard
    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        if (e.key.length === 1) {
            e.preventDefault();
            currentText += e.key;
            updateDisplay();
        } else if (e.key === 'Backspace') {
            e.preventDefault();
            currentText = currentText.slice(0, -1);
            updateDisplay();
        } else if (e.key === 'Enter') {
            e.preventDefault();
            sendBtn.click();
        }
    });
});