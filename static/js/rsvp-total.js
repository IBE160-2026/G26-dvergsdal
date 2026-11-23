/*
 * The running household total on the RSVP form's paid steps (Story 2.3;
 * FR-33, AD-7, AD-12, UX-DR17; DESIGN.md › Running total).
 *
 * Only an enhancement: without it the next page shows the total, computed by
 * the server. On every change in the form, the form is posted to its
 * `data-total-url` (`POST /<code>/svar/sum/?steg=<slug>`, with the form's
 * CSRF token). Only on 200 is `.form-total` replaced with the server's
 * fragment, and its text written to the empty `#total-status` region, so a
 * screen reader hears the new total once. Failures and late answers to an
 * older change are ignored. Vanilla, no build step.
 */
(function () {
  "use strict";
  var form = document.querySelector("form[data-total-url]");
  var status = document.getElementById("total-status");
  if (!form || !status) {
    return;
  }
  var latest = 0;
  form.addEventListener("change", function () {
    var request = ++latest;
    fetch(form.dataset.totalUrl, {
      method: "POST",
      body: new FormData(form),
      credentials: "same-origin",
    })
      .then(function (response) {
        return response.status === 200 ? response.text() : null;
      })
      .then(function (html) {
        var current = form.querySelector(".form-total");
        if (html === null || request !== latest || !current) {
          return;
        }
        var fresh = new DOMParser().parseFromString(html, "text/html").querySelector(".form-total");
        if (fresh) {
          current.replaceWith(fresh);
          status.textContent = fresh.textContent.replace(/[ \t\r\n]+/g, " ").trim();
        }
      })
      .catch(function () {});
  });
})();
