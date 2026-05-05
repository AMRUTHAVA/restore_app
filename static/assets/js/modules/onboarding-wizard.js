"use strict";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MCTQ_INDEX    = 5;
const MCTQ_STEP_KEY = "nonworkday_sleep";

const LOADING_MESSAGES = [
  "Knowledge is power!...",
  "Generating witty dialog...",
  "Calculating your Chronotype...",
  "Swapping time and space...",
  "Spinning violently around the y-axis...",
  "Calculating your Chronotype...",
  "Tokenizing real life...",
  "Bending the spoon...",
  "Calculating your Chronotype...",
  "Filtering morale...",
];

// ---------------------------------------------------------------------------
// Wizard Class
// ---------------------------------------------------------------------------

class OnboardingWizard {

  constructor(target, options = {}) {
    this.onboardingWizard = target instanceof HTMLElement
      ? target
      : document.querySelector(target);

    this.validate = options.validate ?? false;
    this.buttons  = options.buttons  ?? false;
    this.progress = options.progress ?? false;

    // Internal state
    this.selectedIndex    = 0;
    this.formDataObj      = {};
    this._spinnerInterval = null;
    this._spinnerIndex    = 0;

    this._initOptions();
    this._initEventListeners();
  }

  _initOptions() {
    const onboardingModal = document.querySelector(".onboarding-modal");
    const maxSectionId    = onboardingModal.getAttribute("data-survey-completed-tab-index");
    const chronotype      = onboardingModal.getAttribute("data-chronotype");

    // Determine which tab to start on based on prior progress
    if (maxSectionId) {
      if (maxSectionId <= 3) {
        this.selectedIndex = 3 + parseInt(maxSectionId, 10);
      } else if (maxSectionId < 7) {
        this.selectedIndex = 4 + parseInt(maxSectionId, 10);
      } else {
        this.selectedIndex = 3;
      }
    }

    if (chronotype) {
      this._showUserMCTQ(chronotype, false);
    }

    this.progressBar = this.progress
      ? this.onboardingWizard.querySelector(".tab-content .progress .progress-bar")
      : null;

    this.navItems = this.onboardingWizard.querySelectorAll("ul li.nav-item a");
    this.tabPanes = this.onboardingWizard.querySelectorAll(".tab-content .tab-pane");

    this._initButtons();
    this._showSelectedTab();
  }

  _initButtons() {
    const root = this.onboardingWizard;

    if (this.buttons) {
      this.prevBtn  = root.querySelector(".tab-content .button-previous");
      this.nextBtn  = root.querySelector(".tab-content .button-next");
      this.firstBtn = root.querySelector(".tab-content .button-first");
      this.lastBtn  = root.querySelector(".tab-content .button-last");
    } else {
      this.prevBtn  = root.querySelector(".tab-content .previous a");
      this.nextBtn  = root.querySelector(".tab-content .next a");
      this.firstBtn = root.querySelector(".tab-content .first a");
      this.lastBtn  = root.querySelector(".tab-content .last a");
    }
  }

  _initEventListeners() {
    this.prevBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      if (this.selectedIndex > 0) {
        this.selectedIndex--;
        this._showSelectedTab();
      }
    });

    this.nextBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      if (this.selectedIndex < this.navItems.length - 1 && this._validateForm()) {
        this.selectedIndex++;
        this._showSelectedTab();
      }
    });

    this.firstBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      if (this.selectedIndex !== 0 && this._validateForm()) {
        this.selectedIndex = 0;
        this._showSelectedTab();
      }
    });

    this.lastBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      if (this.selectedIndex !== this.navItems.length - 1 && this._validateForm()) {
        this.selectedIndex = this.navItems.length - 1;
        this._showSelectedTab();
      }
    });

    this.navItems.forEach((item, index) => {
      item.addEventListener("click", () => {
        this.selectedIndex = index;
        if (this._validateForm()) {
          this._showSelectedTab();
        }
      });
    });
  }

  _showSelectedTab() {
    const percent = Math.floor(((this.selectedIndex + 1) / this.navItems.length) * 100);
    const width   = `${percent}%`;

    new bootstrap.Tab(this.navItems[this.selectedIndex]).show();

    if (this.progressBar) {
      this.progressBar.style.width = width;
      this.progressBar.innerText   = width;
    }

    this._updateButtonStyles();
  }

  _updateButtonStyles() {
    const isFirst = this.selectedIndex === 0;
    const isLast  = this.selectedIndex === this.navItems.length - 1;

    // Reset disabled state on all buttons
    this.lastBtn?.classList.remove("disabled");
    this.firstBtn?.classList.remove("disabled");
    this.nextBtn?.classList.remove("disabled");
    this.prevBtn?.classList.remove("disabled");

    if (isFirst) {
      this.prevBtn?.classList.add("disabled");
      this.firstBtn?.classList.add("disabled");
    } else if (isLast) {
      this.nextBtn?.classList.add("disabled");
      this.lastBtn?.classList.add("disabled");
    }

    this._toggleCloseButton();
  }

  _toggleCloseButton() {
    // Don't change button visibility on the tab immediately after the MCTQ result
    if (this.selectedIndex === MCTQ_INDEX + 1) return;

    const isNextDisabled = this.nextBtn?.classList.contains("disabled");
    const closeModal     = document.querySelector(".close-modal");

    if (isNextDisabled) {
      closeModal.style.display   = "block";
      this.nextBtn.style.display = "none";
    } else {
      closeModal.style.display   = "none";
      this.nextBtn.style.display = "block";
    }
  }

  _validateForm() {
    if (!this.validate) return true;

    const form = this.tabPanes[this.selectedIndex].querySelector("form");
    if (!form) return true;

    if (form.checkValidity()) {
      return this._processFormData(form);
    }

    form.classList.add("was-validated");
    return false;
  }

  _processFormData(formElem) {
    const formKey  = formElem.getAttribute("data-key");
    const formData = new FormData(formElem);
    const values   = {};

    for (const [key, value] of formData.entries()) {
      if (key === "caffeine_intake_type" || key == "channels") {
        values[key] = formData.getAll(key);
        if (!Array.isArray(values[key])) {
          values[key] = [values[key]];
        }
      } else {
        values[key] = value;
      }
    }

    this.formDataObj[formKey] = values;
    this._postFormData(formElem, formKey, values);
    return true;
  }

  async _postFormData(formElem, formKey, formDataValues) {
    const csrfToken = formElem.querySelector("[name=csrfmiddlewaretoken]").value;
    const payload   = { [formKey]: formDataValues };

    if (formKey === MCTQ_STEP_KEY) {
      this._showHideMCTQ(false);
      this._showHideSpinner(true);
      this._enableDisableNavButtons(false);
    }

    try {
      const response = await fetch("/save_baseline_survey", {
        method: "POST",
        headers: {
          "X-CSRFToken":  csrfToken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      if (data.chronotype) {
        this._showUserMCTQ(data.chronotype, true);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  // -------------------------------------------------------------------------
  // MCTQ result display
  // -------------------------------------------------------------------------

  _showUserMCTQ(chronotype, showConfetti) {
    // eval is used here to dynamically access a global mctq object by chronotype
    // e.g. mctqMorning, mctqEvening, etc.
    const mctqObj = eval(`mctq${chronotype}`); // eslint-disable-line no-eval

    document.querySelector("#mctq_header_label").innerText           = mctqObj.label_alt;
    document.querySelector("#mctq_tag_line").innerText               = mctqObj.tag_line;
    document.querySelector("#mctq_short_description").innerText      = mctqObj.short_description;
    document.querySelector("#mctq_image").setAttribute("src",  `/static/assets/images/chronotypes/${mctqObj.image_file_primary}`);
    document.querySelector("#mctq_image").setAttribute("alt",  mctqObj.label);
    document.querySelector("#mctq_download").href                    = `/static/assets/files/chronotypes/${mctqObj.download_file_primary}`;
    document.querySelector("#mctq_peak_performance_hours_primary").innerText   = mctqObj.peak_performance_hours.primary;
    document.querySelector("#mctq_peak_performance_hours_secondary").innerText = mctqObj.peak_performance_hours.secondary;
    document.querySelector("#mctq_description_label").innerText      = mctqObj.label;
    document.querySelector("#mctq_long_description").innerText       = mctqObj.long_description;

    this._showHideSpinner(false);
    this._showHideMCTQ(true);
    this._enableDisableNavButtons(true);

    if (showConfetti) {
      this._showConfetti();
    }
  }

  // -------------------------------------------------------------------------
  // UI helpers
  // -------------------------------------------------------------------------

  _enableDisableNavButtons(enable) {
    const previousButton = document.querySelector(".previous a");
    const nextButton     = document.querySelector(".next a");
    const display        = enable ? "block" : "none";

    previousButton.style.setProperty("display", display, "important");
    nextButton.style.setProperty("display", display, "important");
  }

  _showHideSpinner(show) {
    const spinner        = document.querySelector(".onboarding-spinner");
    const spinnerMessage = document.querySelector(".spinner-message h3");

    if (show) {
      spinner.style.setProperty("display", "block", "important");
      this._spinnerInterval = setInterval(() => {
        spinnerMessage.innerText = LOADING_MESSAGES[this._spinnerIndex];
        this._spinnerIndex       = (this._spinnerIndex + 1) % LOADING_MESSAGES.length;
      }, 1000);
    } else {
      clearInterval(this._spinnerInterval);
      spinner.style.setProperty("display", "none", "important");
    }
  }

  _showHideMCTQ(show) {
    const mctqDetail = document.querySelector("#mctq_detail");
    mctqDetail.style.setProperty("display", show ? "flex" : "none", "important");
  }

  _showConfetti() {
    confetti({
      particleCount: 1400,
      spread:        180,
      origin:        { y: 0.6 },
    });
  }
}
