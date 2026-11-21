export function createRouter({ routes, beforeRoute, notFound }) {
  return async function renderRoute() {
    beforeRoute?.();
    const [routeName, ...encodedParts] = location.hash.replace(/^#\/?/, "").split("/");
    const route = routeName || "home";
    const handler = routes[route];

    if (!handler) return notFound();
    return handler(...encodedParts.map((part) => decodeURIComponent(part)));
  };
}