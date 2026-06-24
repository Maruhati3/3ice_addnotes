javascript: (async () => {
  const url =
    "https://raw.githubusercontent.com/Maruhati3/3ice_addnotes/main/merged.json";
  const data = await fetch(url).then((r) => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  });
  const map = new Map(data.map((o) => [o.title, o]));
  const diffKey = { 0: "bSP", 1: "BSP", 2: "DSP", 3: "ESP", 4: "CSP" };
  const otp = document.getElementById(
    "jacket-6bid6d9qPQ80DOqiidQQ891o6Od8801l-2",
  );
  if (otp) {
    otp.title = "Over The Period";
  }
  document.querySelectorAll(".div-jacket").forEach((b) => {
    try {
      const img = b.querySelector("img");
      if (!img) return;
      const title = img.title?.trim();
      if (!title) return;
      const m = img.className.match(/diff-(\d)/);
      if (!m) return;
      const key = diffKey[m[1]];
      if (!key) return;
      const row = map.get(title);
      if (!row) return;
      const bpm = row.BPM ?? "";
      const notes = row[key] ?? "";
      if (!bpm && !notes) return;
      b.querySelector(".jacket-text")?.remove();
      b.style.position = "relative";
      const fs = Math.min(28, Math.max(10, b.clientWidth * 0.2));
      const d = document.createElement("div");
      d.className = "jacket-text";
      d.innerHTML = `<div>${bpm}</div><div>${notes}</div>`;
      Object.assign(d.style, {
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%,-50%)",
        color: "white",
        fontWeight: "bold",
        fontSize: fs + "px",
        textShadow: "0 0 4px black",
        textAlign: "center",
        lineHeight: "1.2",
        pointerEvents: "none",
        zIndex: 999,
      });
      b.appendChild(d);
    } catch (e) {
      console.log(e);
    }
  });
})().catch(console.error);
javascript: (function () {
  const userInput = "1";
  const versionSelections = userInput
    .split(",")
    .map((selection) => selection.trim());
  let versionRanges = [];
  versionSelections.forEach((selection) => {
    switch (selection) {
      case "1":
        versionRanges.push([1, 13]);
        break;
      case "2":
        versionRanges.push([14, 16]);
        break;
      case "3":
        versionRanges.push([17, 20]);
        break;
      default:
        alert(
          "無効な入力です。1,2,3のいずれかをカンマ区切りで入力してください。",
        );
        return;
    }
  });

  // ========================================
  // 16.40未満を16.40へ集約
  // ========================================

  // 16.40行を探す
  const targetRow = [...document.querySelectorAll("tr")].find((tr) => {
    const p = tr.querySelector(".p-tier-label");
    return p && p.textContent.trim() === "16.40";
  });

  if (targetRow) {
    const targetDiv = targetRow.querySelector(".div-jackets");
    [...document.querySelectorAll("tr")].forEach((tr) => {
      if (tr === targetRow) return;
      const p = tr.querySelector(".p-tier-label");
      if (!p) return;
      const lv = parseFloat(p.textContent);
      if (isNaN(lv)) return;
      // 16.40未満
      if (lv < 16.4) {
        const jackets = tr.querySelectorAll(".div-jacket");
        jackets.forEach((j) => {
          // 表示中のみ移動
          if (j.style.display !== "none") {
            targetDiv.appendChild(j);
          }
        });
      }
    });
  }

  document.querySelectorAll(".div-jacket").forEach(function (div) {
    const title = div.firstChild.getAttribute("title");
    if (title) {
      const trimmedTitle = title.trim();
      const songData = ALL_SONG_DATA.find(
        (song) => song.song_name.trim() === trimmedTitle,
      );
      if (songData) {
        const isInSelectedRange = versionRanges.some(
          (range) =>
            songData.version_num >= range[0] &&
            songData.version_num <= range[1],
        );
        div.style.display = isInSelectedRange ? "" : "none";
      }
    }
  });
  document.querySelectorAll("tr").forEach(function (tr) {
    const divJackets = tr.querySelector(".td-jackets");
    if (divJackets) {
      const jackets = divJackets.querySelectorAll(".div-jacket");
      const allHidden = Array.from(jackets).every(
        (jacket) => jacket.style.display === "none",
      );
      if (allHidden) {
        tr.style.display = "none";
      }
    }
  });
  let visibleRows = Array.from(document.querySelectorAll("tr")).filter(
    (tr) => tr.style.display !== "none",
  );
  visibleRows.forEach((tr, index) => {
    tr.style.backgroundColor = index % 2 === 0 ? "#292a33" : "#17171c";
  });
  document.getElementById("lights").value = "F10";
  lightsSelectDidChange();
  
  
})();
