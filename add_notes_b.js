window.MakeFlareImage = function () {
  const DATA_URL =
    "https://raw.githubusercontent.com/Maruhati3/3ice_addnotes/refs/heads/main/data.json";

  const diffKeyMap = {
    0: "bSP",
    1: "BSP",
    2: "DSP",
    3: "ESP",
    4: "CSP"
  };

  // ★ 追加：タイトル正規化関数
  const normalizeTitle = (str) =>
    str
      .trim()
      .replace(/&quot;/g, '"')
      .replace(/[“”]/g, '"')
      .replace(/[‘’]/g, "'");

  fetch(DATA_URL)
    .then(res => res.json())
    .then(data => {
      // ★ Map 作成時に正規化
      const dataMap = new Map(
        data.map(row => [normalizeTitle(row.title), row])
      );

      document.querySelectorAll(".div-jacket").forEach(Block => {
        const img = Block.querySelector("img");
        if (!img) return;

        // ★ 取得した title も正規化
        const title = img.title ? normalizeTitle(img.title) : "";
        if (!title) return;

        const diffMatch = img.className.match(/diff-(\d)/);
        if (!diffMatch) return;

        const key = diffKeyMap[diffMatch[1]];
        if (!key) return;

        const row = dataMap.get(title);
        if (!row) return;

        const value = row[key];
        if (!value || value === "-") return;

        if (Block.querySelector(".jacket-text")) return;

        const w = Block.clientWidth;
        const fontSize = Math.min(
          22,
          Math.max(12, w * 0.18)
        );

        Block.style.position = "relative";

        const textDiv = document.createElement("div");
        textDiv.className = "jacket-text";
        textDiv.textContent = value;

        Object.assign(textDiv.style, {
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          color: "white",
          fontWeight: "bold",
          fontSize: `${fontSize}px`,
          textShadow: "0 0 4px black",
          pointerEvents: "none",
          zIndex: 5,
          whiteSpace: "nowrap"
        });

        Block.appendChild(textDiv);
      });
    })
    .catch(err => {
      console.error("data.json の取得に失敗しました", err);
    });
};
