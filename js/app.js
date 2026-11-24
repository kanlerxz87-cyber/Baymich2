// ============================================================================
// Baymich2 — shared UI helpers
// ============================================================================
(function () {
  const STATUS_ORDER = { "3 MICHELIN Stars": 0, "2 MICHELIN Stars": 1, "1 MICHELIN Star": 2, "Bib Gourmand": 3, Listed: 4 };

  function starsHtml(r) {
    if (r.stars === 3) return '<span class="stars-cell star-3">★★★ 3-star</span>';
    if (r.stars === 2) return '<span class="stars-cell star-2">★★ 2-star</span>';
    if (r.stars === 1) return '<span class="stars-cell star-1">★ 1-star</span>';
    if (r.status === "Bib Gourmand") return '<span class="stars-cell bib">Bib Gourmand</span>';
    return '<span class="stars-cell listed">Listed only</span>';
  }

  function priceHtml(r) {
    const sym = r.michelinPrice || "—";
    const est = r.estPrice2Adults || "";
    let out = '<span class="price-cell">' + sym + "</span>";
    if (est) out += ' <span class="price-est">' + est + "</span>";
    else out += ' <span class="blank">total price unverified</span>';
    return out;
  }

  function socialHtml(r) {
    const s = r.social || {};
    let out = "";
    if (s.ig) out += '<a href="' + s.ig + '" target="_blank" rel="noopener" title="Instagram">IG</a>';
    else out += '<span class="blank">IG n/a</span>';
    if (s.yt) out += '<a href="' + s.yt + '" target="_blank" rel="noopener" title="YouTube">YT</a>';
    else out += '<span class="blank">YT n/a</span>';
    if (s.tt) out += '<a href="' + s.tt + '" target="_blank" rel="noopener" title="TikTok">TT</a>';
    else out += '<span class="blank">TT n/a</span>';
    return out;
  }

  function hoursHtml(r) {
    const h = r.hours || {};
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    let parts = [];
    let any = false;
    for (const d of days) {
      const v = h[d];
      if (!v || v === "unverified") {
        parts.push('<span class="unverified">' + d + ": —</span>");
      } else {
        any = true;
        parts.push('<span>' + d + ": " + v + "</span>");
      }
    }
    if (!any) return '<span class="blank">Hours unverified — see official site</span>';
    return parts.join(" ");
  }

  function webHtml(r) {
    if (r.website) return '<a href="' + r.website + '" target="_blank" rel="noopener">Official site</a>';
    return '<span class="blank">—</span>';
  }

  function sourceHtml(r) {
    return '<div class="source small"><strong>Source:</strong> <a href="' + r.source + '" target="_blank" rel="noopener">MICHELIN Guide official page</a>' +
      (r.notes ? ' <span class="unverified">· ' + r.notes + "</span>" : "") + "</div>";
  }

  function sortRestaurants(list) {
    return list.slice().sort((a, b) => {
      const sa = STATUS_ORDER[a.status] ?? 99;
      const sb = STATUS_ORDER[b.status] ?? 99;
      if (sa !== sb) return sa - sb;
      return (a.name || "").localeCompare(b.name || "");
    });
  }

  function renderTable(containerId, list) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const sorted = sortRestaurants(list);
    let rows = "";
    for (const r of sorted) {
      rows += "<tr>";
      rows += '<td class="name-cell"><a href="' + r.website + '" target="_blank" rel="noopener">' + escapeHtml(r.name) + "</a></td>";
      rows += '<td>' + escapeHtml(r.region) + '</td>';
      rows += '<td>' + escapeHtml(r.city) + '</td>';
      rows += '<td>' + escapeHtml(r.address) + '</td>';
      rows += '<td>' + starsHtml(r) + '</td>';
      rows += '<td>' + escapeHtml(r.cuisine) + '</td>';
      rows += '<td>' + priceHtml(r) + '</td>';
      rows += '<td>' + hoursHtml(r) + '</td>';
      rows += '<td class="web-cell">' + webHtml(r) + '</td>';
      rows += '<td class="social-cell">' + socialHtml(r) + '</td>';
      rows += "</tr>";
    }
    container.innerHTML = '<table><thead><tr>' +
      '<th>Restaurant</th><th>Region</th><th>City</th><th>Address</th>' +
      '<th>Michelin status</th><th>Cuisine</th><th>Price (MICHELIN)</th>' +
      '<th>Hours / days open</th><th>Official link</th><th>Social (IG / YT / TT)</th>' +
      '</tr></thead><tbody>' + rows + "</tbody></table>";
  }

  function escapeHtml(t) {
    if (t == null) return "";
    return String(t)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  window.Baymich = { starsHtml, priceHtml, socialHtml, hoursHtml, webHtml, renderTable, sortRestaurants, escapeHtml };
})();
