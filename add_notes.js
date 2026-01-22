document.querySelectorAll(".div-jacket").forEach((Block) => {
  console.log(Block.clientWidth);

  // 親を基準にする
  Block.style.position = "relative";

  // 既に追加済みならスキップ（再実行対策）
  if (Block.querySelector(".jacket-text")) return;

  const textDiv = document.createElement("div");
  textDiv.className = "jacket-text";
  textDiv.textContent = "111/55";

  // 中央配置
  Object.assign(textDiv.style, {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    color: "white",
    fontWeight: "bold",
    fontSize: "18px",
    textShadow: "0 0 4px black",
    pointerEvents: "none"
  });

  Block.appendChild(textDiv);
});