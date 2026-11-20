(() => {
  const modal = document.querySelector("#task-modal");
  const form = document.querySelector("#task-form");
  const titleInput = document.querySelector("#task-title");
  const modalTitle = document.querySelector("#modal-title");
  const saveButton = document.querySelector("#save-task");
  const statusTabs = [...document.querySelectorAll("[data-status]")];
  const rows = [...document.querySelectorAll("[data-task-row]")];
  const searchInput = document.querySelector("#task-search");
  const categoryFilter = document.querySelector("#category-filter");
  const noResults = document.querySelector("#no-results");
  let activeStatus = "all";

  const openModal = (task) => {
    form.reset();
    if (task) {
      modalTitle.textContent = "Edit task";
      saveButton.innerHTML = 'Save changes <span>↗</span>';
      form.action = `/tasks/${task.dataset.id}/edit`;
      titleInput.value = task.dataset.title;
      document.querySelector("#task-notes").value = task.dataset.notes;
      document.querySelector("#task-category").value = task.dataset.category;
      document.querySelector("#task-priority").value = task.dataset.priority;
      document.querySelector("#task-due-date").value = task.dataset.dueDate;
    } else {
      modalTitle.textContent = "Add a task";
      saveButton.innerHTML = 'Add to my list <span>↗</span>';
      form.action = "/tasks";
    }
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
    window.setTimeout(() => titleInput.focus(), 80);
  };

  const closeModal = () => {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
  };

  document.querySelectorAll("[data-open-modal]").forEach((button) => {
    button.addEventListener("click", () => openModal());
  });
  document.querySelectorAll("[data-close-modal]").forEach((button) => {
    button.addEventListener("click", closeModal);
  });
  document.querySelectorAll("[data-edit-task]").forEach((button) => {
    button.addEventListener("click", () => openModal(button));
  });
  modal.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.classList.contains("is-open")) closeModal();
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      searchInput.focus();
    }
  });

  const filterTasks = () => {
    const query = searchInput.value.trim().toLowerCase();
    const category = categoryFilter.value;
    let visibleCount = 0;
    rows.forEach((row) => {
      const matchesStatus = activeStatus === "all" || row.dataset.status === activeStatus;
      const matchesCategory = category === "all" || row.dataset.category === category;
      const matchesQuery = !query || row.dataset.title.includes(query) || row.dataset.notes.includes(query);
      const visible = matchesStatus && matchesCategory && matchesQuery;
      row.hidden = !visible;
      if (visible) visibleCount += 1;
    });
    if (noResults) noResults.hidden = visibleCount > 0;
  };

  statusTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      activeStatus = tab.dataset.status;
      statusTabs.forEach((item) => item.classList.toggle("active", item === tab));
      filterTasks();
    });
  });
  searchInput.addEventListener("input", filterTasks);
  categoryFilter.addEventListener("change", filterTasks);

  document.querySelectorAll("[data-filter-link]").forEach((link) => {
    link.addEventListener("click", () => {
      activeStatus = link.dataset.filterLink;
      statusTabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.status === activeStatus));
      filterTasks();
    });
  });
  document.querySelectorAll("[data-category-link]").forEach((link) => {
    link.addEventListener("click", () => {
      categoryFilter.value = link.dataset.categoryLink;
      filterTasks();
      document.querySelector("#task-list").scrollIntoView({ behavior: "smooth" });
    });
  });

  document.querySelectorAll("[data-delete-form]").forEach((deleteForm) => {
    deleteForm.addEventListener("submit", (event) => {
      if (!window.confirm("Remove this task from your list?")) event.preventDefault();
    });
  });

  const menuButton = document.querySelector("#mobile-menu");
  const sidebar = document.querySelector("#sidebar");
  menuButton.addEventListener("click", () => {
    const isOpen = sidebar.classList.toggle("is-open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
    menuButton.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
  });
  document.addEventListener("click", (event) => {
    if (window.innerWidth <= 760 && sidebar.classList.contains("is-open")
      && !sidebar.contains(event.target) && !menuButton.contains(event.target)) {
      sidebar.classList.remove("is-open");
      menuButton.setAttribute("aria-expanded", "false");
    }
  });

  const filterButton = document.querySelector("#filter-toggle");
  filterButton.addEventListener("click", () => {
    const expanded = filterButton.getAttribute("aria-expanded") === "true";
    filterButton.setAttribute("aria-expanded", String(!expanded));
    categoryFilter.classList.toggle("is-emphasized", !expanded);
    if (!expanded) categoryFilter.focus();
  });

  document.querySelectorAll(".flash").forEach((flash) => {
    window.setTimeout(() => flash.classList.add("is-hiding"), 4200);
    window.setTimeout(() => flash.remove(), 4700);
  });
})();
