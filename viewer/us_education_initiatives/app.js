(function () {
  const root = document.getElementById("app");
  const data = window.US_EDUCATION_INITIATIVES_DATA;
  if (!root) throw new Error("App root not found.");
  window.InitiativeAtlas.create(root, data);
})();
