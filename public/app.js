document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const input = document.getElementById('englishInput').value.trim();

  if (!input) {
    alert("Please enter an English word.");
    return;
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input })
    });

    const data = await res.json();

    document.getElementById('chineseText').textContent = data.hanzi || '--';
    document.getElementById('pinyinText').textContent = data.pinyin || '--';

    const img = document.getElementById('resultImage');
    if (data.image) {
      img.src = data.image;
      img.style.display = 'block';
    } else {
      img.style.display = 'none';
    }
  } catch (err) {
    console.error(err);
    alert('Translation failed.');
  }
});