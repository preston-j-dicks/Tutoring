/**
 * FissionLab Universal Navigation Component
 * Inject into every page via: <div id="nav-root"></div><script src="/nav-component.js"></script>
 * Depth-aware: automatically computes correct relative paths.
 */
(function () {
  var path = window.location.pathname;
  var segments = path.replace(/^\//, '').split('/').filter(Boolean);

  // depth 0 = root (index.html), depth 1 = /blog/ etc, depth 2 = /community/resources/
  var depth = segments.length;
  if (path.endsWith('.html')) depth = Math.max(0, depth - 1);

  function base(d) {
    if (d <= 0) return '/';
    return '../'.repeat(d);
  }
  var b = base(depth);

  // Is this the root?
  var isRoot = (depth === 0 || path === '/' || path === '/index.html');

  var navLinks = [
    { label: 'Home',       href: isRoot ? '#' : b + 'index.html',                  key: 'home' },
    { label: 'Community',  href: b + 'community/',                                  key: 'community' },
    { label: 'Resources',  href: b + 'community/resources/',                        key: 'resources' },
    { label: 'Blog',       href: b + 'blog/',                                       key: 'blog' },
    { label: 'Bookshelf',  href: b + 'community/bookshelf/',                        key: 'bookshelf' },
    { label: 'Products',   href: b + 'community/products/',                         key: 'products' },
    { label: 'About',      href: isRoot ? '#about' : b + 'index.html#about',        key: 'about' },
  ];

  var subjectsItems = [
    { label: '&#9883; AFOQT Prep',    href: b + 'community/' },
    { label: '&#128300; Physics',      href: b + 'community/physics/' },
    { label: '&#129302; AI / ML / DL', href: b + 'community/ai-ml/' },
    { label: '&#128221; SAT / ACT',    href: b + 'community/sat-act/' },
    { label: '&#128208; Mathematics',  href: b + 'community/mathematics/' },
  ];

  var calendlyURL = 'https://calendly.com/preston-j-dicks/introductory-meeting';

  function isActive(key) {
    var p = path.toLowerCase();
    if (key === 'home'      && (p === '/' || p.endsWith('/index.html') && depth === 0)) return true;
    if (key === 'tutoring'  && (p.includes('/students') || (isRoot && p.includes('#services')))) return true;
    if (key === 'community' && p.includes('/community/') && !p.includes('/resources') && !p.includes('/bookshelf') && !p.includes('/products') && !p.includes('/practice') && !p.includes('/forum') && !p.includes('/about') && !p.includes('/downloads') && !p.includes('/app')) return true;
    if (key === 'resources' && p.includes('/community/resources')) return true;
    if (key === 'blog'      && p.includes('/blog')) return true;
    if (key === 'bookshelf' && p.includes('/bookshelf')) return true;
    if (key === 'products'  && p.includes('/products')) return true;
    if (key === 'about'     && p.includes('#about')) return true;
    return false;
  }

  // Build desktop nav: Home | Subjects dropdown | Community | Resources | Blog | Bookshelf | Products | About
  var navHTML = '<nav id="fl-nav">' +
    '<a href="' + (isRoot ? '/' : b) + '" class="nav-logo">' +
    '<span class="nav-atom-core" style="color:#c9a84c;font-size:18px;margin-right:6px;">&#9883;</span>' +
    '<span class="nav-logo-text">FISSION<span style="color:#c9a84c">LAB</span></span>' +
    '</a>' +
    '<div class="nav-links" id="fl-nav-links">';

  // Home link
  var homeActive = isActive('home');
  navHTML += '<a href="' + (isRoot ? '#' : b + 'index.html') + '"' +
    (homeActive ? ' class="fl-active" style="color:var(--gold,#c9a84c);border-bottom:2px solid var(--gold,#c9a84c);padding-bottom:2px"' : '') +
    '>Home</a>';

  // Subjects dropdown
  var subjectsDropdownPanel = '<div class="nav-dropdown-panel">';
  subjectsItems.forEach(function (item) {
    subjectsDropdownPanel += '<a href="' + item.href + '">' + item.label + '</a>';
  });
  subjectsDropdownPanel += '</div>';

  navHTML += '<div class="nav-dropdown">' +
    '<span class="nav-dropdown-label">Subjects <span class="dropdown-arrow">&#9660;</span></span>' +
    subjectsDropdownPanel +
    '</div>';

  // Remaining links
  navLinks.forEach(function (link) {
    var active = isActive(link.key);
    navHTML += '<a href="' + link.href + '"' + (active ? ' class="fl-active" style="color:var(--gold,#c9a84c);border-bottom:2px solid var(--gold,#c9a84c);padding-bottom:2px"' : '') + '>' + link.label + '</a>';
  });

  navHTML += '<a href="' + calendlyURL + '" target="_blank" class="nav-cta">Book Free Intro</a>' +
    '</div>' +
    '<button class="nav-hamburger" id="fl-hamburger" aria-label="Open menu">' +
    '<span></span><span></span><span></span>' +
    '</button>' +
    '</nav>';

  // Overlay: Home, then Subjects section, then remaining links
  var overlayHTML = '<div class="nav-overlay" id="fl-overlay">' +
    '<button class="nav-overlay-close" id="fl-overlay-close" aria-label="Close menu">&#x2715;</button>';

  overlayHTML += '<a href="' + (isRoot ? '#' : b + 'index.html') + '" onclick="document.getElementById(\'fl-overlay\').classList.remove(\'open\')">Home</a>';

  // Subjects section header in overlay
  overlayHTML += '<div class="overlay-subjects-section">' +
    '<span class="overlay-subjects-header">Subjects</span>';
  subjectsItems.forEach(function (item) {
    overlayHTML += '<a href="' + item.href + '" class="overlay-subjects-link" onclick="document.getElementById(\'fl-overlay\').classList.remove(\'open\')">' + item.label + '</a>';
  });
  overlayHTML += '</div>';

  navLinks.forEach(function (link) {
    overlayHTML += '<a href="' + link.href + '" onclick="document.getElementById(\'fl-overlay\').classList.remove(\'open\')">' + link.label + '</a>';
  });

  overlayHTML += '<a href="' + calendlyURL + '" target="_blank" class="overlay-cta" onclick="document.getElementById(\'fl-overlay\').classList.remove(\'open\')">Book Free Intro</a>' +
    '</div>';

  var navCSS = '<style id="fl-nav-css">' +
    '#fl-nav{position:fixed;top:0;left:0;right:0;z-index:200;background:rgba(10,22,40,0.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(201,168,76,0.15);height:64px;padding:0 8vw;display:flex;align-items:center;justify-content:space-between;}' +
    '#fl-nav .nav-logo{display:flex;align-items:center;text-decoration:none;color:#fff;font-size:1.05rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;}' +
    '#fl-nav .nav-logo-text{letter-spacing:0.12em}' +
    '#fl-nav-links{display:flex;gap:1.4rem;align-items:center}' +
    '#fl-nav-links a{font-size:0.75rem;font-weight:500;color:rgba(240,235,224,0.72);text-decoration:none;letter-spacing:0.06em;text-transform:uppercase;transition:color 0.2s;}' +
    '#fl-nav-links a:hover{color:#fff}' +
    '#fl-nav .nav-cta{background:#c9a84c!important;color:#0a1628!important;padding:7px 16px!important;border-radius:6px;font-weight:700!important;font-size:0.75rem!important;}' +
    '.nav-hamburger{display:none;background:none;border:none;cursor:pointer;padding:4px;color:#f0ebe0}' +
    '.nav-hamburger span{display:block;width:24px;height:2px;background:#f0ebe0;margin:5px 0}' +
    '.nav-overlay{display:none;position:fixed;inset:0;z-index:199;background:rgba(10,22,40,0.97);flex-direction:column;align-items:center;justify-content:center;gap:2.5rem;overflow-y:auto;padding:80px 2rem 40px}' +
    '.nav-overlay.open{display:flex}' +
    '.nav-overlay a{font-size:1.4rem;font-weight:600;color:#f0ebe0;text-decoration:none;letter-spacing:0.08em;text-transform:uppercase;transition:color 0.2s}' +
    '.nav-overlay a:hover{color:#c9a84c}' +
    '.nav-overlay .overlay-cta{background:#c9a84c;color:#0a1628!important;padding:14px 40px;border-radius:8px}' +
    '.nav-overlay-close{position:absolute;top:24px;right:8vw;background:none;border:none;cursor:pointer;color:#f0ebe0;font-size:2rem}' +
    '.overlay-subjects-section{display:flex;flex-direction:column;align-items:center;gap:1rem;width:100%}' +
    '.overlay-subjects-header{font-size:0.65rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:rgba(201,168,76,0.6);border-bottom:1px solid rgba(201,168,76,0.2);padding-bottom:8px;width:100%;text-align:center}' +
    '.overlay-subjects-link{font-size:1.1rem!important;color:rgba(240,235,224,0.82)!important;letter-spacing:0.05em!important}' +
    '.nav-dropdown{position:relative}' +
    '.nav-dropdown-label{cursor:pointer;display:flex;align-items:center;gap:4px;font-size:0.75rem;font-weight:500;color:rgba(240,235,224,0.72);text-decoration:none;letter-spacing:0.06em;text-transform:uppercase;transition:color 0.2s;}' +
    '.nav-dropdown:hover .nav-dropdown-label{color:#fff}' +
    '.nav-dropdown-panel{display:none;position:absolute;top:calc(100% + 8px);left:-12px;background:rgba(10,22,40,0.98);border:1px solid rgba(201,168,76,0.2);border-radius:8px;min-width:200px;padding:8px 0;z-index:300}' +
    '.nav-dropdown:hover .nav-dropdown-panel,.nav-dropdown-panel:hover{display:block}' +
    '.nav-dropdown-panel a{display:flex;align-items:center;gap:8px;padding:10px 16px;font-size:0.78rem;color:rgba(240,235,224,0.82);text-decoration:none;letter-spacing:0.04em;transition:background 0.15s,color 0.15s}' +
    '.nav-dropdown-panel a:hover{background:rgba(201,168,76,0.08);color:#c9a84c}' +
    '.dropdown-arrow{font-size:10px;color:rgba(201,168,76,0.6)}' +
    'body{padding-top:64px}' +
    '@media(max-width:900px){#fl-nav-links{display:none}.nav-hamburger{display:block}}' +
    '</style>';

  // Inject styles into head
  document.head.insertAdjacentHTML('beforeend', navCSS);

  // Inject nav into nav-root if present, otherwise into body start
  var root = document.getElementById('nav-root');
  if (root) {
    root.outerHTML = navHTML + overlayHTML;
  } else {
    document.body.insertAdjacentHTML('afterbegin', navHTML + overlayHTML);
  }

  // Wire hamburger
  document.addEventListener('DOMContentLoaded', function () {
    var ham = document.getElementById('fl-hamburger');
    var overlay = document.getElementById('fl-overlay');
    var closeBtn = document.getElementById('fl-overlay-close');
    if (ham && overlay) ham.addEventListener('click', function () { overlay.classList.add('open'); });
    if (closeBtn && overlay) closeBtn.addEventListener('click', function () { overlay.classList.remove('open'); });
  });

  // Also wire immediately for pages where DOMContentLoaded already fired
  (function wireNow() {
    var ham = document.getElementById('fl-hamburger');
    var overlay = document.getElementById('fl-overlay');
    var closeBtn = document.getElementById('fl-overlay-close');
    if (ham) ham.onclick = function () { if (overlay) overlay.classList.add('open'); };
    if (closeBtn) closeBtn.onclick = function () { if (overlay) overlay.classList.remove('open'); };
  })();
})();
