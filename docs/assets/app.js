(function(){
  var D = window.SITE_DATA;
  var page = document.body.getAttribute('data-page') || '';
  var pages = [
    ['index','Dashboard','index.html'],
    ['starred','Michelin Stars','starred.html'],
    ['hotels','Hotels','hotels.html'],
    ['questions','Questions','questions.html'],
    ['suggestions','Suggestions','suggestions.html'],
    ['flagged','Flagged for Review','flagged.html'],
    ['sources','Sources','sources.html']
  ];
  function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function unv(v,label){ return v ? esc(v) : '<span class="unv">UNVERIFIED'+(label?' – '+label:'')+'</span>'; }
  // header + footer
  var nav = pages.map(function(p){return '<a href="'+p[2]+'"'+(p[0]===page?' class="active"':'')+'>'+p[1]+'</a>';}).join('');
  var hdr = document.createElement('header'); hdr.className='top';
  hdr.innerHTML = '<a class="brand" href="index.html">Bay Area Michelin · Dashboard</a><nav class="menu">'+nav+'</nav>';
  document.body.insertBefore(hdr, document.body.firstChild);
  var ft = document.createElement('footer');
  ft.innerHTML = 'Data as of '+esc(D.asOf)+'. Michelin status from the official Michelin Guide California 2026 selection (announced 24 Jun 2026). Blank or "UNVERIFIED" fields have not been confirmed from an official source.';
  document.body.appendChild(ft);

  var starLabel = function(s){return s===3?'3 ★★★':s===2?'2 ★★':'1 ★';};
  var starBadge = function(s){return '<span class="badge b-star">'+starLabel(s)+'</span>';};

  if(page==='index'){
    var s = D.starred;
    var core = s.filter(function(r){return r.area==='Bay Area';});
    var wine = s.filter(function(r){return r.area!=='Bay Area';});
    var c = function(n){return s.filter(function(r){return r.stars===n && (r.area==='Bay Area'||true);}).length;};
    var coreByStar = {3:0,2:0,1:0}; core.forEach(function(r){coreByStar[r.stars]++;});
    var verifiedRows = s.filter(function(r){return r.verification && r.verification.indexOf('Verified:')===0;}).length;
    var partialRows = s.filter(function(r){return r.verification && r.verification.indexOf('Partial:')===0;}).length;
    var pendingRows = s.length - verifiedRows - partialRows;
    document.getElementById('app').innerHTML =
      '<h1>Bay Area Michelin Dashboard</h1>'+
      '<p class="sub">Starred restaurants, verified against official Michelin pages. Built 24 Nov 2026.</p>'+
      '<div class="cards">'+
        '<div class="card"><div class="num">'+core.length+'</div><div class="lbl">Core Bay Area starred restaurants</div><a class="go" href="starred.html">View table →</a></div>'+
        '<div class="card"><div class="num">'+coreByStar[3]+' / '+coreByStar[2]+' / '+coreByStar[1]+'</div><div class="lbl">Core Bay Area: 3★ / 2★ / 1★</div></div>'+
        '<div class="card"><div class="num">'+wine.length+'</div><div class="lbl">Adjacent wine country starred (shown separately)</div></div>'+
        '<div class="card"><div class="num">'+verifiedRows+' / '+partialRows+' / '+pendingRows+'</div><div class="lbl">Rows fully verified / partly verified / pending detail</div></div>'+
      '</div>'+
      '<h2>Executive summary</h2>'+
      '<div class="box"><ul class="clean">'+
        '<li><b>Scope:</b> 41 starred restaurants: 33 in the core Bay Area (SF, Oakland, Palo Alto, Atherton, San Mateo, Saratoga, Woodside, San Anselmo) and 8 in adjacent wine country. Michelin states 83 starred restaurants across California in 2026 (<a href="https://guide.michelin.com/us/en/article/michelin-guide-ceremony/guide-michelin-california" target="_blank" rel="noopener">source</a>).</li>'+
        '<li><b>San Francisco concentration:</b> 4 three-star, 6 two-star and 15 one-star restaurants in SF proper, the largest cluster in the region.</li>'+
        '<li><b>2026 changes (official):</b> Californios became the first Mexican restaurant with 3 stars; Enclos (Sonoma) is also new at 3 stars. New one-stars include Naides, Wolfsbane and Troubadour (Healdsburg).</li>'+
        '<li><b>What is verified:</b> star status for all 41 rows. Address, cuisine, price tier, phone and website for the 11 three- and two-star Bay Area rows. Hours are complete for 7, partial for 2 (weekend hours missing), and missing for 2.</li>'+
        '<li><b>What is NOT yet verified:</b> couple cost (no official dollar figures found), social links, one-star details, hotel rankings, Bib Gourmand list. These are blank on purpose. See <a href="questions.html">Questions</a>.</li>'+
        '<li><b>Ranking hotels by nearby stars:</b> not done yet. This needs Michelin Hotels data verified per hotel. See <a href="hotels.html">Hotels</a>.</li>'+
      '</ul></div>'+
      '<h2>Sections</h2>'+
      '<div class="cards">'+
        '<div class="card"><b>Michelin Stars</b><div class="small">Table of all starred rows with status, price, hours, links.</div><a class="go" href="starred.html">Open →</a></div>'+
        '<div class="card"><b>Hotels</b><div class="small">Method and status for ranking hotels by nearby Michelin restaurants.</div><a class="go" href="hotels.html">Open →</a></div>'+
        '<div class="card"><b>Questions</b><div class="small">What is answered, what is missing, and how to find it.</div><a class="go" href="questions.html">Open →</a></div>'+
        '<div class="card"><b>Suggestions</b><div class="small">Improvements to review. Nothing is changed until you choose.</div><a class="go" href="suggestions.html">Open →</a></div>'+
        '<div class="card"><b>Flagged for Review</b><div class="small">Source conflicts, data gaps and irregularities.</div><a class="go" href="flagged.html">Open →</a></div>'+
        '<div class="card"><b>Sources</b><div class="small">Every official source used, with links.</div><a class="go" href="sources.html">Open →</a></div>'+
      '</div>';
  }

  if(page==='starred'){
    var rows = D.starred;
    var html =
      '<h1>Michelin Starred Restaurants</h1>'+
      '<p class="sub">Source of star status: official Michelin Guide California 2026 selection. Use the search and filters to narrow. Blank cells are UNVERIFIED and are not estimated.</p>'+
      '<div class="toolbar">'+
        '<input id="q" type="search" placeholder="Search name, city, cuisine…">'+
        '<select id="f-star"><option value="">All stars</option><option value="3">3 ★★★</option><option value="2">2 ★★</option><option value="1">1 ★</option></select>'+
        '<select id="f-area"><option value="">All areas</option><option value="Bay Area">Core Bay Area</option><option value="Wine Country">Wine country (adjacent)</option></select>'+
        '<span class="small" id="count"></span>'+
      '</div>'+
      '<div class="tablewrap"><table class="responsive" id="tbl"><thead><tr>'+
        '<th>Restaurant</th><th>City / area</th><th>Michelin status</th><th>Cuisine</th><th>Price tier (Michelin)</th><th>Cost for 2 adults (total)</th>'+
        '<th>Days open · hours · exceptions</th><th>Address · phone</th><th>Links</th><th>Social (YouTube / TikTok / IG)</th><th>Verification</th>'+
      '</tr></thead><tbody></tbody></table></div>';
    document.getElementById('app').innerHTML = html;
    var tbody = document.querySelector('#tbl tbody');
    function render(){
      var q = document.getElementById('q').value.toLowerCase();
      var fs = document.getElementById('f-star').value;
      var fa = document.getElementById('f-area').value;
      var out = rows.filter(function(r){
        if(fs && String(r.stars)!==fs) return false;
        if(fa && r.area!==fa) return false;
        if(q && (r.name+' '+r.city+' '+(r.cuisine||'')).toLowerCase().indexOf(q)<0) return false;
        return true;
      });
      document.getElementById('count').textContent = out.length+' of '+rows.length+' rows';
      tbody.innerHTML = out.map(function(r){
        var status = starBadge(r.stars) + (r.isNew?' <span class="badge b-ok">NEW 2026</span>':'') + ' <span class="badge">Starred</span>';
        var hours = r.hours ? esc(r.hours)+(r.closedDays?'<div class="small">Closed: '+esc(r.closedDays)+'</div>':'')+(r.hoursExceptions?'<div class="small">'+esc(r.hoursExceptions)+'</div>':'') : '<span class="unv">UNVERIFIED</span>';
        var addr = r.address ? esc(r.address)+(r.phone?'<div class="small">'+esc(r.phone)+'</div>':'') : '<span class="unv">UNVERIFIED</span>';
        var links = '<a href="'+esc(r.michelinUrl)+'" target="_blank" rel="noopener">Michelin page</a>'+(r.website?'<br><a href="'+esc(r.website)+'" target="_blank" rel="noopener">Official website</a>':'');
        var ver = r.verification ? (r.verification.indexOf('Verified:')===0?'<span class="badge b-ok">Verified</span>':'<span class="badge b-warn">Partial</span>')+'<div class="small">'+esc(r.verification)+'</div>' : '<span class="badge b-bad">Pending</span><div class="small">Michelin status only (official article). Details not yet verified.</div>';
        return '<tr>'+
          '<td data-label="Restaurant"><b>'+esc(r.name)+'</b></td>'+
          '<td data-label="City / area">'+esc(r.city)+'<div class="small">'+esc(r.area)+'</div></td>'+
          '<td data-label="Michelin status">'+status+'</td>'+
          '<td data-label="Cuisine">'+(r.cuisine?esc(r.cuisine):'<span class="unv">UNVERIFIED</span>')+'</td>'+
          '<td data-label="Price tier">'+(r.priceTier?esc(r.priceTier):'<span class="unv">UNVERIFIED</span>')+'</td>'+
          '<td data-label="Cost for 2">'+(r.coupleCost?esc(r.coupleCost):'<span class="unv">UNVERIFIED – no official figure yet</span>')+'</td>'+
          '<td data-label="Hours">'+hours+'</td>'+
          '<td data-label="Address">'+addr+'</td>'+
          '<td data-label="Links">'+links+'</td>'+
          '<td data-label="Social">'+(r.social?'<a href="'+esc(r.social)+'">link</a>':'<span class="unv">NOT FOUND YET</span>')+'</td>'+
          '<td data-label="Verification">'+ver+'</td>'+
        '</tr>';
      }).join('');
    }
    ['q','f-star','f-area'].forEach(function(id){document.getElementById(id).addEventListener('input',render);document.getElementById(id).addEventListener('change',render);});
    render();
  }

  if(page==='flagged'){
    document.getElementById('app').innerHTML =
      '<h1>Flagged for Review</h1>'+
      '<p class="sub">Irregularities, source conflicts and gaps found during verification. Each needs a decision or a fix before it is treated as final.</p>'+
      '<div class="tablewrap"><table class="responsive"><thead><tr><th>ID</th><th>Type</th><th>Item</th><th>Detail</th><th>Sources</th><th>Suggested action</th></tr></thead><tbody>'+
      D.flagged.map(function(f){return '<tr><td data-label="ID">'+f.id+'</td><td data-label="Type"><span class="badge b-warn">'+esc(f.type)+'</span></td><td data-label="Item"><b>'+esc(f.item)+'</b></td><td data-label="Detail">'+esc(f.detail)+'</td><td data-label="Sources">'+f.sources.map(function(u){return '<a href="'+esc(u)+'" target="_blank" rel="noopener">link</a>';}).join('<br>')+'</td><td data-label="Action">'+esc(f.action)+'</td></tr>';}).join('')+
      '</tbody></table></div>';
  }

  if(page==='sources'){
    document.getElementById('app').innerHTML =
      '<h1>Sources</h1>'+
      '<p class="sub">Every value on the site must trace to one of these. Secondary sources are used only for cross-checks.</p>'+
      '<div class="tablewrap"><table class="responsive"><thead><tr><th>Source</th><th>Link</th><th>Used for</th></tr></thead><tbody>'+
      D.sources.map(function(s){return '<tr><td data-label="Source">'+esc(s.label)+'</td><td data-label="Link"><a href="'+esc(s.url)+'" target="_blank" rel="noopener">open</a></td><td data-label="Used for">'+esc(s.used)+'</td></tr>';}).join('')+
      '</tbody></table></div>'+
      '<h2>Verification log</h2>'+
      '<div class="box"><ul class="clean">'+
        '<li>Star status: the full official article list was read (3★ 10, 2★ 13, 1★ 60 = 83 statewide, matching the article\'s own total). Bay Area rows were checked against that list.</li>'+
        '<li>Restaurant details: 11 three- and two-star Bay Area Michelin pages were opened. Address, cuisine, price tier, phone, website and hours were read from each page.</li>'+
        '<li>Not yet done: one-star detail pages, couple-cost prices, social links, Bib Gourmand, hotels.</li>'+
      '</ul></div>';
  }

  if(page==='questions'){
    var answered = [
      ['Which Bay Area restaurants hold Michelin stars in 2026?','Answered. See Michelin Stars page. Source: official Michelin 2026 California selection.'],
      ['Which are NEW in 2026?','Answered. Californios and Enclos (3★); Naides, Wolfsbane and Troubadour (1★).'],
      ['Is the Michelin list the same as the Bay Area list?','Answered in part. The official list is statewide; the core Bay Area subset is defined on the site.'],
      ['What does the Michelin price symbol mean?','Answered. $ to $$$$ is a price tier shown by Michelin, not a dollar amount.']
    ];
    var open = [
      ['What is the cost for 2 adults at each restaurant?','Not answered. Needed for the budget table. Where to find it: each restaurant\'s official menu or booking page (OpenTable, Tock, Resy, SevenRooms). Only record exact prices with a link.'],
      ['Are hours for Birdsong, Sons & Daughters, Saison (weekend) and Commis (weekend) correct?','Partly answered. The fetched page did not include them. Re-check Michelin pages or the restaurant website.'],
      ['Which restaurants have an Instagram, TikTok or YouTube account?','Not answered. Needs a search per restaurant and a check that the account is the restaurant\'s own (the restaurant website often links its social accounts).'],
      ['What are the one-star details (address, hours, prices)?','Not answered. Only star status is verified. Each Michelin page needs to be read.'],
      ['Which Bib Gourmand and Michelin Recommended restaurants are in the Bay Area?','Not answered. Needs the official Bib Gourmand list for San Francisco and surroundings.'],
      ['How should hotels be ranked?','Not answered. Need: which hotels (Michelin Hotels list), the radius (e.g. 1 km / 5 km), and whether to count Bib and Recommended restaurants or only stars.'],
      ['Is Wine Country in scope?','Open decision. Included on the site as "adjacent" and shown separately. Confirm before ranking.'],
      ['Is Selby\'s in Atherton or Redwood City?','Open. Michelin says Atherton; Eater says Redwood City. Confirm on the Michelin page.'],
      ['Were Le Comptoir at Bar Crenn, O\' by Claude Le Tohic and The Shota removed as one-stars?','Open. Reported by Eater, not confirmed on an official page. Do not present as fact until checked.'],
      ['What is the repository license and should the site live in /docs?','Open. The repo has no license. Decide before publishing publicly.']
    ];
    document.getElementById('app').innerHTML =
      '<h1>Questions, Information and Answers</h1>'+
      '<p class="sub">What is known, what is missing, and how to find it. Decisions wait on the open items.</p>'+
      '<h2>Answered</h2><div class="box"><ol class="qa">'+answered.map(function(a){return '<li><b>'+esc(a[0])+'</b><br><span class="small">'+esc(a[1])+'</span></li>';}).join('')+'</ol></div>'+
      '<h2>Open – needed before decisions</h2><div class="box"><ol class="qa">'+open.map(function(a){return '<li><b>'+esc(a[0])+'</b><br><span class="small">'+esc(a[1])+'</span></li>';}).join('')+'</ol></div>';
  }

  if(page==='hotels'){
    document.getElementById('app').innerHTML =
      '<h1>Hotels</h1>'+
      '<p class="sub">Ranking hotels by nearby Michelin restaurants is not done yet. No hotel rows are listed because none have been verified.</p>'+
      '<div class="box"><b>Planned method (for review)</b><ol class="qa">'+
        '<li>Take the official Michelin Hotels list for the Bay Area (verified per hotel on Michelin\'s own page).</li>'+
        '<li>Use the verified restaurant coordinates from each Michelin page (Google Maps link from the page) and a fixed radius (choose 1 km or 5 km).</li>'+
        '<li>Count starred restaurants within the radius (3★ weighted highest), then Bib Gourmand, then Recommended. Show each count separately.</li>'+
        '<li>Show the hotel\'s own official website link. Do not use third-party rankings.</li>'+
      '</ol></div>'+
      '<div class="box"><b>Status:</b> <span class="badge b-bad">Not started</span> · See <a href="suggestions.html">Suggestions</a> and <a href="questions.html">Questions</a> for the decisions needed.</div>';
  }

  if(page==='suggestions'){
    var sug = [
      ['S1','Finish the couple-cost column from official menu or booking pages','Gives the requested budget view. Takes ~1 page per restaurant. Only exact published prices, with links.'],
      ['S2','Add social links (YouTube, TikTok, Instagram) from each restaurant\'s own website first','Keeps accounts verified. Add third-party accounts only if clearly labelled.'],
      ['S3','Finish one-star detail rows (address, hours, price tier, website)','Brings every row to Verified status.'],
      ['S4','Add a Bib Gourmand and Recommended table for the Bay Area','Adds the "rated" restaurants requested in the brief.'],
      ['S5','Build the hotel ranking after the scope and radius are chosen','Keeps the ranking transparent (show counts, not a single score).'],
      ['S6','Add a "Map" page (Michelin coordinates, clusters by area)','Visual clustering; coordinates must come from official pages.'],
      ['S7','Add a "last verified" date per row and a monthly re-check reminder','Michelin hours and selections change; keeps the data current.'],
      ['S8','Add filters for day of the week and open-now (after hours are complete)','Helps planning. Needs complete hours first.']
    ];
    document.getElementById('app').innerHTML =
      '<h1>Suggestions for Review</h1>'+
      '<p class="sub">Nothing below has been implemented. Choose the path you want (Approve, Modify or Reject), then the next session acts only on approved items.</p>'+
      '<div class="tablewrap"><table class="responsive"><thead><tr><th>ID</th><th>Suggestion</th><th>Why</th><th>Your decision</th></tr></thead><tbody>'+
      sug.map(function(s){return '<tr><td data-label="ID">'+s[0]+'</td><td data-label="Suggestion"><b>'+esc(s[1])+'</b></td><td data-label="Why">'+esc(s[2])+'</td><td data-label="Decision"><select><option>Pending</option><option>Approve</option><option>Modify</option><option>Reject</option></select></td></tr>';}).join('')+
      '</tbody></table></div>';
  }
})();
