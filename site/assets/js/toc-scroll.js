(function () {
  const tocLinks = document.querySelectorAll('.toc-sidebar nav a');
  if (tocLinks.length === 0) return;

  // Build a map: heading id → toc link element
  const linkMap = new Map();
  tocLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      const id = href.slice(1);
      const heading = document.getElementById(id);
      if (heading) {
        linkMap.set(heading, link);
      }
    }
  });

  if (linkMap.size === 0) return;

  const headings = [...linkMap.keys()];

  // Track which headings are currently above the viewport midpoint
  const visible = new Set();

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        visible.add(entry.target);
      } else {
        visible.delete(entry.target);
      }
    });

    // Find the first visible heading (topmost in the document)
    let activeHeading = null;
    for (const h of headings) {
      if (visible.has(h)) {
        activeHeading = h;
        break;
      }
    }

    // If no heading is fully in view, find the last one above the viewport
    if (!activeHeading) {
      for (let i = headings.length - 1; i >= 0; i--) {
        const rect = headings[i].getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.4) {
          activeHeading = headings[i];
          break;
        }
      }
    }

    // Apply active class
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
