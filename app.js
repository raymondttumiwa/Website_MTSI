(() => {
  const navItems = [...document.querySelectorAll(".nav-item")];
  const sections = [...document.querySelectorAll(".section-anchor")];
  const sidebar = document.querySelector(".sidebar");
  const menuToggle = document.querySelector(".menu-toggle");

  const setActiveNav = (id) => navItems.forEach((item) => item.classList.toggle("is-active", item.dataset.nav === id));
  const observer = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) setActiveNav(visible.target.id);
  }, { rootMargin: "-25% 0px -60%", threshold: [0, .25, .5] });
  sections.forEach((section) => observer.observe(section));

  navItems.forEach((item) => item.addEventListener("click", () => {
    sidebar?.classList.remove("is-open");
    menuToggle?.setAttribute("aria-expanded", "false");
  }));
  menuToggle?.addEventListener("click", () => {
    const open = sidebar.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", String(open));
  });

  const cards = [...document.querySelectorAll(".customer-card")];
  const filterButtons = [...document.querySelectorAll(".filter-button")];
  const search = document.querySelector("#customer-search");
  const emptyState = document.querySelector("#empty-state");
  const moreButton = document.querySelector("#portfolio-more");
  const initialCardCount = 8;
  let activeFilter = "all";
  let showAllCards = false;
  cards.forEach((card) => {
    const name = card.querySelector("h3")?.textContent.trim() || "";
    card.dataset.brand = name;
  });
  const applyFilters = () => {
    const query = (search?.value || "").trim().toLowerCase();
    const matchingCards = cards.filter((card) => {
      const matchesFilter = activeFilter === "all" || card.dataset.type === activeFilter;
      return matchesFilter && (!query || card.textContent.toLowerCase().includes(query));
    });
    const visibleLimit = showAllCards ? matchingCards.length : initialCardCount;
    cards.forEach((card) => {
      const index = matchingCards.indexOf(card);
      card.hidden = index < 0 || index >= visibleLimit;
    });
    if (emptyState) emptyState.hidden = matchingCards.length > 0;
    if (moreButton) {
      moreButton.hidden = matchingCards.length <= initialCardCount;
      moreButton.innerHTML = showAllCards ? 'Show fewer <span>↑</span>' : 'Discover all customers <span>↓</span>';
    }
  };
  filterButtons.forEach((button) => button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    showAllCards = false;
    filterButtons.forEach((item) => item.classList.toggle("is-selected", item === button));
    applyFilters();
  }));
  search?.addEventListener("input", () => {
    showAllCards = false;
    applyFilters();
  });
  moreButton?.addEventListener("click", () => {
    showAllCards = !showAllCards;
    applyFilters();
  });
  applyFilters();

  document.querySelector("#inquiry-form")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const subject = encodeURIComponent(`${data.get("interest")} enquiry — ${data.get("company")}`);
    const body = encodeURIComponent(`Name: ${data.get("name")}\nCompany: ${data.get("company")}\nEmail: ${data.get("email")}\nInterest: ${data.get("interest")}\n\nMessage:\n${data.get("message") || "(No additional message)"}`);
    window.location.href = `mailto:mtsi@muliatsi.co.id?subject=${subject}&body=${body}`;
  });
  document.querySelector("#year").textContent = new Date().getFullYear();
})();
