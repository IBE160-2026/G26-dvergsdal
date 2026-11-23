/*
 * «Send svaret» on the RSVP check page (Stories 2.6a, 2.6c; FR-74, UX-DR15,
 * UX-DR52, AD-20; DESIGN.md › Button, busy).
 *
 * Only an enhancement: without it the form still posts natively. On the
 * first submit the button reads «Sender …» and gets `aria-disabled="true"`;
 * it is never `disabled`. A second submit while busy is prevented. The form
 * is sent with fetch, with `action=send` added (a submit event's form data
 * leaves the button out). A redirect (sent page, or the check page with a
 * notice) is followed; any other response is sent again natively so the
 * server's own page shows (the one-time submission id makes that repeat
 * safe). When the connection breaks, the button is reset and the hidden
 * `[data-send-failed]` notice is shown and focused, so the guest can try
 * again. When the page comes back from the back-forward cache, the button
 * is restored. Vanilla, no build step.
 */
(function () {
  "use strict";
  var form = document.querySelector("form[data-send-form]");
  var button = form && form.querySelector('button[name="action"][value="send"]');
  if (!button) {
    return;
  }
  var label = button.textContent;
  var failed = form.querySelector("[data-send-failed]");
  var busy = false;

  function reset() {
    busy = false;
    button.textContent = label;
    button.removeAttribute("aria-disabled");
  }

  function sendNatively() {
    var action = document.createElement("input");
    action.type = "hidden";
    action.name = "action";
    action.value = "send";
    form.appendChild(action);
    HTMLFormElement.prototype.submit.call(form);
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (busy) {
      return;
    }
    busy = true;
    button.textContent = "Sender …";
    button.setAttribute("aria-disabled", "true");
    if (failed) {
      failed.hidden = true;
    }
    var data = new FormData(form);
    data.set("action", "send");
    fetch(form.action || location.href, {
      method: "POST",
      body: data,
      credentials: "same-origin",
    }).then(
      function (response) {
        if (response.redirected) {
          location.assign(response.url);
        } else {
          sendNatively();
        }
      },
      function () {
        reset();
        if (failed) {
          failed.hidden = false;
          failed.focus();
        }
      }
    );
  });

  window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
      reset();
    }
  });
})();
