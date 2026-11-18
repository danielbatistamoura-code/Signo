const form = document.getElementById('signForm');
const submitBtn = document.getElementById('submitBtn');
const errorBox = document.getElementById('errorBox');
const resultEmpty = document.getElementById('resultEmpty');
const resultCard = document.getElementById('resultCard');
const historyBody = document.getElementById('historyBody');
const historyCount = document.getElementById('historyCount');
const refreshBtn = document.getElementById('refreshHistoryBtn');

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = 'block';
}

function hideError() {
  errorBox.style.display = 'none';
  errorBox.textContent = '';
}

function renderResult(data) {
  const { name, birthdate, sign, id } = data;
  document.getElementById('resSymbol').textContent = sign.symbol;
  document.getElementById('resSymbol').style.borderColor = sign.color;
  document.getElementById('resTitle').textContent = `${name} — ${sign.name}`;
  document.getElementById('resSubtitle').textContent = `Nascimento: ${birthdate.split('-').reverse().join('/')} • Registro #${id}`;
  document.getElementById('resPeriod').textContent = `📅 ${sign.period}`;
  document.getElementById('resElement').textContent = `🔥 Elemento: ${sign.element}`;
  document.getElementById('resModality').textContent = `🧭 Modalidade: ${sign.modality}`;
  document.getElementById('resRuler').textContent = `🪐 Regente: ${sign.ruler}`;
  document.getElementById('resDesc').textContent = sign.description;
  document.getElementById('resLucky').textContent = sign.lucky_numbers;
  document.getElementById('resCompat').textContent = sign.compatibility;

  resultEmpty.style.display = 'none';
  resultCard.style.display = 'block';
}

async function fetchHistory() {
  try {
    const res = await fetch('/api/historico');
    const data = await res.json();
    const items = data.items || [];
    historyCount.textContent = items.length;

    if (items.length === 0) {
      historyBody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:#94a3b8;">Nenhuma consulta gravada em signos.db ainda.</td></tr>`;
      return;
    }

    historyBody.innerHTML = items.map(item => `
      <tr>
        <td>#${item.id}</td>
        <td><strong>${escapeHtml(item.name)}</strong></td>
        <td>${item.symbol} ${escapeHtml(item.sign_name)}</td>
        <td>${escapeHtml(item.element)} • ${escapeHtml(item.ruler)}</td>
        <td>${escapeHtml(item.created_at)}</td>
        <td>
          <button class="btn-del" onclick="deleteHistoryItem(${item.id})">Excluir</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    historyBody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:#fca5a5;">Erro ao carregar /api/historico.</td></tr>`;
  }
}

async function deleteHistoryItem(id) {
  try {
    const res = await fetch(`/api/historico/${id}`, { method: 'DELETE' });
    if (res.ok) {
      await fetchHistory();
    }
  } catch (err) {
    console.error(err);
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  hideError();

  const name = document.getElementById('nameInput').value.trim();
  const birthdate = document.getElementById('birthdateInput').value;

  submitBtn.disabled = true;
  submitBtn.textContent = 'Consultando API...';

  try {
    const response = await fetch('/api/descobrir', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, birthdate })
    });

    const data = await response.json();
    if (!response.ok) {
      showError(data.error || 'Erro ao processar consulta.');
      return;
    }

    renderResult(data);
    await fetchHistory();
  } catch (err) {
    showError('Não foi possível conectar ao servidor Flask.');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Descobrir Signo';
  }
});

refreshBtn.addEventListener('click', fetchHistory);

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', fetchHistory);
