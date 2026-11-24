// Baymich2 — Michelin SF Bay Area Guide app
// Loads data/restaurants.json and renders category tables.

(function () {
  const DATA_URL = 'data/restaurants.json';
  const HOTELS_URL = 'data/hotels.json';

  // Read ?category= from URL (e.g. restaurants.html?category=3-stars)
  function getParam(name) {
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
  }

  const STAR_LABEL = {
    3: '3 stars',
    2: '2 stars',
    1: '1 star',
    0: 'Listed (no star)'
  };

  function starsBadge(stars) {
    if (stars === 3) return '<span class="star star-3">3★</span>';
    if (stars === 2) return '<span class="star star-2">2★</span>';
    if (stars === 1) return '<span class="star star-1">1★</span>';
    return '<span class="star star-0">Listed</span>';
  }

  function statusBadge(verified) {
    if (verified) return '<span class="badge badge-verified">verified</span>';
    return '<span class="badge badge-unverified">unverified</span>';
  }

  function escapeHtml(text) {
    if (text == null) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
  }

  function linkOrBlank(url, label) {
    if (!url) return '<span class="link dim">—</span>';
    return '<a class="link" href="' + escapeHtml(url) + '" target="_blank" rel="noopener">' + escapeHtml(label || url) + '</a>';
  }

  function renderRestaurants(data, containerId, category) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Build the list of entries to show
    let entries = [];
    let heading = '';
    let intro = '';

    if (category === '3-stars' || category === '3star') {
      entries = data.restaurants.filter(r => r.stars === 3);
      heading = '3 Michelin Stars';
      intro = 'Exceptional cuisine, worth a special journey.';
    } else if (category === '2-stars' || category === '2star') {
      entries = data.restaurants.filter(r => r.stars === 2);
      heading = '2 Michelin Stars';
      intro = 'Excellent cooking, worth a detour.';
    } else if (category === '1-stars' || category === '1star') {
      entries = data.restaurants.filter(r => r.stars === 1);
      heading = '1 Michelin Star';
      intro = 'High quality cooking, worth a stop.';
    } else if (category === 'listed' || category === 'listed-only' || category === 'no-star') {
      entries = [];
      data.listedOnly.bibGourmand.forEach(r => entries.push(Object.assign({}, r, { distinctionLabel: 'Bib Gourmand' })));
      data.listedOnly.selected.forEach(r => entries.push(Object.assign({}, r, { distinctionLabel: 'Selected' })));
      heading = 'Listed in Guide (no star)';
      intro = data.listedOnly.note;
    } else {
      // default: all starred
      entries = data.restaurants.filter(r => r.stars > 0);
      heading = 'All Starred Restaurants';
      intro = data.summary.totalStarred + ' starred restaurants.';
    }

    entries.sort((a, b) => (b.stars || 0) - (a.stars || 0) || (a.name || '').localeCompare(b.name || ''));

    // Page header
    let html = '';
    html += '<h2>' + escapeHtml(heading) + ' <span class="badge badge-listed">' + entries.length + '</span></h2>';
    if (intro) html += '<p class="note-box">' + escapeHtml(intro) + '</p>';

    // Filters
    html += '<div class="filters">';
    html += '<span class="filter-pill active" onclick="filterTable(this, null)">All</span>';
    const cities = [...new Set(entries.map(e => e.city).filter(Boolean))].sort();
    cities.forEach(c => {
      html += '<span class="filter-pill" onclick="filterTable(this, \'' + escapeHtml(c) + '\')">' + escapeHtml(c) + '</span>';
    });
    html += '<input type="search" id="table-search" placeholder="Search name / cuisine / area…" onkeyup="searchTable(this.value)">';
    html += '</div>';

    // Table
    html += '<div class="table-wrap"><table id="restaurant-table">';
    html += '<thead><tr>';
    html += '<th>Restaurant</th>';
    html += '<th>Stars</th>';
    html += '<th>Area / City</th>';
    html += '<th>Cuisine</th>';
    html += '<th>Price (MICHELIN)</th>';
    html += '<th>Official website</th>';
    html += '<th>Phone</th>';
    html += '<th>Open days / hours</th>';
    html += '<th>Exceptions</th>';
    html += '<th>Instagram</th>';
    html += '<th>Source</th>';
    html += '<th>Status</th>';
    html += '</tr></thead><tbody>';

    entries.forEach(r => {
      const verified = r.hoursVerified && r.socialVerified;
      const rowStars = r.distinction ? (r.distinction === 'Bib Gourmand' ? 'bib' : 'listed') : starsBadge(r.stars);
      const starsCell = r.distinction ? '<span class="star star-0 bib">Bib</span>' : starsBadge(r.stars);
      const area = r.neighborhood ? (r.neighborhood + ', ' + r.city) : (r.city || '—');
      html += '<tr data-city="' + escapeHtml(r.city || '') + '" data-name="' + escapeHtml((r.name || '').toLowerCase()) + '" data-cuisine="' + escapeHtml((r.cuisine || '').toLowerCase()) + '">';
      html += '<td class="name-cell">' + escapeHtml(r.name) + '</td>';
      html += '<td>' + starsCell + '</td>';
      html += '<td>' + escapeHtml(area) + '</td>';
      html += '<td>' + escapeHtml(r.cuisine || '—') + '</td>';
      html += '<td class="price nowrap">' + escapeHtml(r.price || '—') + '</td>';
      html += '<td>' + linkOrBlank(r.website, 'website') + '</td>';
      html += '<td>' + escapeHtml(r.phone || '—') + '</td>';
      html += '<td>' + escapeHtml(r.hours || '—') + '</td>';
      html += '<td>' + escapeHtml(r.exceptions || '—') + '</td>';
      html += '<td>' + linkOrBlank(r.instagram, r.instagramHandle || 'Instagram') + '</td>';
      html += '<td>' + linkOrBlank(r.source, 'MICHELIN') + '</td>';
      html += '<td>' + statusBadge(verified) + '</td>';
      html += '</tr>';
    });

    html += '</tbody></table></div>';

    // Footnote about verification
    html += '<p class="note-box warn-box"><strong>Verification note:</strong> Every row links to its official MICHELIN Guide detail page (source column). Values that could not be confirmed from an official source are left blank and flagged unverified. No prices or hours were inferred.</p>';

    container.innerHTML = html;
    window._currentEntries = entries;
  }

  window.filterTable = function (el, city) {
    document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
    el.classList.add('active');
    const rows = document.querySelectorAll('#restaurant-table tbody tr');
    const term = (document.getElementById('table-search') || {}).value || '';
    rows.forEach(row => {
      const matchCity = city === null || row.getAttribute('data-city') === city;
      const text = (row.getAttribute('data-name') + ' ' + row.getAttribute('data-cuisine')).toLowerCase();
      const matchText = term === '' || text.includes(term.toLowerCase());
      row.style.display = (matchCity && matchText) ? '' : 'none';
    });
  };

  window.searchTable = function (term) {
    const rows = document.querySelectorAll('#restaurant-table tbody tr');
    let activeCity = null;
    document.querySelectorAll('.filter-pill.active').forEach(p => {
      // determine city from text content except 'All'
    });
    // re-apply using current filter: find which city pill is active
    const active = document.querySelector('.filter-pill.active');
    const cityLabel = active && active.textContent.trim() !== 'All' ? active.textContent.trim() : null;
    rows.forEach(row => {
      const matchCity = cityLabel === null || row.getAttribute('data-city') === cityLabel;
      const text = (row.getAttribute('data-name') + ' ' + row.getAttribute('data-cuisine')).toLowerCase();
      const matchText = term === '' || text.includes(term.toLowerCase());
      row.style.display = (matchCity && matchText) ? '' : 'none';
    });
  };

  // Load + render
  function init() {
    const category = getParam('category') || 'all';
    fetch(DATA_URL)
      .then(r => { if (!r.ok) throw new Error('Failed to load ' + DATA_URL); return r.json(); })
      .then(data => {
        renderRestaurants(data, 'restaurants-container', category);
        // set active category pill in header nav if present
        document.querySelectorAll('nav a').forEach(a => {
          if (a.href.includes('category=' + category)) a.classList.add('active');
        });
      })
      .catch(err => {
        const container = document.getElementById('restaurants-container');
        if (container) container.innerHTML = '<div class="empty">Failed to load restaurant data: ' + escapeHtml(err.message) + '</div>';
        console.error(err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
