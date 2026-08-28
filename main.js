/* =========================================================
   main.js — behaviour shared by every page.

   The old hash router is gone: each section is now its own
   document, so navigation is plain <a href> and the browser
   handles history, back/forward and bookmarking for free.
   ========================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ---------- Mobile menu ---------- */
  var nav = document.getElementById("nav");
  var toggle = document.querySelector(".menu-toggle");

  function closeMenu() {
    if (!nav) { return; }
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeMenu(); }
  });

  /* ---------- Card tilt ----------
     Only on devices with a real pointer. Touch gets the flat card,
     which is the right call: there is no hover to reveal it and the
     transform would only fight scrolling. */
  if (finePointer && !reduced) {
    var TILT = document.querySelectorAll(".card, .role, .news-item, .paper, .explore-card");

    Array.prototype.forEach.call(TILT, function (el) {
      el.classList.add("tilt");
      var frame = null;

      el.addEventListener("pointermove", function (e) {
        if (frame) { return; }
        frame = requestAnimationFrame(function () {
          frame = null;
          var b = el.getBoundingClientRect();
          var px = (e.clientX - b.left) / b.width;
          var py = (e.clientY - b.top) / b.height;
          el.style.setProperty("--ry", ((px - 0.5) * 2 * 7).toFixed(2) + "deg");
          el.style.setProperty("--rx", ((0.5 - py) * 2 * 7).toFixed(2) + "deg");
          el.style.setProperty("--sx", ((0.5 - px) * 24).toFixed(1) + "px");
          el.style.setProperty("--sy", ((0.5 - py) * 24 + 14).toFixed(1) + "px");
        });
      });

      el.addEventListener("pointerenter", function () { el.classList.add("is-tilting"); });

      el.addEventListener("pointerleave", function () {
        el.classList.remove("is-tilting");
        el.style.setProperty("--rx", "0deg");
        el.style.setProperty("--ry", "0deg");
      });
    });
  }

  /* ---------- Scroll reveal ---------- */
  if (!reduced && window.IntersectionObserver) {
    var targets = document.querySelectorAll(".card, .paper, .programme, .news-item, .role, .explore-card");
    Array.prototype.forEach.call(targets, function (el) { el.classList.add("reveal"); });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) { return; }
        var el = entry.target;
        setTimeout(function () { el.classList.add("in"); }, (i % 4) * 80);
        io.unobserve(el);
      });
    }, { threshold: 0.12 });

    Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
  }

  /* ---------- Contact form ----------
     Falls back to the visitor's mail client so an enquiry is never
     silently dropped. See contact.html for how to point this at a
     real endpoint instead. */
  var form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = document.getElementById("cname").value.trim();
      var email = document.getElementById("cemail").value.trim();
      var topic = document.getElementById("ctopic").value;
      var msg = document.getElementById("cmsg").value.trim();
      var out = document.getElementById("formMsg");

      if (!name || !email || !msg) {
        out.style.color = "#ffb4b4";
        out.textContent = "Fill in your name, email and message so we can reply.";
        return;
      }
      if (!/^\S+@\S+\.\S+$/.test(email)) {
        out.style.color = "#ffb4b4";
        out.textContent = "That email address doesn't look right — check it and try again.";
        return;
      }

      var body = "Name: " + name + "\nEmail: " + email + "\nTopic: " + topic + "\n\n" + msg;
      out.style.color = "var(--mint)";
      out.textContent = "Opening your email app to send this — press send there and it reaches us.";
      window.location.href = "mailto:customer_service@genolytix.co.in"
        + "?subject=" + encodeURIComponent("[" + topic + "] " + name)
        + "&body=" + encodeURIComponent(body);
    });
  }

  /* ---------- Footer year ---------- */
  var year = document.getElementById("year");
  if (year) { year.textContent = new Date().getFullYear(); }

  /* ---------- Legacy hash links ----------
     Anything already shared as genolytix.co.in/#research keeps
     working and lands on the real page. */
  var LEGACY = {
    "#work": "/work", "#about": "/about", "#services": "/services",
    "#research": "/research", "#news": "/news", "#join": "/careers",
    "#contact": "/contact"
  };
  var path = location.pathname;
  if ((path === "/" || path === "/index.html") && LEGACY[location.hash]) {
    location.replace(LEGACY[location.hash]);
  }
})();
