(function () {
  "use strict";

  function renderScratchScripts() {
    if (!window.scratchblocks) return;
    window.scratchblocks.renderMatching("pre.scratchblocks", {
      style: "scratch3",
      languages: ["en"],
      scale: 0.82
    });
    document.documentElement.classList.add("scratchblocks-ready");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderScratchScripts);
  } else {
    renderScratchScripts();
  }
}());
