(function () {
  const form = document.getElementById("whatIfForm");
  const table = document.getElementById("whatifTable");
  const addClassBtn = document.getElementById("addClassBtn");
  const gpaSpan = document.getElementById("gpaValue");

  // If any of these are missing, do nothing (this prevents affecting other pages)
  if (!form || !table || !addClassBtn || !gpaSpan) {
    return;
  }

  const tbody = table.querySelector("tbody");

  // Keep DB strictly read-only for this page (so students can't edit real grades)
  form.addEventListener("submit", function (event) {
    event.preventDefault();
  });

  const gradePoints = {
    "A"  : 4.0,
    "A-" : 3.7,
    "B+" : 3.3,
    "B"  : 3.0,
    "B-" : 2.7,
    "C+" : 2.3,
    "C"  : 2.0,
    "C-" : 1.7,
    "D+" : 1.3,
    "D"  : 1.0,
    "F"  : 0.0,
  };

  function computeGpa() {
    var totalUnits = 0;
    var totalPoints = 0;

    tbody.querySelectorAll("tr").forEach(function (row) {
      var unitsInput = row.querySelector('input[name="units"]');
      var gradeSelect = row.querySelector('select[name="grade"]');

      if (!unitsInput || !gradeSelect) {
        return;
      }

      var units = parseFloat(unitsInput.value);
      var grade = gradeSelect.value;

      if (!isNaN(units) && units > 0 && gradePoints.hasOwnProperty(grade)) {
        totalUnits += units;
        totalPoints += units * gradePoints[grade];
      }
    });

    if (totalUnits === 0) {
      gpaSpan.textContent = "–";
    } else {
      var gpa = totalPoints / totalUnits;
      gpaSpan.textContent = gpa.toFixed(2);
    }
  }

  addClassBtn.addEventListener("click", function () {
    var row = document.createElement("tr");
    row.setAttribute("data-enrolled", "false");

    row.innerHTML = [
      '<td class="align-middle">',
      '  <input type="text" class="form-control" name="course_name" placeholder="Course Name (optional)">',
      "</td>",
      '<td class="align-middle">',
      '  <input type="number" class="form-control" name="units" min="0" step="0.5" placeholder="0">',
      "</td>",
      '<td class="align-middle">',
      '  <select class="form-select" name="grade">',
      '    <option value="">Select grade</option>',
      '    <option value="A">A</option>',
      '    <option value="A-">A-</option>',
      '    <option value="B+">B+</option>',
      '    <option value="B">B</option>',
      '    <option value="B-">B-</option>',
      '    <option value="C+">C+</option>',
      '    <option value="C">C</option>',
      '    <option value="C-">C-</option>',
      '    <option value="D+">D+</option>',
      '    <option value="D">D</option>',
      '    <option value="F">F</option>',
      "  </select>",
      "</td>",
      '<td class="align-middle text-center">',
      '  <button type="button" class="btn btn-outline-danger btn-sm remove-row">✕</button>',
      "</td>",
    ].join("");

    tbody.appendChild(row);
    computeGpa();
  });

  tbody.addEventListener("click", function (event) {
    var btn = event.target.closest(".remove-row");
    if (!btn) {
      return;
    }

    var row = btn.closest("tr");
    if (!row) {
      return;
    }

    if (row.getAttribute("data-enrolled") === "true") {
      return;
    }

    row.remove();
    computeGpa();
  });

  // Recalculate GPA when units or grades change
  tbody.addEventListener("change", function (event) {
    if (
      event.target.matches('input[name="units"]') ||
      event.target.matches('select[name="grade"]')
    ) {
      computeGpa();
    }
  });

  // Initial GPA calculation on page load
  computeGpa();
})();
