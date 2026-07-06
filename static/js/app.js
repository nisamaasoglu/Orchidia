const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const dzInner = document.getElementById('dzInner');
const preview = document.getElementById('preview');
const analyzeBtn = document.getElementById('analyzeBtn');
const results = document.getElementById('results');
const uploadCard = document.getElementById('uploadCard');
let selectedFile = null;

dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('drag'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag'));
dropzone.addEventListener('drop', e => {
  e.preventDefault(); dropzone.classList.remove('drag');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) handleFile(fileInput.files[0]); });

function handleFile(file){
  if(!file.type.startsWith('image/')) return;
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    preview.src = e.target.result; preview.hidden = false; dzInner.hidden = true;
    analyzeBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

analyzeBtn.addEventListener('click', async () => {
  if(!selectedFile) return;
  analyzeBtn.textContent = 'Analyzing…'; analyzeBtn.disabled = true;
  const fd = new FormData(); fd.append('image', selectedFile);
  try{
    const res = await fetch('/analyze', {method:'POST', body:fd});
    const data = await res.json();
    if(data.error){ alert(data.error); return; }
    renderResults(data);
  }catch(err){ alert('Something went wrong. Please try again.'); }
  finally{ analyzeBtn.textContent = 'Identify & Analyze'; analyzeBtn.disabled = false; }
});

document.getElementById('againBtn').addEventListener('click', () => {
  results.hidden = true; uploadCard.hidden = false;
  preview.hidden = true; dzInner.hidden = false; analyzeBtn.disabled = true; selectedFile = null;
  window.scrollTo({top:0, behavior:'smooth'});
});

function renderResults(data){
  uploadCard.hidden = true; results.hidden = false;
  const conf = Math.round(data.prediction.confidence * 100);
  document.getElementById('speciesName').textContent = data.species_info.display_name;
  document.getElementById('speciesDesc').textContent = data.species_info.description;
  const ring = document.getElementById('confRing');
  ring.style.setProperty('--p', conf + '%');
  document.getElementById('confValue').textContent = conf + '%';
  document.getElementById('difficultyBadge').textContent = '🌱 ' + data.species_info.difficulty;
  document.getElementById('waterBadge').textContent = '💧 Water every ' + data.care.water_days + ' days';
  const sb = document.getElementById('statusBadge');
  sb.textContent = ({healthy:'✓ Healthy',attention:'! Needs attention',critical:'⚠ Critical'})[data.care.status];
  sb.className = 'badge status ' + data.care.status;

  const grid = document.getElementById('sensorGrid'); grid.innerHTML = '';
  const icons = {Temperature:'🌡️', Humidity:'💧', Light:'☀️'};
  data.care.checks.forEach(c => {
    const div = document.createElement('div');
    div.className = 'sensor ' + c.level;
    div.innerHTML = `<div class="lbl">${icons[c.metric]||''} ${c.metric}</div>
      <div class="val">${c.value}${c.unit}</div>
      <div class="lbl"><span class="dot"></span>${c.level==='ok'?'Optimal':'Off-range'}</div>`;
    grid.appendChild(div);
  });

  const tips = document.getElementById('tipsList'); tips.innerHTML = '';
  data.care.warnings.forEach(w => {
    const li = document.createElement('li');
    li.style.borderLeftColor = 'var(--warn)';
    li.innerHTML = '⚠️ ' + w.message; tips.appendChild(li);
  });
  data.care.tips.forEach(t => {
    const li = document.createElement('li'); li.textContent = '🌸 ' + t; tips.appendChild(li);
  });
  results.scrollIntoView({behavior:'smooth'});
}
