
(function () {
  "use strict";

  var root = document.documentElement.dataset.root || "";
  var READ_KEY = "aec-read-v1";
  var THEME_KEY = "aec-theme-v1";

  function loadRead() {
    try { return new Set(JSON.parse(localStorage.getItem(READ_KEY) || "[]")); }
    catch (_) { return new Set(); }
  }
  function saveRead(set) {
    try { localStorage.setItem(READ_KEY, JSON.stringify(Array.from(set))); } catch (_) {}
  }

  var read = loadRead();

  function lessonInputs() {
    return Array.prototype.slice.call(
      document.querySelectorAll('input[type="checkbox"][data-lesson]')
    );
  }

  function uniqueIds(inputs) {
    var ids = new Set();
    inputs.forEach(function (input) { ids.add(input.dataset.lesson); });
    return ids;
  }

  function updateProgress() {
    var inputs = lessonInputs();
    var ids = uniqueIds(inputs);
    var total = ids.size;
    var done = 0;
    ids.forEach(function (id) { if (read.has(id)) done++; });
    var pct = total ? Math.round((done / total) * 100) : 0;

    var fill = document.getElementById("progress-fill");
    if (fill) fill.style.width = pct + "%";
    var label = document.getElementById("progress-label");
    if (label) label.textContent = done + " of " + total + " lessons read";
    var top = document.getElementById("progress-text");
    if (top) top.textContent = pct + "%";

    var homeFill = document.getElementById("home-progress-fill");
    if (homeFill) homeFill.style.width = pct + "%";
    var homeText = document.getElementById("home-progress-text");
    if (homeText) homeText.textContent = done + " of " + total + " lessons read";

    document.querySelectorAll("[data-nav-count]").forEach(function (el) {
      var moduleNum = el.dataset.navCount;
      var moduleInputs = inputs.filter(function (input) {
        return input.dataset.module === moduleNum;
      });
      var moduleIds = uniqueIds(moduleInputs);
      var moduleDone = 0;
      moduleIds.forEach(function (id) { if (read.has(id)) moduleDone++; });
      el.textContent = moduleDone + "/" + moduleIds.size;
    });

    document.querySelectorAll("[data-card-module]").forEach(function (card) {
      var moduleNum = card.dataset.cardModule;
      var moduleInputs = inputs.filter(function (input) {
        return input.dataset.module === moduleNum;
      });
      var moduleIds = uniqueIds(moduleInputs);
      var moduleDone = 0;
      moduleIds.forEach(function (id) { if (read.has(id)) moduleDone++; });
      var cardFill = card.querySelector(".card-progress-fill, .module-progress-fill");
      if (cardFill) {
        cardFill.style.width = (moduleIds.size ? Math.round((moduleDone / moduleIds.size) * 100) : 0) + "%";
      }
      var cardText = card.querySelector(".card-progress-text, .module-progress-text");
      if (cardText) cardText.textContent = moduleDone + "/" + moduleIds.size + " read";
    });
  }

  var inputs = lessonInputs();
  inputs.forEach(function (input) {
    input.checked = read.has(input.dataset.lesson);
    input.addEventListener("change", function () {
      if (input.checked) read.add(input.dataset.lesson);
      else read.delete(input.dataset.lesson);
      saveRead(read);
      inputs.forEach(function (other) {
        if (other.dataset.lesson === input.dataset.lesson) other.checked = input.checked;
      });
      updateProgress();
    });
  });
  updateProgress();

  // Theme
  var themeToggle = document.getElementById("theme-toggle");
  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    if (themeToggle) themeToggle.textContent = theme === "dark" ? "☀️" : "🌙";
    try { localStorage.setItem(THEME_KEY, theme); } catch (_) {}
  }
  var savedTheme = null;
  try { savedTheme = localStorage.getItem(THEME_KEY); } catch (_) {}
  if (!savedTheme) {
    savedTheme = (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }
  applyTheme(savedTheme);
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
    });
  }

  // Mobile sidebar
  var menuToggle = document.getElementById("menu-toggle");
  var overlay = document.getElementById("sidebar-overlay");
  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      document.body.classList.toggle("sidebar-open");
    });
  }
  if (overlay) overlay.addEventListener("click", function () {
    document.body.classList.remove("sidebar-open");
  });
  document.querySelectorAll(".sidebar a").forEach(function (link) {
    link.addEventListener("click", function () {
      document.body.classList.remove("sidebar-open");
    });
  });

  // Mark a module as read / unread
  document.querySelectorAll("[data-mark-module]").forEach(function (button) {
    button.addEventListener("click", function () {
      var moduleNum = button.dataset.markModule;
      var moduleInputs = lessonInputs().filter(function (input) {
        return input.dataset.module === moduleNum;
      });
      var ids = uniqueIds(moduleInputs);
      var allDone = true;
      ids.forEach(function (id) { if (!read.has(id)) allDone = false; });
      ids.forEach(function (id) {
        if (allDone) read.delete(id); else read.add(id);
      });
      saveRead(read);
      lessonInputs().forEach(function (input) {
        input.checked = read.has(input.dataset.lesson);
      });
      updateProgress();
      button.textContent = allDone ? "Mark module as read" : "Mark module as unread";
    });
  });

  // Search
  var search = document.getElementById("search");
  var results = document.getElementById("search-results");
  var searchIndex = null;
  var loadingIndex = false;
  var selected = -1;
  var currentResults = [];

  function loadSearchIndex() {
    if (searchIndex) return Promise.resolve(searchIndex);
    if (loadingIndex) {
      return new Promise(function (resolve) {
        var timer = setInterval(function () {
          if (searchIndex) { clearInterval(timer); resolve(searchIndex); }
        }, 60);
      });
    }
    loadingIndex = true;
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = root + "assets/search-index.js";
      script.onload = function () {
        searchIndex = window.SEARCH_INDEX || [];
        loadingIndex = false;
        resolve(searchIndex);
      };
      script.onerror = function () {
        loadingIndex = false;
        reject(new Error("search index failed to load"));
      };
      document.head.appendChild(script);
    });
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }
  function highlight(text, terms) {
    var safe = escapeHtml(text);
    terms.forEach(function (term) {
      if (!term) return;
      safe = safe.replace(new RegExp("(" + escapeRegExp(escapeHtml(term)) + ")", "gi"), "<mark>$1</mark>");
    });
    return safe;
  }
  function snippet(text, terms) {
    var lower = text.toLowerCase();
    var positions = terms.map(function (term) { return lower.indexOf(term); })
      .filter(function (pos) { return pos >= 0; });
    var start = positions.length ? Math.max(0, Math.min.apply(null, positions) - 70) : 0;
    var slice = text.slice(start, start + 230);
    if (start > 0) slice = "…" + slice;
    if (start + 230 < text.length) slice += "…";
    return highlight(slice, terms);
  }
  function hideResults() {
    if (results) results.hidden = true;
    selected = -1;
    currentResults = [];
  }
  function renderResults(items, terms) {
    if (!results) return;
    if (!items.length) {
      results.innerHTML = '<div class="search-empty">No lessons found.</div>';
      results.hidden = false;
      return;
    }
    results.innerHTML = items.map(function (item, index) {
      return '<a class="search-result" data-index="' + index + '" href="' + root + item.url + '">' +
        '<div class="search-result-title">' + highlight(item.title, terms) + '</div>' +
        '<div class="search-result-meta">Module ' + item.module + ' · ' + escapeHtml(item.module_title) + '</div>' +
        '<div class="search-result-snippet">' + snippet(item.text, terms) + '</div>' +
        '</a>';
    }).join("");
    results.hidden = false;
    selected = -1;
    currentResults = items;
    results.querySelectorAll(".search-result").forEach(function (link) {
      link.addEventListener("mouseenter", function () {
        selected = Number(link.dataset.index);
        updateSelected();
      });
    });
  }
  function updateSelected() {
    if (!results) return;
    results.querySelectorAll(".search-result").forEach(function (link, index) {
      link.classList.toggle("active", index === selected);
    });
  }
  function runSearch(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { hideResults(); return; }
    loadSearchIndex().then(function (index) {
      var scored = [];
      index.forEach(function (item) {
        var title = item.title.toLowerCase();
        var tags = (item.tags || []).join(" ").toLowerCase();
        var text = item.text.toLowerCase();
        var all = true;
        var score = 0;
        terms.forEach(function (term) {
          var inTitle = title.indexOf(term) !== -1;
          var inTags = tags.indexOf(term) !== -1;
          var inText = text.indexOf(term) !== -1;
          if (!inTitle && !inTags && !inText) { all = false; return; }
          if (inTitle) score += 100;
          if (inTags) score += 20;
          if (inText) score += 5;
          if (title.indexOf(term) === 0) score += 50;
        });
        if (!all) return;
        if (title.indexOf(query.toLowerCase()) !== -1) score += 200;
        scored.push({ item: item, score: score });
      });
      scored.sort(function (a, b) { return b.score - a.score; });
      renderResults(scored.slice(0, 12).map(function (entry) { return entry.item; }), terms);
    }).catch(function () {
      if (results) {
        results.innerHTML = '<div class="search-empty">Search index could not be loaded.</div>';
        results.hidden = false;
      }
    });
  }

  if (search) {
    var timer = null;
    search.addEventListener("input", function () {
      clearTimeout(timer);
      var value = search.value.trim();
      if (value.length < 2) { hideResults(); return; }
      timer = setTimeout(function () { runSearch(value); }, 130);
    });
    search.addEventListener("focus", function () {
      if (search.value.trim().length >= 2) runSearch(search.value.trim());
    });
    search.addEventListener("keydown", function (event) {
      if (event.key === "Escape") { hideResults(); search.blur(); return; }
      if (!currentResults.length) return;
      if (event.key === "ArrowDown") {
        event.preventDefault();
        selected = Math.min(currentResults.length - 1, selected + 1);
        updateSelected();
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        selected = Math.max(0, selected - 1);
        updateSelected();
      } else if (event.key === "Enter") {
        event.preventDefault();
        var target = selected >= 0 ? currentResults[selected] : currentResults[0];
        if (target) window.location.href = root + target.url;
      }
    });
    document.addEventListener("click", function (event) {
      if (results && !results.hidden && !results.contains(event.target) && event.target !== search) {
        hideResults();
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "/" && document.activeElement !== search &&
          !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
        event.preventDefault();
        search.focus();
      }
    });
  }

  // Active TOC entry
  var tocLinks = Array.prototype.slice.call(
    document.querySelectorAll(".toc a[href^='#']")
  );
  if (tocLinks.length && "IntersectionObserver" in window) {
    var headingMap = {};
    tocLinks.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      var heading = document.getElementById(id);
      if (heading) headingMap[id] = link;
    });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (link) { link.classList.remove("active"); });
        var active = headingMap[entry.target.id];
        if (active) active.classList.add("active");
      });
    }, { rootMargin: "-80px 0px -70% 0px" });
    Object.keys(headingMap).forEach(function (id) {
      var heading = document.getElementById(id);
      if (heading) observer.observe(heading);
    });
  }
})();
