const form = document.getElementById('chat');
const input = document.getElementById('message');
const messages = document.getElementById('messages');
const sessionId = crypto.randomUUID();

function addMessage(text) {
  const line = document.createElement('p');
  line.textContent = text;
  messages.appendChild(line);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  const button = form.querySelector('button');
  button.disabled = true;
  addMessage(message);
  input.value = '';
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    const data = await response.json();
    addMessage(response.ok ? data.response : (data.error || 'Please try again shortly.'));
  } catch {
    addMessage('We could not connect. Please try again shortly.');
  } finally {
    button.disabled = false;
    input.focus();
  }
});
