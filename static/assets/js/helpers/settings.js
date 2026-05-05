"use strict";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SLIDER_IDS = [
  "#frequency"
];

// ---------------------------------------------------------------------------
// DOM helpers
// ---------------------------------------------------------------------------

function getAll(selector) {
  return [...document.querySelectorAll(selector)];
}

// ---------------------------------------------------------------------------
// FORM helpers
// ---------------------------------------------------------------------------

function selectValueInSelect(select, value) {
  const matchIndex = [...select.options].findIndex((opt) => opt.value === value);
  if (matchIndex !== -1) {
    select.selectedIndex = matchIndex;
  }
}

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

function initSliders() {
  SLIDER_IDS.forEach((id) => new Slider(id));
}

function initSelects() {
  getAll("select").forEach((select) => {
    const storedValue = select.getAttribute("data-value");
    if (storedValue) {
      selectValueInSelect(select, storedValue);
    }
  });
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

window.addEventListener("DOMContentLoaded", function() {
  initSliders();
  initSelects();
});