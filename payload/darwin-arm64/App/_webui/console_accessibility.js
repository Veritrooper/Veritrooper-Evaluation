(function () {
  "use strict";

  function syncSegmentedState(root) {
    (root || document).querySelectorAll(".modes,.utilsw").forEach(function (group) {
      if (!group.getAttribute("aria-label")) {
        group.setAttribute("aria-label", group.id
          ? group.id.replace(/([a-z])([A-Z])/g, "$1 $2")
          : "Selection");
      }
      group.querySelectorAll(":scope > button").forEach(function (button) {
        var value = button.classList.contains("on") ? "true" : "false";
        if (button.getAttribute("aria-pressed") !== value) {
          button.setAttribute("aria-pressed", value);
        }
      });
    });
  }

  window.installSegmentedA11y = function (root) {
    syncSegmentedState(root || document);
    var observer = new MutationObserver(function (records) {
      if (records.some(function (record) {
        return record.type === "childList" || record.attributeName === "class";
      })) syncSegmentedState(root || document);
    });
    observer.observe((root || document).body || root, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ["class"],
    });
    return observer;
  };
})();
