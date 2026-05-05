self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: "window" }).then((clientList) => {
      // Focus existing tab if open
      for (const client of clientList) {
        if (client.url.includes("dashboard") && "focus" in client) {
          return client.focus();
        }
      }
      // Otherwise open a new tab
      if (clients.openWindow) {
        return clients.openWindow("/");
      }
    })
  );
});

self.addEventListener('message', (event) => {
  let notification = event.data;
  self.registration.showNotification(
    notification.title,
    notification.options
  ).catch((error) => {
    console.log(error);
  });
});