/*
 * The busy state of «Send svaret» on the RSVP check page (Story 2.6a;
 * FR-74, UX-DR15; DESIGN.md › Button, busy).
 *
 * Only an enhancement: without it the form still sends. On the first submit
 * the button reads «Sender …» and gets `aria-disabled="true"`; it is never
 * `disabled`, since a disabled submitter is left out of the form data and
 * `action=send` would be lost. A second submit while busy is prevented. When
 * the page comes back from the back-forward cache, the button is restored.
 * A repeated send that still reaches the server is handled there (Story 2.6c).
 * Vanilla, no build step.
 */
(function () {
  "use strict";
  var form = document.querySelector("form[data-send-form]");
  var button = form && form.querySelector('button[name="action"][value="send"]');
  if (!button) {
    return;
  }
  var label = button.textContent;
  var busy = false;
  form.addEventListener("submit", function (event) {
    if (busy) {
      event.preventDefault();
      return;
    }
    busy = true;
    button.textContent = "Sender …";
    button.setAttribute("aria-disabled", "true");
  });
  window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
      busy = false;
      button.textContent = label;
      button.removeAttribute("aria-disabled");
    }
  });
})();
