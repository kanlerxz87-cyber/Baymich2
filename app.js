const STAR_SOURCE = 'https://guide.michelin.com/en/article/michelin-guide-ceremony/guide-michelin-california';
const GUIDE_YEAR = 2026;

async function loadData() {
  const [restaurants, hotels] = await Promise.all([
    fetch('data/restaurants.json').then((response) => {
      if (!response.ok) throw new Error('Could not load restaurant data');
      return response.json();
    }),
    fetch('data/hotels.json').then((response) => {
      if (!response.ok) throw new Error('Could not load hotel data');
      return response.json();
    })
  ]);
  return { restaurants, hotels };
}

function escapeHtml(value = '') {
  return String(value).replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[character]);
}

function sourceLink(url = STAR_SOURCE, label = 'MICHELIN ↗') {
  return `<a class="source-link" href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${label}</a>`;
}

function priceMarkup(restaurant) {
  if (!restaurant.pairPrice) return '<span class="missing">Unverified</span>';
  const priceSource = restaurant.menuUrl ? `<br><a class="source-link" href="${escapeHtml(restaurant.menuUrl)}" target="_blank" rel="noreferrer">Official menu source ↗</a>` : '';
  return `<details class="price-detail"><summary>${escapeHtml(restaurant.pairPrice)}</summary><p>${escapeHtml(restaurant.pairPriceNote)}${priceSource}</p></details>`;
}

function hoursMarkup(restaurant) {
  if (!restaurant.hours) return '<span class="missing">Unverified</span>';
  const note = restaurant.hoursNote || 'Exceptions unverified.';
  return `<span>${escapeHtml(restaurant.hours)}<small class="hours-note"> · ${escapeHtml(note)}</small></span>`;
}

function socialMarkup(restaurant = {}) {
  const labels = { youtube: 'YouTube ↗', tiktok: 'TikTok ↗', instagram: 'Instagram ↗' };
  if (!restaurant.social || !restaurant.social.length) {
    return '<span class="missing" title="No official social profile confirmed from an official venue source">Unverified</span>';
  }
  return restaurant.social.map((item) => {
    const label = labels[item.platform] || item.platform;
    return `<a class="source-link" href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`;
  }).join(' ');
}

function venueMarkup(restaurant) {
  const url = restaurant.restaurantUrl || restaurant.michelinUrl;
  if (!url) return '<span class="missing">Unverified</span>';
  const label = restaurant.restaurantUrl ? 'Official venue ↗' : 'MICHELIN profile ↗';
  return `<a class="venue-link" href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${label}</a>`;
}

function renderRestaurants(restaurants) {
  const search = document.querySelector('#restaurant-search').value.trim().toLowerCase();
  const star = document.querySelector('#star-filter').value;
  const city = document.querySelector('#city-filter').value;
  const shown = restaurants.filter((restaurant) => {
    const matchesSearch = `${restaurant.name} ${restaurant.city}`.toLowerCase().includes(search);
    return matchesSearch && (star === 'all' || restaurant.stars === Number(star)) && (city === 'all' || restaurant.city === city);
  });
  document.querySelector('#result-count').textContent = `Showing ${shown.length} of ${restaurants.length}`;
  document.querySelector('#restaurant-rows').innerHTML = shown.map((restaurant) => `
    <tr>
      <td class="name-cell"><a class="venue-link" href="${escapeHtml(restaurant.michelinUrl)}" target="_blank" rel="noreferrer">${escapeHtml(restaurant.name)} ↗</a>${restaurant.address ? `<div class="place">${escapeHtml(restaurant.address)}</div>` : ''}</td>
      <td>${escapeHtml(restaurant.city)}</td>
      <td><span class="star-badge">${'✳'.repeat(restaurant.stars)} <span>${restaurant.statusYear || GUIDE_YEAR} · ${restaurant.stars} ${restaurant.stars === 1 ? 'star' : 'stars'}</span></span></td>
      <td>${restaurant.priceBand ? escapeHtml(restaurant.priceBand) : '<span class="missing">Unverified</span>'}</td>
      <td>${priceMarkup(restaurant)}</td>
      <td>${hoursMarkup(restaurant)}</td>
      <td>${socialMarkup(restaurant)}</td>
      <td>${sourceLink(restaurant.statusSource || STAR_SOURCE, `Official ${restaurant.statusYear || GUIDE_YEAR} star list ↗`)}</td>
    </tr>`).join('');
  document.querySelector('#restaurant-cards').innerHTML = shown.map((restaurant) => `
    <article class="restaurant-card">
      <div class="restaurant-card-top"><div><h3>${escapeHtml(restaurant.name)}</h3><div class="place">${escapeHtml(restaurant.city)}</div></div><span class="star-badge">${'✳'.repeat(restaurant.stars)} ${restaurant.statusYear || GUIDE_YEAR} · ${restaurant.stars} ${restaurant.stars === 1 ? 'star' : 'stars'}</span></div>
      <div class="restaurant-card-info">
        <div><label>DINNER FOR TWO</label>${priceMarkup(restaurant)}</div>
        <div><label>OPEN DAYS / HOURS</label>${hoursMarkup(restaurant)}</div>
        <div><label>OFFICIAL SOCIAL</label>${socialMarkup(restaurant)}</div>
        <div><label>VENUE LINK</label>${venueMarkup(restaurant)}</div>
      </div>
      <div class="restaurant-card-bottom">${sourceLink(restaurant.michelinUrl || STAR_SOURCE, 'Official MICHELIN profile ↗')}${restaurant.menuUrl ? `<a class="source-link" href="${escapeHtml(restaurant.menuUrl)}" target="_blank" rel="noreferrer">Price source ↗</a>` : ''}</div>
    </article>`).join('');
}

function renderHotels(hotels) {
  document.querySelector('#hotel-grid').innerHTML = hotels.map((hotel) => `
    <article class="hotel-card">
      <div class="hotel-top"><span class="key-stars">${'✦'.repeat(hotel.keys)}<span class="sr-only"> ${hotel.keys} MICHELIN Keys</span></span><span class="hotel-area">${escapeHtml(hotel.area)}</span></div>
      <h3>${escapeHtml(hotel.name)}</h3><div class="hotel-address">${escapeHtml(hotel.address)}</div>
      <div class="hotel-metric"><span>Rooms</span><strong>${escapeHtml(hotel.rooms || 'Not verified')}</strong></div>
      <div class="hotel-metric"><span>Stay price (from)</span><strong>${hotel.rateFrom ? escapeHtml(hotel.rateFrom) : '<span class="missing">Unverified</span>'}</strong></div>
      ${hotel.rateNote ? `<p class="hotel-rate-note">${escapeHtml(hotel.rateNote)}</p>` : ''}
      ${sourceLink(hotel.source, 'MICHELIN hotel profile ↗')}
    </article>`).join('');
}

function renderClusters(restaurants) {
  const counts = restaurants.reduce((result, restaurant) => {
    result[restaurant.city] = (result[restaurant.city] || 0) + 1;
    return result;
  }, {});
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  document.querySelector('#cluster-list').innerHTML = sorted.map(([city, count]) => `
    <div class="cluster-row"><i class="cluster-dot"></i><span class="cluster-city">${escapeHtml(city)}</span><span class="cluster-count">${count} ${count === 1 ? 'entry' : 'entries'}</span></div>`).join('');
}

function initialize(data) {
  const { restaurants, hotels } = data;
  document.querySelector('#three-count').textContent = restaurants.filter((restaurant) => restaurant.stars === 3).length;
  document.querySelector('#two-count').textContent = restaurants.filter((restaurant) => restaurant.stars === 2).length;
  document.querySelector('#one-count').textContent = restaurants.filter((restaurant) => restaurant.stars === 1).length;
  const citySelect = document.querySelector('#city-filter');
  [...new Set(restaurants.map((restaurant) => restaurant.city))].sort().forEach((city) => {
    const option = document.createElement('option');
    option.value = city;
    option.textContent = city;
    citySelect.append(option);
  });
  ['#restaurant-search', '#star-filter', '#city-filter'].forEach((selector) => {
    document.querySelector(selector).addEventListener('input', () => renderRestaurants(restaurants));
    document.querySelector(selector).addEventListener('change', () => renderRestaurants(restaurants));
  });
  renderRestaurants(restaurants);
  renderHotels(hotels);
  renderClusters(restaurants);
}

loadData().then(initialize).catch((error) => {
  document.querySelector('#restaurant-rows').innerHTML = `<tr><td colspan="8">${escapeHtml(error.message)}. Run the site through a local HTTP server (not file://).</td></tr>`;
});
