(function(){
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lb-img');
  const cap = document.getElementById('lb-cap');
  const closeBtn = document.querySelector('.lb-close');

  function open(href, caption){
    img.src = href;
    img.alt = caption || '';
    cap.textContent = caption || '';
    lb.classList.remove('hidden');
  }
  function close(){
    lb.classList.add('hidden');
    img.src = '';
    cap.textContent = '';
  }

  document.addEventListener('click', (e)=>{
    const a = e.target.closest('a.card');
    if(!a) return;
    e.preventDefault();
    open(a.href, a.dataset.caption);
  });
  closeBtn.addEventListener('click', close);
  lb.addEventListener('click', (e)=>{ if(e.target === lb) close(); });
  document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') close(); });
})();
