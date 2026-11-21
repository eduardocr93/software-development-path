export function registerAppEvents(handlers) {
  document.addEventListener("submit", (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    event.preventDefault();

    if (form.id === "login-form") handlers.submitAuth(form, "login");
    if (form.id === "register-form") handlers.submitAuth(form, "register");
    if (form.id === "product-form") handlers.submitProduct(form);
    if (form.id === "checkout-form") handlers.submitCheckout(form);
  });

  document.addEventListener("click", async (event) => {
    if (!(event.target instanceof Element)) return;

    const menuButton = event.target.closest(".menu-toggle");
    if (menuButton) {
      const nav = handlers.header.querySelector(".main-nav");
      const expanded = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!expanded));
      nav.classList.toggle("nav-open", !expanded);
      return;
    }

    if (event.target.closest('[data-action="logout"]')) {
      handlers.logout();
      return;
    }

    const addButton = event.target.closest("[data-add-product]");
    if (addButton) {
      const quantity = document.querySelector("#detail-quantity")?.value || "1";
      await handlers.addToCart(addButton.dataset.addProduct, quantity);
      return;
    }

    const cartButton = event.target.closest("[data-cart-action]");
    if (cartButton) {
      await handlers.changeCart(
        cartButton.dataset.cartAction,
        cartButton.dataset.itemId,
        cartButton.dataset.quantity,
        cartButton,
      );
      return;
    }

    const deleteButton = event.target.closest("[data-delete-product]");
    if (deleteButton) await handlers.deleteProduct(deleteButton);
  });

  document.addEventListener("input", (event) => {
    if (event.target.id === "product-search") handlers.filterProducts();
  });

  document.addEventListener("change", (event) => {
    if (event.target.id === "available-only") handlers.filterProducts();
  });

  window.addEventListener("hashchange", handlers.renderRoute);
}