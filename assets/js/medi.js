(function () {
  "use strict";

  var STORAGE_KEY = "omegleblog_continue";

  /* Mobile nav */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Save serial reading progress on post pages */
  var postEl = document.querySelector("article.post-page");
  if (postEl) {
    var series = postEl.getAttribute("data-series-slug");
    var url = postEl.getAttribute("data-post-url");
    var title = postEl.getAttribute("data-post-title");
    var part = postEl.getAttribute("data-series-part");
    var next = postEl.getAttribute("data-next-part");
    if (series && url) {
      try {
        var payload = {
          series: series,
          url: url,
          title: title || document.title,
          part: part ? parseInt(part, 10) : null,
          next: next || null,
          savedAt: Date.now()
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
        if (series === "late-bloom-stories") {
          localStorage.setItem(STORAGE_KEY + "_late-bloom", JSON.stringify(payload));
        }
      } catch (err) { /* private mode */ }
    }
  }

  /* Homepage / featured: Continue reading from localStorage */
  var continueBtn = document.getElementById("continue-reading-btn");
  var continueMeta = document.getElementById("continue-reading-meta");
  if (continueBtn) {
    try {
      var raw = localStorage.getItem(STORAGE_KEY + "_late-bloom") || localStorage.getItem(STORAGE_KEY);
      if (raw) {
        var data = JSON.parse(raw);
        if (data && data.url && data.series === "late-bloom-stories") {
          continueBtn.setAttribute("href", data.url);
          continueBtn.textContent = data.next ? "Continue next part →" : "Continue reading";
          if (data.next) {
            continueBtn.setAttribute("href", data.next);
          }
          if (continueMeta) {
            var label = data.part ? ("Part " + data.part) : "your last episode";
            continueMeta.textContent = "Resume from " + label;
            continueMeta.hidden = false;
          }
        }
      }
    } catch (err2) { /* ignore */ }
  }

  /* Auto TOC from h2 in .prose */
  var prose = document.querySelector(".post-body.prose");
  var lists = [
    document.getElementById("post-toc-list"),
    document.getElementById("post-toc-list-desktop")
  ].filter(Boolean);
  if (prose && lists.length) {
    var headings = prose.querySelectorAll("h2");
    if (headings.length >= 3) {
      headings.forEach(function (h, i) {
        if (!h.id) {
          h.id = "section-" + (i + 1);
        }
        lists.forEach(function (tocRoot) {
          var li = document.createElement("li");
          var a = document.createElement("a");
          a.href = "#" + h.id;
          a.textContent = h.textContent;
          li.appendChild(a);
          tocRoot.appendChild(li);
        });
      });
      var tocMobile = document.getElementById("post-toc");
      var tocDesktop = document.getElementById("post-toc-desktop");
      if (tocMobile) tocMobile.hidden = false;
      if (tocDesktop) tocDesktop.hidden = false;
    } else {
      var td = document.getElementById("post-toc-desktop");
      if (td) td.style.display = "none";
    }
  }
})();
