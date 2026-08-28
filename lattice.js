/* =========================================================
   lattice.js — the 3D molecular field behind the dark bands.

   No library. It is a point cloud in a 3D box, rotated on two
   axes and projected through a perspective divide, with bonds
   drawn between neighbours that are genuinely close in 3D.
   Depth drives radius, brightness and bond opacity, which is
   what makes it read as volume rather than as a flat web.

   Attach it by putting <canvas class="fx3d"></canvas> inside any
   positioned element. Optional attributes:
     data-count    node count override
     data-speed    rotation multiplier (default 1)
   ========================================================= */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) { return; }

  var CYAN = "0,188,212";
  var MINT = "94,234,212";

  function Field(canvas) {
    this.canvas = canvas;
    this.host = canvas.parentElement;
    this.ctx = canvas.getContext("2d");
    this.nodes = [];
    this.w = 0;
    this.h = 0;
    this.raf = null;
    this.running = false;
    this.rotX = -0.18;
    this.rotY = 0;
    this.targetX = -0.18;
    this.targetY = 0;
    this.speed = parseFloat(canvas.getAttribute("data-speed") || "1");
    this.size();
    this.bind();
    this.start();
  }

  Field.prototype.size = function () {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    this.w = this.host.offsetWidth;
    this.h = this.host.offsetHeight;
    this.canvas.width = this.w * dpr;
    this.canvas.height = this.h * dpr;
    this.canvas.style.width = this.w + "px";
    this.canvas.style.height = this.h + "px";
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    this.depth = Math.max(320, Math.min(this.w, 900) * 0.75);

    /* Focal length and camera offset are tuned together: short enough
       that near and far nodes differ by about 2x in size, long enough
       that a node can never swing behind the camera during rotation. */
    this.focal = this.depth * 1.6;
    this.offset = this.depth * 1.9;
    var maxZ = this.depth * 1.8;
    this.smin = this.focal / (this.focal + this.offset + maxZ);
    this.smax = this.focal / (this.focal + this.offset - maxZ);

    var override = parseInt(this.canvas.getAttribute("data-count"), 10);
    var count = override || Math.round(Math.min(70, Math.max(20, this.w * this.h / 13000)));
    if (this.w < 700) { count = Math.round(count * 0.62); }

    /* Bond length scales with the box, so the lattice keeps the same
       visual density on a phone as on a wide desktop. */
    this.bond = this.depth * 0.62;

    this.nodes = [];
    for (var i = 0; i < count; i++) {
      this.nodes.push({
        x: (Math.random() - 0.5) * this.depth * 2.5,
        y: (Math.random() - 0.5) * this.depth * 1.25,
        z: (Math.random() - 0.5) * this.depth,
        vx: (Math.random() - 0.5) * 0.22,
        vy: (Math.random() - 0.5) * 0.22,
        vz: (Math.random() - 0.5) * 0.22,
        r: Math.random() * 1.5 + 1.4
      });
    }
  };

  Field.prototype.bind = function () {
    var self = this;

    var timer;
    window.addEventListener("resize", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { self.stop(); self.size(); self.start(); }, 160);
    });

    document.addEventListener("visibilitychange", function () {
      document.hidden ? self.stop() : self.start();
    });

    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        entries[0].isIntersecting ? self.start() : self.stop();
      }, { threshold: 0 }).observe(this.host);
    }

    /* Pointer nudges the viewing angle. Small range — the lattice
       should feel like it has a physical orientation, not swing. */
    if (window.matchMedia("(hover: hover)").matches) {
      this.host.addEventListener("pointermove", function (e) {
        var b = self.host.getBoundingClientRect();
        self.targetY = ((e.clientX - b.left) / b.width - 0.5) * 0.6;
        self.targetX = -0.18 + ((e.clientY - b.top) / b.height - 0.5) * -0.4;
      });
      this.host.addEventListener("pointerleave", function () {
        self.targetY = 0;
        self.targetX = -0.18;
      });
    }
  };

  Field.prototype.project = function (n, cosX, sinX, cosY, sinY) {
    var x = n.x * cosY - n.z * sinY;
    var z = n.x * sinY + n.z * cosY;
    var y = n.y * cosX - z * sinX;
    z = n.y * sinX + z * cosX;

    var scale = this.focal / (this.focal + z + this.offset);
    /* t is normalised depth: 0 at the back of the box, 1 at the front.
       Radius, brightness and bond opacity all key off it. */
    var t = (scale - this.smin) / (this.smax - this.smin);
    return {
      sx: this.w / 2 + x * scale,
      sy: this.h / 2 + y * scale,
      scale: scale,
      t: t < 0 ? 0 : (t > 1 ? 1 : t),
      z: z
    };
  };

  Field.prototype.draw = function () {
    var ctx = this.ctx;
    var n, i, j, p, q, d;

    this.rotY += (this.targetY - this.rotY) * 0.045;
    this.rotX += (this.targetX - this.rotX) * 0.045;
    this.spin = (this.spin || 0) + 0.0013 * this.speed;

    var cosX = Math.cos(this.rotX), sinX = Math.sin(this.rotX);
    var cosY = Math.cos(this.rotY + this.spin), sinY = Math.sin(this.rotY + this.spin);

    ctx.clearRect(0, 0, this.w, this.h);

    var pts = [];
    for (i = 0; i < this.nodes.length; i++) {
      n = this.nodes[i];
      n.x += n.vx; n.y += n.vy; n.z += n.vz;
      if (Math.abs(n.x) > this.depth * 1.25) { n.vx *= -1; }
      if (Math.abs(n.y) > this.depth * 0.62) { n.vy *= -1; }
      if (Math.abs(n.z) > this.depth * 0.5) { n.vz *= -1; }
      pts.push(this.project(n, cosX, sinX, cosY, sinY));
    }

    /* Bonds first, so nodes sit on top of them. */
    for (i = 0; i < this.nodes.length; i++) {
      for (j = i + 1; j < this.nodes.length; j++) {
        var a = this.nodes[i], b = this.nodes[j];
        d = Math.sqrt(
          (a.x - b.x) * (a.x - b.x) +
          (a.y - b.y) * (a.y - b.y) +
          (a.z - b.z) * (a.z - b.z)
        );
        if (d > this.bond) { continue; }
        p = pts[i]; q = pts[j];
        var near = (p.t + q.t) / 2;
        ctx.strokeStyle = "rgba(" + CYAN + "," + (1 - d / this.bond) * (0.16 + near * 0.78) * 0.8 + ")";
        ctx.lineWidth = 0.5 + near * 1.1;
        ctx.beginPath();
        ctx.moveTo(p.sx, p.sy);
        ctx.lineTo(q.sx, q.sy);
        ctx.stroke();
      }
    }

    /* Far nodes painted before near ones. */
    var order = pts.map(function (p, k) { return k; }).sort(function (a, b) {
      return pts[b].z - pts[a].z;
    });

    for (var k = 0; k < order.length; k++) {
      i = order[k];
      p = pts[i];
      var rad = this.nodes[i].r * p.scale * (1.1 + p.t * 1.9);
      ctx.fillStyle = "rgba(" + MINT + "," + (0.24 + p.t * 0.72) + ")";
      ctx.beginPath();
      ctx.arc(p.sx, p.sy, Math.max(0.4, rad), 0, Math.PI * 2);
      ctx.fill();
    }

    this.raf = requestAnimationFrame(this.draw.bind(this));
  };

  Field.prototype.start = function () {
    if (this.running) { return; }
    this.running = true;
    this.draw();
  };

  Field.prototype.stop = function () {
    this.running = false;
    cancelAnimationFrame(this.raf);
  };

  function init() {
    var list = document.querySelectorAll("canvas.fx3d");
    for (var i = 0; i < list.length; i++) { new Field(list[i]); }
  }

  document.readyState === "loading"
    ? document.addEventListener("DOMContentLoaded", init)
    : init();
})();
