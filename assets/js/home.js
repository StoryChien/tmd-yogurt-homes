/* 天母的優格｜精選待售 — homepage filter */
(function () {
  "use strict";
  var form = document.getElementById("filter-panel");
  if (!form) return;
  var toggle = document.querySelector(".filter-toggle");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".listing-card"));
  var empty = document.querySelector(".filter-empty");
  var result = document.querySelector("[data-filter-result]");
  var count = document.querySelector("[data-filter-count]");

  function inRange(v, range) {
    if (!range) return true;
    var p = range.split("-");
    var lo = p[0] === "" ? -Infinity : Number(p[0]);
    var hi = p[1] === "" || p[1] === undefined ? Infinity : Number(p[1]);
    return v >= lo && v < hi;
  }

  function apply() {
    var area = form.area.value;
    var price = form.price.value;
    var rooms = form.rooms.value;
    var parking = form.parking.value;
    var shown = 0;
    cards.forEach(function (c) {
      var ok = true;
      if (area && c.dataset.area !== area) ok = false;
      if (ok && !inRange(Number(c.dataset.price), price)) ok = false;
      if (ok && rooms) {
        var r = Number(c.dataset.rooms);
        ok = rooms === "4" ? r >= 4 : r === Number(rooms);
      }
      if (ok && parking && c.dataset.parking !== parking) ok = false;
      c.hidden = !ok;
      if (ok) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
    if (result) result.textContent = "共 " + shown + " 間";
    if (count) count.textContent = shown + " 間";
    var active = area || price || rooms || parking;
    form.classList.toggle("is-active", !!active);
    if (toggle) toggle.classList.toggle("is-active", !!active);
  }

  form.addEventListener("change", apply);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  form.addEventListener("reset", function () { setTimeout(apply, 0); });

  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
      form.classList.toggle("is-open", !open);
    });
  }
  apply();
})();
