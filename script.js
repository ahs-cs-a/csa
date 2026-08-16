// ---- Where we are in the course right now -------------------------------
// Update this each week (or wire it up to a real date later). Everything
// else on the site (highlighting, "This Week" card, done/upcoming state)
// is derived from this one value.
const CURRENT = { semester: "s1", week: 1 };

const SEM_LABEL = { s1: "Semester 1", s2: "Semester 2" };

const CONCEPT_COLOR = {
  "course-info": "var(--cx)", "c1": "var(--c1)", "c2": "var(--c2)", "c3": "var(--c3)",
  "c4": "var(--c4)", "c5": "var(--c5)", "c6": "var(--c6)", "c7": "var(--c7)",
  "c8": "var(--c8)", "ap-review": "var(--cx)", "c9": "var(--c9)", "final": "var(--cx)",
};

const CONCEPT_SHORT = {
  "c1": "Classes & Objects", "c2": "Strings", "c3": "Conditionals", "c4": "Iteration",
  "c5": "ArrayLists", "c6": "Arrays", "c7": "2D Arrays", "c8": "Recursion",
  "ap-review": "AP Review", "c9": "Data & Regression", "final": "Final Moments",
  "course-info": "Course Info",
};

function conceptById(id) {
  return CONCEPTS.find((c) => c.id === id);
}

function weekOrder(w) {
  // s1 weeks first, then s2 — used for before/after comparisons
  return (w.semester === "s1" ? 0 : 1000) + w.week;
}
const CURRENT_ORDER = (CURRENT.semester === "s1" ? 0 : 1000) + CURRENT.week;

function weekStatus(w) {
  const o = weekOrder(w);
  if (o === CURRENT_ORDER) return "now";
  return o < CURRENT_ORDER ? "past" : "upcoming";
}

function chip(id) {
  const c = conceptById(id);
  const label = CONCEPT_SHORT[id] || (c ? c.title : id);
  const color = CONCEPT_COLOR[id] || "var(--cx)";
  const href = id === "final" || id === "ap-review" || id === "course-info"
    ? `topics.html#${id}` : `topics.html#${id}`;
  return `<a class="concept-chip" href="${href}"><span class="dot" style="background:${color}"></span>${label}</a>`;
}

function linkItem(item) {
  const label = item.title;
  if (item.url) {
    return `<li><a href="${item.url}" target="_blank" rel="noopener">${label}</a></li>`;
  }
  return `<li class="item-plain">${label}</li>`;
}

// ---------------------------------------------------------------- Week page
function renderWeekTable(semester) {
  const tbody = document.getElementById("week-tbody");
  if (!tbody) return;
  const rows = WEEKS.filter((w) => w.semester === semester);
  tbody.innerHTML = rows.map((w) => {
    const status = weekStatus(w);
    const rowClass = status === "now" ? "row-now" : status === "past" ? "row-past" : "";
    const badge = status === "past" ? '<span class="done-pill">Done</span>' : "";
    const chips = w.concepts.length ? w.concepts.map(chip).join("") : '<span class="empty-cell">—</span>';

    const highlights = [];
    if (w.assessments.length) highlights.push(...w.assessments.map((i) => ({ ...i, tag: "Due" })));
    if (w.slides.length) highlights.push(...w.slides.map((i) => ({ ...i, tag: "Slides" })));
    if (w.homework.length) highlights.push(...w.homework.map((i) => ({ ...i, tag: "HW" })));
    if (w.resources.length) highlights.push(...w.resources.map((i) => ({ ...i, tag: "Resource" })));
    const resourcesHtml = highlights.length
      ? `<ul class="link-list">${highlights.slice(0, 6).map((i) => {
          const cleanTitle = i.title.replace(/^S[12]:\s*/i, "").replace(/^Week\s*\d+(\s*\/\s*\d+)?[:\s]*/i, "");
          const label = `<span class="item-tag">${i.tag}</span> ${cleanTitle || i.title}`;
          return i.url
            ? `<li><a href="${i.url}" target="_blank" rel="noopener">${label}</a></li>`
            : `<li class="item-plain">${label}</li>`;
        }).join("")}</ul>`
      : '<span class="empty-cell">—</span>';

    const newsHtml = w.news.length
      ? `<ul class="link-list">${w.news.map((i) => {
          const cleanNews = i.title.replace(/^S[12]:\s*/i, "").replace(/^Week\s*\d+(\s*\/\s*\d+)?[:\s]*/i, "");
          return `<li class="item-plain">${cleanNews || i.title}</li>`;
        }).join("")}</ul>`
      : '<span class="empty-cell">—</span>';

    return `<tr class="${rowClass}" data-week-row="${w.semester}-${w.week}">
      <td data-label="Week"><span class="week-num">Week ${w.week}</span>${badge}</td>
      <td data-label="Unit">${chips}</td>
      <td data-label="Focus"><span class="focus-text">${w.focus}</span></td>
      <td data-label="Resources & Due">${resourcesHtml}</td>
      <td data-label="CS in the News">${newsHtml}</td>
    </tr>`;
  }).join("");
}

function renderNowCard() {
  const el = document.getElementById("now-card");
  if (!el) return;
  const w = WEEKS.find((w) => w.semester === CURRENT.semester && w.week === CURRENT.week);
  if (!w) { el.style.display = "none"; return; }
  const chips = w.concepts.map(chip).join(" ");
  el.innerHTML = `
    <div style="flex:1; min-width:240px;">
      <div class="now-kicker">Right now &middot; ${SEM_LABEL[w.semester]}, Week ${w.week}</div>
      <h2>${chips || "—"}</h2>
      <p>${w.focus}</p>
    </div>`;
}

function initSemToggle() {
  const buttons = document.querySelectorAll("[data-sem-btn]");
  if (!buttons.length) return;
  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      buttons.forEach((b) => b.setAttribute("aria-pressed", "false"));
      btn.setAttribute("aria-pressed", "true");
      renderWeekTable(btn.dataset.semBtn);
      scrollToNow();
    });
  });
}

function scrollToNow() {
  const raf = window.requestAnimationFrame || ((fn) => setTimeout(fn, 0));
  raf(() => {
    const row = document.querySelector('tr.row-now');
    if (row && row.scrollIntoView) row.scrollIntoView({ block: "center", behavior: "smooth" });
  });
}

function initWeekPage() {
  if (!document.getElementById("week-tbody")) return;
  renderNowCard();
  const startSem = CURRENT.semester;
  const startBtn = document.querySelector(`[data-sem-btn="${startSem}"]`);
  if (startBtn) {
    document.querySelectorAll("[data-sem-btn]").forEach((b) => b.setAttribute("aria-pressed", "false"));
    startBtn.setAttribute("aria-pressed", "true");
  }
  renderWeekTable(startSem);
  initSemToggle();
  scrollToNow();
}

// --------------------------------------------------------------- Topic page
function sectionOrder(name) {
  const order = ["Slides", "Resources", "Resources and Code", "Code", "Homework", "Assessments", "Quiz/Test", "Quizzes", "Quiz/Tests", "Reviews", "CS in the News", "General"];
  const i = order.indexOf(name);
  return i === -1 ? order.length : i;
}

function conceptSpanLabel(c) {
  const weeks = WEEKS.filter((w) => w.concepts.includes(c.id));
  if (!weeks.length) return "";
  const first = weeks[0], last = weeks[weeks.length - 1];
  const firstLabel = `${SEM_LABEL[first.semester]} Wk ${first.week}`;
  const lastLabel = `${SEM_LABEL[last.semester]} Wk ${last.week}`;
  return first === last || (first.semester === last.semester && first.week === last.week)
    ? firstLabel : `${firstLabel} &ndash; ${lastLabel}`;
}

function isCurrentConcept(id) {
  const w = WEEKS.find((w) => w.semester === CURRENT.semester && w.week === CURRENT.week);
  return !!w && w.concepts.includes(id);
}

function renderTopics() {
  const root = document.getElementById("concept-list");
  const jump = document.getElementById("concept-jump");
  if (!root) return;

  jump.innerHTML = CONCEPTS.map((c) => {
    const color = CONCEPT_COLOR[c.id] || "var(--cx)";
    return `<a href="#${c.id}"><span class="dot" style="background:${color};display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;"></span>${c.title}</a>`;
  }).join("");

  const anyCurrent = CONCEPTS.some((c) => isCurrentConcept(c.id));

  root.innerHTML = CONCEPTS.map((c, idx) => {
    const isOpen = anyCurrent ? isCurrentConcept(c.id) : idx === 0;
    const color = CONCEPT_COLOR[c.id] || "var(--cx)";
    const sections = Object.entries(c.sections)
      .filter(([, items]) => items.length)
      .sort((a, b) => sectionOrder(a[0]) - sectionOrder(b[0]));
    const span = conceptSpanLabel(c);
    const sectionsHtml = sections.map(([name, items]) => `
      <div class="section-block">
        <h3>${name}</h3>
        <ul>${items.map((i) => {
          const weekTag = i.week ? `<span class="week-tag">Wk ${i.week}${i.semester ? " (" + i.semester.toUpperCase() + ")" : ""}</span>` : "";
          const cleanTitle = i.title.replace(/^S[12]:\s*/i, "").replace(/^Week\s*\d+(\s*\/\s*\d+)?[:\s]*/i, "");
          const label = `${weekTag}${cleanTitle || i.title}`;
          return i.url
            ? `<li><a href="${i.url}" target="_blank" rel="noopener">${label}</a></li>`
            : `<li class="item-plain">${label}</li>`;
        }).join("")}</ul>
      </div>`).join("");

    return `<section class="concept-block" id="${c.id}" data-open="${isOpen ? "true" : "false"}">
      <button class="concept-head" data-toggle="${c.id}" aria-expanded="${isOpen}">
        <span class="dot" style="background:${color}"></span>
        <h2>${c.title}</h2>
        ${isCurrentConcept(c.id) ? '<span class="now-pill">Now</span>' : ""}
        <span class="concept-span">${span}</span>
        <span class="chevron">&#9656;</span>
      </button>
      <div class="concept-body">
        <div class="section-grid">${sectionsHtml || '<p class="empty-cell">Nothing here yet.</p>'}</div>
      </div>
    </section>`;
  }).join("");

  root.querySelectorAll("[data-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const block = btn.closest(".concept-block");
      const open = block.dataset.open === "true";
      block.dataset.open = open ? "false" : "true";
      btn.setAttribute("aria-expanded", String(!open));
    });
  });

  // open + scroll to a concept if URL has a hash
  if (location.hash) {
    const target = document.querySelector(location.hash);
    if (target && target.classList.contains("concept-block")) {
      document.querySelectorAll(".concept-block").forEach((b) => (b.dataset.open = "false"));
      target.dataset.open = "true";
      setTimeout(() => target.scrollIntoView({ block: "start", behavior: "smooth" }), 50);
    }
  }
}

function initTopicsPage() {
  if (!document.getElementById("concept-list")) return;
  renderTopics();
}

document.addEventListener("DOMContentLoaded", () => {
  initWeekPage();
  initTopicsPage();
});
