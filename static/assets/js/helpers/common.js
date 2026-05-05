
// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const IDLE_TIMEOUT = 3600000;
let idleTime;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function reloadPage() {
  window.location.href = '/dashboard';
}

function resetTimerActivity(idleTime) {
  clearTimeout(idleTime);
  idleTime = setTimeout(reloadPage, IDLE_TIMEOUT);
}

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

// Fetch all the forms we want to apply custom Bootstrap validation styles to
const bsValidationForms = document.querySelectorAll('.needs-validation');
// Loop over them and prevent submission
Array.prototype.slice.call(bsValidationForms).forEach(function (form) {
  form.addEventListener(
    'submit',
    function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    },
    false
  );
});

function setActivityTracking() {
  document.addEventListener("mousemove", resetTimerActivity);
  document.addEventListener("keypress", resetTimerActivity);
  document.addEventListener("click", resetTimerActivity);
  document.addEventListener("mousedown", resetTimerActivity);
  document.addEventListener("scroll", resetTimerActivity);

  resetTimerActivity(idleTime);
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
  const toastElements = document.querySelectorAll('.toast');
  toastElements.forEach(function (el) {
    const toast = new bootstrap.Toast(el);
    toast.show();
  });

  // Poor man's implementation of reload, so we can go to market fast. 
  // We can spend the effort to put in push per v2 and feedback on notifications
  setActivityTracking();
});