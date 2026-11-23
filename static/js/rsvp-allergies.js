/*
 * «Ingen allergier eller matbehov» is exclusive per person on step 5 of the
 * RSVP form (Story 2.4; FR-25, UX-DR21; EXPERIENCE.md › Choice control).
 *
 * Only an enhancement: without it the server refuses «Ingen …» together with
 * a category or a note and asks the guest to choose one. Within one person's
 * fieldset (`[data-allergy-group]`), ticking «Ingen …» unticks the
 * categories, and ticking a category unticks «Ingen …». The note is never
 * cleared, so nothing typed is lost. Vanilla, no build step.
 */
(function () {
  "use strict";
  document.addEventListener("change", function (event) {
    var input = event.target;
    if (!(input instanceof HTMLInputElement) || !input.checked) {
      return;
    }
    var group = input.closest("[data-allergy-group]");
    if (!group) {
      return;
    }
    var selector = input.hasAttribute("data-allergy-none")
      ? "[data-allergy-category]"
      : input.hasAttribute("data-allergy-category")
        ? "[data-allergy-none]"
        : null;
    if (!selector) {
      return;
    }
    group.querySelectorAll(selector).forEach(function (other) {
      other.checked = false;
    });
  });
})();
