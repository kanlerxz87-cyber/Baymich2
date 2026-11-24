// Client-side row filter for data tables. No network calls, no tracking.
(function () {
  document.querySelectorAll('input[data-filter]').forEach(function (input) {
    var table = document.getElementById(input.getAttribute('data-filter'));
    if (!table) return;
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      table.querySelectorAll('tbody tr').forEach(function (row) {
        row.style.display = !q || row.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
      });
    });
  });
})();
