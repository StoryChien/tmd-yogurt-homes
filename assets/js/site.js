/* 天母的優格｜精選待售 — gallery + video embed */
(function () {
  "use strict";

  /* ---------- YouTube / Instagram embed ---------- */
  function youtubeId(url) {
    var m = String(url).match(
      /(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/
    );
    return m ? m[1] : null;
  }

  function instagramId(url) {
    var m = String(url).match(
      /instagram\.com\/(?:reel|p|tv)\/([A-Za-z0-9_-]+)/
    );
    return m ? m[1] : null;
  }

  function embedHtml(url) {
    var yt = youtubeId(url);
    if (yt) {
      return (
        '<iframe src="https://www.youtube.com/embed/' +
        yt +
        '" title="物件影片" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>'
      );
    }
    var ig = instagramId(url);
    if (ig) {
      var kind = /\/reel\//.test(url) ? "reel" : "p";
      return (
        '<iframe src="https://www.instagram.com/' +
        kind +
        "/" +
        ig +
        '/embed" title="Instagram 影片" allowtransparency="true" allow="encrypted-media" loading="lazy"></iframe>'
      );
    }
    return "";
  }

  function mountVideo(url) {
    var root = document.getElementById("video-frame");
    if (!root || !url) return;
    var html = embedHtml(url);
    if (!html) return;
    root.classList.remove("is-empty");
    root.innerHTML = html;
  }

  function initVideo() {
    var section = document.getElementById("video");
    if (!section) return;
    var preset = (section.getAttribute("data-video") || "").trim();
    if (preset) {
      mountVideo(preset);
      return;
    }
    var src = section.getAttribute("data-listing");
    if (!src) return;
    fetch(src, { cache: "no-cache" })
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (data) {
        if (data && data.video) mountVideo(data.video);
      })
      .catch(function () {});
  }

  /* ---------- Lightbox ---------- */
  function initLightbox() {
    var links = Array.prototype.slice.call(
      document.querySelectorAll("[data-gallery]")
    );
    if (!links.length) return;

    var items = links.map(function (a) {
      return {
        src: a.getAttribute("href"),
        alt: (a.querySelector("img") && a.querySelector("img").alt) || "",
        cap: a.getAttribute("data-caption") || "",
      };
    });

    var lb = document.createElement("div");
    lb.className = "lb";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "照片瀏覽");
    lb.innerHTML =
      '<button class="lb-btn lb-close" type="button" aria-label="關閉">×</button>' +
      '<button class="lb-btn lb-prev" type="button" aria-label="上一張">‹</button>' +
      '<img alt="">' +
      '<button class="lb-btn lb-next" type="button" aria-label="下一張">›</button>' +
      '<div class="lb-cap"></div>';
    document.body.appendChild(lb);

    var img = lb.querySelector("img");
    var cap = lb.querySelector(".lb-cap");
    var idx = 0;
    var startX = 0;

    function show(i) {
      idx = (i + items.length) % items.length;
      var it = items[idx];
      img.src = it.src;
      img.alt = it.alt;
      cap.textContent =
        (it.cap || it.alt) + "  " + (idx + 1) + "／" + items.length;
    }

    function open(i) {
      show(i);
      lb.classList.add("is-open");
      document.body.classList.add("lb-on");
      lb.querySelector(".lb-close").focus();
    }

    function close() {
      lb.classList.remove("is-open");
      document.body.classList.remove("lb-on");
      img.removeAttribute("src");
    }

    links.forEach(function (a, i) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        open(i);
      });
    });

    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () {
      show(idx - 1);
    });
    lb.querySelector(".lb-next").addEventListener("click", function () {
      show(idx + 1);
    });
    lb.addEventListener("click", function (e) {
      if (e.target === lb) close();
    });

    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });

    img.addEventListener("touchstart", function (e) {
      startX = e.changedTouches[0].screenX;
    }, { passive: true });
    img.addEventListener("touchend", function (e) {
      var dx = e.changedTouches[0].screenX - startX;
      if (dx > 50) show(idx - 1);
      if (dx < -50) show(idx + 1);
    }, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initVideo();
      initLightbox();
    });
  } else {
    initVideo();
    initLightbox();
  }
})();
