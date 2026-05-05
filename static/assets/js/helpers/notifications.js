
// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getRegistration() {
  return navigator.serviceWorker.getRegistration();
}

async function registerServiceWorker() {
  await navigator.serviceWorker.register('./service-worker.js')
}

async function unRegisterServiceWorker() {
  let registration = await getRegistration();
  await registration.unregister();
}

async function sendNotification(title, body) {
  let notification = {
    title: title,
    options: { body: body }
  };
  let registration = await getRegistration();
  if (registration) {
    if (navigator.serviceWorker.controller) {
      if (Notification.permission == 'granted') {
        navigator.serviceWorker.controller.postMessage(notification);
      } else {
        Notification.requestPermission().then((permission) => {
          if (Notification.permission == 'granted') {
            navigator.serviceWorker.controller.postMessage(notification);
          }
        });
      };
    } else {
      console.log('No service worker controller found. Try a soft reload.');
    }
  }
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

window.addEventListener("DOMContentLoaded", function() {
  const nudgeDesktop = document.querySelector(".nudge-modal");
  const nudgeText = document.querySelector(".nudge-modal");

  if (Notification.permission !== 'granted') {
    Notification.requestPermission();
  };

  registerServiceWorker();

  if (nudgeDesktop && nudgeText && nudgeDesktop.getAttribute("data-user-nudge-desktop") == "True" && nudgeText.getAttribute("data-user-nudge-text")) {
    sendNotification(nudgeText, nudgeText);
  };
});

window.addEventListener("unload", function() {
  unRegisterServiceWorker();
});