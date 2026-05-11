(function () {
  const tocSidebar = document.querySelector('.toc-sidebar');
  if (!tocSidebar) return;

  const tocNav = tocSidebar.querySelector('nav');
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
  let manualActive = null;
  let manualTimeout = null;

  // Scroll the sidebar so the active link is visible
  function scrollSidebarToActive(link) {
    const sidebarRect = tocSidebar.getBoundingClientRect();
    const linkRect = link.getBoundingClientRect();
    if (linkRect.top < sidebarRect.top + 20) {
      tocSidebar.scrollBy({ top: linkRect.top - sidebarRect.top - 20, behavior: 'smooth' });
    } else if (linkRect.bottom > sidebarRect.bottom - 20) {
      tocSidebar.scrollBy({ top: linkRect.bottom - sidebarRect.bottom + 20, behavior: 'smooth' });
    }
  }

  function setActive(heading) {
    tocLinks.forEach(l => l.classList.remove('active'));
    if (heading && linkMap.has(heading)) {
      const link = linkMap.get(heading);
      link.classList.add('active');
      scrollSidebarToActive(link);
    }
  }

  // --- Click: instant highlight, suppress observer briefly ---
  tocNav.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;
    const href = link.getAttribute('href');
    if (!href || !href.startsWith('#')) return;
    const id = href.slice(1);
    const heading = document.getElementById(id);
    if (!heading) return;

    tocLinks.forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    scrollSidebarToActive(link);
    manualActive = heading;

    if (manualTimeout) clearTimeout(manualTimeout);
    manualTimeout = setTimeout(() => { manualActive = null; }, 800);
  });

  // --- IntersectionObserver ---
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        visible.add(entry.target);
      } else {
        visible.delete(entry.target);
      }
    });

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

    setActive(activeHeading);
  }, {
    rootMargin: '-15% 0px -70% 0px',
    threshold: 0,
  });

  headings.forEach(h => observer.observe(h));
})();
