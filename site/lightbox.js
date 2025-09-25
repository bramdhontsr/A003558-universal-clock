(function(){
  const lb = document.getElementById('lightbox');
  const lbImg = document.getElementById('lb-img');
  const lbCap = document.getElementById('lb-cap');
  const lbClose = document.querySelector('.lb-close');

  document.addEventListener('click', (e) => {
    const a = e.target.closest('a.card');
    if(!a) return;
    e.preventDefault();
    lbImg.src = a.getAttribute('href');
    lbImg.alt = a.querySelector('img')?.alt || '';
    lbCap.textContent = a.dataset.caption || a.querySelector('.cap')?.textContent || '';
    lb.classList.remove('hidden');
  });

  const hide = () => lb.classList.add('hidden');
  lbClose.addEventListener('click', hide);
  lb.addEventListener('click', (e)=>{ if(e.target === lb) hide(); });
  document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') hide(); });
})();
