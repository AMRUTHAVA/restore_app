// ---------------------------------------------------------------------------
// Timezone utilities
// ---------------------------------------------------------------------------

function getTimezoneOffset() {
  const now = new Date();
  const jan = new Date(now.getFullYear(), 0, 1);
  const jun = new Date(now.getFullYear(), 6, 1);

  const utcOffset = (date) => (date - new Date(date.toGMTString().slice(0, -4))) / (1000 * 60 * 60);

  const stdOffset = utcOffset(jan);
  const dstOffset = utcOffset(jun);
  const observesDST = stdOffset !== dstOffset;
  const offset = observesDST && stdOffset - dstOffset >= 0 ? dstOffset : stdOffset;

  return `${formatOffset(offset)},${observesDST ? 1 : 0}`;
}

function formatOffset(value) {
  const hours = Math.trunc(value);
  const mins = Math.round((Math.abs(value) % 1) * 60);
  const pad = (n) => String(Math.abs(n)).padStart(2, "0");

  const sign = hours > 0 ? "+" : hours < 0 ? "-" : "";
  return `${sign}${pad(hours)}:${pad(mins)}`;
}

function setTimezoneSelect() {
  var elem = document.getElementById("timezone");
  if (!elem) return;
  const target = getTimezoneOffset();
  elem.value = target;
}