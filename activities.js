function escapeHtml(value = '') {
  return String(value).replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[character]);
}

function externalLink(url, label, className = '') {
  return `<a class="${className}" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)} ↗</a>`;
}

function socialLinks(activity) {
  if (!activity.socials?.length) {
    return '<span class="activity-unverified">No official YouTube, TikTok or Instagram link verified.</span>';
  }
  return `<div class="activity-social-links">${activity.socials.map((social) =>
    externalLink(social.url, social.label || social.platform, 'activity-social-link')
  ).join('')}</div>`;
}

function sourceLinks(activity) {
  return `<div class="activity-source-links">${activity.sources.map((source) =>
    externalLink(source.url, source.label, 'activity-source-link')
  ).join('')}</div>`;
}

function hoursMarkup(activity) {
  const flag = activity.flags?.length
    ? `<p class="activity-flag"><strong>Source conflict:</strong> ${escapeHtml(activity.flags.join(' '))}</p>`
    : '';
  return `<div class="activity-hours"><strong>Regular / current hours</strong><p>${escapeHtml(activity.hours)}</p><strong>Exceptions</strong><p>${escapeHtml(activity.exceptions)}</p>${flag}</div>`;
}

function priceMarkup(activity) {
  return `<div class="activity-price"><strong>Adult admission</strong><p>${escapeHtml(activity.adultAdmission)}</p><strong>Two-adult subtotal</strong><p class="two-adult-total">${escapeHtml(activity.twoAdultSubtotal)}</p><small>${escapeHtml(activity.priceNote)}</small></div>`;
}

function renderTable(activities) {
  const rows = activities.map((activity) => `
    <tr>
      <td class="activity-name-cell"><a class="activity-name" href="${escapeHtml(activity.officialUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(activity.name)} ↗</a><span>Verified ${escapeHtml(activity.verifiedOn)}</span></td>
      <td><strong>${escapeHtml(activity.city)}</strong><span class="activity-type">${escapeHtml(activity.category)}</span></td>
      <td>${hoursMarkup(activity)}</td>
      <td>${priceMarkup(activity)}</td>
      <td>${socialLinks(activity)}</td>
      <td>${sourceLinks(activity)}</td>
    </tr>`).join('');
  document.querySelector('#activity-rows').innerHTML = rows || '<tr><td colspan="6" class="no-activities">No activities match these filters.</td></tr>';
}

function renderCards(activities) {
  document.querySelector('#activity-cards').innerHTML = activities.map((activity) => `
    <article class="activity-card">
      <div class="activity-card-heading">
        <div><h3><a href="${escapeHtml(activity.officialUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(activity.name)} ↗</a></h3><p>${escapeHtml(activity.city)} · ${escapeHtml(activity.category)}</p></div>
        <span class="activity-verified">Verified ${escapeHtml(activity.verifiedOn)}</span>
      </div>
      <div class="activity-card-section"><h4>Open days, hours & exceptions</h4>${hoursMarkup(activity)}</div>
      <div class="activity-card-section"><h4>Admission for two adults</h4>${priceMarkup(activity)}</div>
      <div class="activity-card-section"><h4>Official social / video</h4>${socialLinks(activity)}</div>
      <div class="activity-card-section"><h4>Official sources</h4>${sourceLinks(activity)}</div>
    </article>`).join('');
}

function initializeActivities(activities) {
  const cityFilter = document.querySelector('#activity-city-filter');
  const categoryFilter = document.querySelector('#activity-category-filter');

  [...new Set(activities.map((activity) => activity.city))].sort().forEach((city) => {
    const option = document.createElement('option');
    option.value = city;
    option.textContent = city;
    cityFilter.append(option);
  });
  [...new Set(activities.map((activity) => activity.category))].sort().forEach((category) => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categoryFilter.append(option);
  });

  const update = () => {
    const search = document.querySelector('#activity-search').value.trim().toLocaleLowerCase();
    const city = cityFilter.value;
    const category = categoryFilter.value;
    const shown = activities.filter((activity) => {
      const searchable = `${activity.name} ${activity.city} ${activity.category} ${activity.address}`.toLocaleLowerCase();
      return searchable.includes(search)
        && (city === 'all' || activity.city === city)
        && (category === 'all' || activity.category === category);
    });
    document.querySelector('#activity-result-count').textContent = `Showing ${shown.length} of ${activities.length}`;
    renderTable(shown);
    renderCards(shown);
  };

  ['#activity-search', '#activity-city-filter', '#activity-category-filter'].forEach((selector) => {
    document.querySelector(selector).addEventListener('input', update);
    document.querySelector(selector).addEventListener('change', update);
  });
  update();
}

fetch('data/activities.json')
  .then((response) => {
    if (!response.ok) throw new Error('Could not load the activity data');
    return response.json();
  })
  .then(initializeActivities)
  .catch((error) => {
    document.querySelector('#activity-rows').innerHTML = `<tr><td colspan="6">${escapeHtml(error.message)}. Serve this directory over HTTP rather than opening the page as a file.</td></tr>`;
    document.querySelector('#activity-cards').innerHTML = `<p class="activity-load-error">${escapeHtml(error.message)}. Serve this directory over HTTP rather than opening the page as a file.</p>`;
  });
