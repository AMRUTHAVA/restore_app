// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

window.addEventListener("DOMContentLoaded", function() {
  const onboardingCompletedAtElem = document.querySelector(".onboarding-modal");
  const nudgeTextElem = document.querySelector(".nudge-modal");

  if (onboardingCompletedAtElem && nudgeTextElem) {
    const onboardingCompletedAt = onboardingCompletedAtElem.getAttribute("data-survey-completed-at");
    const nudgeText = nudgeTextElem.getAttribute("data-user-nudge-text");
    if (onboardingCompletedAt && nudgeText) {
      new bootstrap.Modal(".nudge-modal", {
        keyboard: false,
        backdrop: "static",
        focus:    true,
      }).toggle();
    }
  }
});