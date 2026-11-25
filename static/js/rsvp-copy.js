/*
 * «Kopier» on «Slik betaler du» (Story 2.7; FR-34, FR-71, UX-DR25;
 * DESIGN.md › Payment details).
 *
 * Only an enhancement: the values are plain selectable text without it. The
 * buttons are shown only when `navigator.clipboard.writeText` exists in a
 * secure context. A click writes the button's `data-copy`, empties every
 * other `.copy-status` and puts «Kopiert» in this row's. When the write is
 * refused, the row's value is selected and the status reads «Trykk og hold
 * for å kopiere». The status spans are in the page from load; the script
 * only sets their text (emptied, then filled after 100 ms, so a repeat is
 * announced again) and never adds a live region. Vanilla, no build step.
 */
(function () {
  "use strict";
  var clipboard = navigator.clipboard;
  if (!window.isSecureContext || !clipboard || typeof clipboard.writeText !== "function") {
    return;
  }
  var statuses = document.querySelectorAll(".copy-status");

  function show(status, text) {
    Array.prototype.forEach.call(statuses, function (other) {
      if (other !== status) {
        other.textContent = "";
      }
    });
    // Emptied first and filled a moment later, so the same text twice is
    // still a change the screen reader announces.
    status.textContent = "";
    window.setTimeout(function () {
      status.textContent = text;
    }, 100);
  }

  function selectValue(value) {
    var range = document.createRange();
    range.selectNodeContents(value);
    var selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  }

  Array.prototype.forEach.call(document.querySelectorAll("button[data-copy]"), function (button) {
    var row = button.closest("dd");
    var status = row.querySelector(".copy-status");
    var value = row.querySelector("[data-copy-value]");
    button.hidden = false;
    button.addEventListener("click", function () {
      clipboard.writeText(button.getAttribute("data-copy")).then(
        function () {
          show(status, "Kopiert");
        },
        function () {
          selectValue(value);
          show(status, "Trykk og hold for å kopiere");
        }
      );
    });
  });
})();
