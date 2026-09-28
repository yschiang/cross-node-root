## Why

後續每個 Feature 都需要一個可以建置、測試並在 PR 上自動檢查的起點，也需要所有 agent 共同遵守的工程規則。本 Feature 建立這個起點，是 M1 的第一個 Feature（ticket #1；roadmap；PD-05、PD-08）。依 loop-engineering D56 由人協調完成，歷程標明「人工協調」。

## What Changes

- **Maven 多模組骨架**：Java 21 的 parent pom 與下一個 Feature「Finalize 協議」（#2）需要的 core 模組，可以在乾淨的 clone 上執行建置與測試（PD-04）。
- **CI 必要 checks**：PR 上自動建置並執行測試；必要 check 的名稱與內容在 design 列出，經 Project Lead 核准後才生效。
- **工程規則**：採用 gigaxfer 工作目錄中的 `AGENTS.md`（sha256 `f69d669a97424657ef78c9fc9a4ebb3d123257d5886aa4a688d8ce7fdff77316`，PD-05），並以 `CLAUDE.md` 引用它。

### 不做

- 任何產品行為：Finalize、ingest、同步、HTTP 端點、DB schema 都屬於之後的 Feature。
- 下一個 Feature 用不到的模組（library、sync-service、cli、nfs-acceptance）：到了需要它們的 Feature 再建。
- Oracle Free 的 CI job：第一個用到 DB 的 Feature 再加。
- CD、部署與監控設定。

## Capabilities

### New Capabilities

- `engineering-baseline`：開發與交付本專案必須成立的工程條件，包括乾淨 clone 可建置測試、PR 必要 checks、agent 遵守的工程規則。它不是產品行為；之後改動 CI 或工程規則的 Feature 以 MODIFIED 修改它（PD-07）。

### Modified Capabilities

無。

## Impact

- 影響兩個 repo（PD-10）：程式 repo `cross-node-file-transfer` 新增 `pom.xml`、core 模組、`.github/workflows/` 的 CI 設定、`.gitignore`；root repo `cross-node-root` 放共用的 `AGENTS.md`、`CLAUDE.md`。確切分法見待決 Q-4。
- 之後所有 Feature 都建立在這個骨架與規則上。
- 參考：gigaxfer 的 `.github/workflows/ci.yml` 與 P00 的建置假設，只作設計參考，不直接沿用為證據。

## 待決與依賴

| ID | 問題 | 是否阻擋 Design | 決策者 |
| --- | --- | --- | --- |
| Q-1 | ~~專案骨架沒有產品行為，規格放哪~~ **已決定：新增 `engineering-baseline` 能力規格**（PD-07） | — | Lead 回答「ok 用 engineering-baseline」（2026-09-28） |
| Q-2 | ~~只建下一個 Feature 需要的 core 模組，或一次建好 P00 的五個模組空殼~~ **已決定：不建空殼，只建 parent 與 core**；其他模組到了需要它們的 Feature 再建 | — | Lead 回答「先不要建空殼」（2026-09-28） |
| Q-3 | ~~`AGENTS.md` 的 gigaxfer 專屬引用怎麼處理~~ **已決定：原樣複製，只改三處並在 PR 列出改動**：① 開頭「與 `goal.md`、`reviewer.md` 衝突時以這兩份為準」，本 repo 沒有這兩份檔案；② `docs/validation/P0N-validation.md` 路徑，改為本 repo 的驗證文件位置（由本 Feature 的 design 決定）；③ `FaultInjectingNfs`、`FaultInjectingDataSource` 等尚不存在的類別名，改為不指名的說法。其餘文字原樣 | — | Lead 回答「AGENTS.md 照你建議」（2026-09-28） |

| Q-4 | root 與程式 repo 分開後（PD-10），EB-01～EB-03 各適用哪個 repo？共用規則放 root 時，agent 從程式 repo 啟動讀不讀得到：Claude Code 會往上層目錄讀 `CLAUDE.md`；Codex 預設從所在 git repo 的根目錄往下找 `AGENTS.md`，可能讀不到上一層（design 時實測） | 是：影響 EB-01～EB-03 的寫法 | Project Lead |
| Q-5 | 工程規則採哪一版 `AGENTS.md`：PD-05 釘的舊版（sha `f69d669…`），或 gigaxfer 後來加了 commit 訊息規範的新版 | 是：影響 EB-03 的內容 | Project Lead |

依賴：無上游 Feature。需要兩個 repo 的 GitHub Actions 可用（repo 已建立）。

## SA 確認

尚未確認。
