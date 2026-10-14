// Screenshot-tabs per project
document.querySelectorAll('.showcase').forEach((showcase) => {
  const main = showcase.querySelector('.showcase-main img');
  const tabs = showcase.querySelectorAll('.tabs button');
  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      tabs.forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');
      main.style.opacity = '0';
      setTimeout(() => {
        main.src = tab.dataset.src;
        main.alt = tab.dataset.alt;
        main.style.opacity = '1';
      }, 150);
    });
  });
});

// Lightbox
const lightbox = document.querySelector('.lightbox');
const lightboxImg = lightbox.querySelector('img');
document.querySelectorAll('.showcase-main').forEach((btn) => {
  btn.addEventListener('click', () => {
    const img = btn.querySelector('img');
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightbox.showModal();
  });
});
lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
lightbox.addEventListener('click', (e) => { if (e.target === lightbox) lightbox.close(); });

// Actieve link in de navigatie volgt de sectie in beeld
const navLinks = document.querySelectorAll('.seg a');
const sections = [...navLinks].map((a) => document.querySelector(a.getAttribute('href')));
const navObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    navLinks.forEach((a) => a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id));
  });
}, { rootMargin: '-45% 0px -50% 0px' });
sections.forEach((s) => s && navObserver.observe(s));

// Inloopanimatie
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.row-body > *, .footer-grid > *').forEach((el) => {
  el.classList.add('reveal');
  revealObserver.observe(el);
});

document.getElementById('year').textContent = new Date().getFullYear();
