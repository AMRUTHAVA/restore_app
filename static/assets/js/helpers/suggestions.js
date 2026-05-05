// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------


function selectSuggestion(elem, tier) {
  parent = elem.parentElement;
  classNum = tier * 100;
  value = elem.value;
  if (elem.checked) {
    parent.classList.remove('bg-gray-'+classNum);
    parent.classList.add('bg-blue-'+classNum);
    postSuggestionSelection(value, true);
    confetti({
      particleCount: 1400,
      spread:        180,
      origin:        { y: 0.6 },
    });
  } else {
    parent.classList.remove('bg-blue-'+classNum);
    parent.classList.add('bg-gray-'+classNum);
    postSuggestionSelection(value, false);
  }
}

async function postSuggestionSelection(value, is_checked) {
  const csrfToken = document.getElementById("suggestionsForm").querySelector("[name=csrfmiddlewaretoken]").value;
  const payload   = { 'user_energy_plan_suggestion_id': value, 'is_checked': is_checked };

  try {
    const response = await fetch("/save_energy_plan_suggestion_selection", {
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
  } catch (error) {
    console.error("Error:", error);
  }
}