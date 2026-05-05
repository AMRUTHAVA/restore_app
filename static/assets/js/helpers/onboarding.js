"use strict";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const TIME_PICKER_CONFIGS = [
  { selector: ".pick-time-morn",      defaultHour: 7  },
  { selector: ".pick-time-aftn",      defaultHour: 14 },
  { selector: ".pick-time-eve",       defaultHour: 21 },
  { selector: ".pick-time-bfast",     defaultHour: 8  },
  { selector: ".pick-time-lunch",     defaultHour: 12 },
  { selector: ".pick-time-dinner",    defaultHour: 18 },
  { selector: ".pick-time-workstart", defaultHour: 8  },
  { selector: ".pick-time-workend",   defaultHour: 17 },
];

const FLATPICKR_TIME_BASE = {
  enableTime:      true,
  noCalendar:      true,
  dateFormat:      "h:i K",
  minuteIncrement: 15,
  clickOpens:      true,
  allowInput:      true,
  static:          true,
};

const SLIDER_IDS = [
  "#daily_stress_level",
  "#work_life_balance",
  "#exercise_intensity",
  "#caffeine_frequency",
  "#frequency"
];

// ---------------------------------------------------------------------------
// DOM helpers
// ---------------------------------------------------------------------------

function getById(id) {
  return document.getElementById(id);
}

function getAll(selector) {
  return [...document.querySelectorAll(selector)];
}

// ---------------------------------------------------------------------------
// Form helpers
// ---------------------------------------------------------------------------

function enableDisableCheckboxDependents(checkbox, id) {
  getById(id).disabled = checkbox.checked;
}

function enableDisableWorkTimes(checkbox) {
  ["work_start_time", "work_end_time"].forEach((id) => {
    getById(id).disabled = checkbox.checked;
  });
}

function enableDisableAdditionalQuestions(select) {
  const isNo                = select.value === "no";
  const additionalQuestions = getById("additional_caffeine_questions");

  additionalQuestions.style.display = isNo ? "none" : "flex";

  [
    getById("caffeine_frequency"),
    document.querySelector(".caffeine_intake_type"),
    getById("primary_caffeine_timing"),
    getById("secondary_caffeine_timing"),
  ].forEach((el) => {
    el.disabled = isNo;
  });
}

function selectValueInSelect(select, value) {
  const matchIndex = [...select.options].findIndex((opt) => opt.value === value);
  if (matchIndex !== -1) {
    select.selectedIndex = matchIndex;
  }
}

// ---------------------------------------------------------------------------
// Time utilities
// ---------------------------------------------------------------------------

function to24Hour(time) {
  const [hours, minutes, period] = time.match(/(\d+):(\d+) (\w+)/).slice(1);
  const hour24 = (+hours % 12) + (period === "PM" ? 12 : 0);
  return `${hour24}:${minutes}`;
}

function getMaxBirthDate() {
  const now = new Date();
  return `${now.getMonth() + 1}.${now.getDate()}.${now.getFullYear() - 18}`;
}

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

function initTimePickers() {
  TIME_PICKER_CONFIGS.forEach(({ selector, defaultHour }) => {
    getAll(selector).forEach((picker) => {
      const storedValue = picker.getAttribute("data-value");
      const defaultDate = storedValue ? { defaultDate: to24Hour(storedValue) } : {};
      picker.flatpickr({ ...FLATPICKR_TIME_BASE, defaultHour, ...defaultDate });
    });
  });
}

function initDateOfBirthPicker() {
  document.querySelector("#date_of_birth").flatpickr({
    altInput:      true,
    altFormat:     "F j, Y",
    dateFormat:    "m-d-Y",
    maxDate:       getMaxBirthDate(),
    disableMobile: "false",
  });
}

function initFlatpickr() {
  initTimePickers();
  initDateOfBirthPicker();
}

function initSecondDatePicker() {
  const secondDatePick = getAll(".pick-date")[1];
  secondDatePick.removeAttribute("readonly");
  secondDatePick.onkeydown = () => false;
}

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

function showOnboardingModal() {
  new OnboardingWizard("#onboarding_wizard_main", { validate: true, progress: true });
  new bootstrap.Modal(".onboarding-modal", {
    keyboard: false,
    backdrop: "static",
    focus:    true,
  }).toggle();
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

window.addEventListener("DOMContentLoaded", function() {
  var onboardingCompletedAtElem = document.querySelector(".onboarding-modal")

  if (onboardingCompletedAtElem) {
    const onboardingCompletedAt = onboardingCompletedAtElem.getAttribute("data-survey-completed-at");
    if (!onboardingCompletedAt) {
      showOnboardingModal();
    }
  }

  initFlatpickr();
  initSecondDatePicker();
  initSliders();
  initSelects();
});