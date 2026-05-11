(function () {
  const tocNav = document.querySelector('.toc-sidebar nav');
  if (!tocNav) return;

  const tocLinks = tocNav.querySelectorAll('a');
  if (tocLinks.length === 0) return;

  const linkMap = new Map();
  tocLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      const id = href.slice(1);
      const heading = document.getElementById(id);
      if (heading) linkMap.set(heading, link);
    }
  });

  if (linkMap.size === 0) return;

  const headings = [...linkMap.keys()];
  const visible = new Set();
  let manualActive = null;       // user-clicked heading
  let manualTimeout = null;

  // --- Click: instantly highlight, suppress observer briefly ---
  tocNav.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;

    const href = link.getAttribute('href');
    if (!href || !href.startsWith('#')) return;

    const id = href.slice(1);
    const heading = document.getElementById(id);
    if (!heading) return;

    // Clear all, set clicked as active
    tocLinks.forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    manualActive = heading;

    // Suppress observer updates for 800ms (smooth scroll duration)
    if (manualTimeout) clearTimeout(manualTimeout);
    manualTimeout = setTimeout(() => {
      manualActive = null;
    }, 800);
  });

  // --- IntersectionObserver: track scroll position ---
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        visible.add(entry.target);
      } else {
        visible.delete(entry.target);
      }
    });

    // Don't update during manual click scroll
    if (manualActive) return;

    let activeHeading = null;
    for (const h of headings) {
      if (visible.has(h)) {
        activeHeading = h;
        break;
      }
    }

    if (!activeHeading) {
      for (let i = headings.length - 1; i >= 0; i--) {
        const rect = headings[i].getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.4) {
          activeHeading = headings[i];
          break;
        }
      }
    }

    tocLinks.forEach(link => link.classList.remove('active'));
    if (activeHeading && linkMap.has(activeHeading)) {
      linkMap.get(activeHeading).classList.add('active');
    }
  }, {
    rootMargin: '-15% 0px -70% 0px',
    threshold: 0,
  });

  headings.forEach(h => observer.observe(h));
})();
