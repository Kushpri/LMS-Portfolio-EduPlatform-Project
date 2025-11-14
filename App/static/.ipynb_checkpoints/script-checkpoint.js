// ---------- Mark lesson as complete (used on course page) ----------
async function markCompleted(lessonId, button) {
  if (!lessonId) return;

  try {
    const res = await fetch("/complete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lesson_id: Number(lessonId) }),
    });

    if (!res.ok) {
      console.error("Failed to mark complete");
      alert("Could not update progress. Please try again.");
      return;
    }

    const data = await res.json();
    if (!data.success) {
      console.error("Server error:", data.error);
      alert("Server error while saving progress.");
      return;
    }

    // Update button UI
    if (button) {
      button.disabled = true;
      button.textContent = "Completed ✓";
      button.classList.add("completed");
    }

    // If we ever add a progress bar, we can update it here
    // using data.progress_pct (already sent by backend).
    console.log("Updated progress:", data.progress_pct + "%");

  } catch (e) {
    console.error("Request failed", e);
    alert("Network error. Please try again.");
  }
}

// ---------- Course search (used on index + dashboard) ----------
function filterCourses() {
  const input = document.getElementById("courseSearch");
  if (!input) return;

  const query = input.value.toLowerCase().trim();
  const cards = document.querySelectorAll("[data-course-card]");

  cards.forEach((card) => {
    const title = (card.getAttribute("data-title") || "").toLowerCase();
    card.style.display = title.includes(query) ? "" : "none";
  });
}
