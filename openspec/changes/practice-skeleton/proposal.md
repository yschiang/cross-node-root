> 練習：本 change 是 `feature-to-spec` 的演練，對應 roadmap 的 #1 專案骨架（ticket #4）。PR 不會 merge；正式的 change `project-skeleton` 與 ticket #1、#2 不受影響。

## Why

之後每個 Feature 都要在程式 repo 寫碼、在 PR 上跑檢查，並由不同 agent 協作。現在程式 repo `cross-node-file-transfer` 只有 README（研究 F1），沒有建置、沒有 CI、也沒有工程規則；下一個 Feature #2 Finalize 協議無處落腳。本 Feature 建立這個起點。

依據：project intent `6d007d1`、高層設計 `system-design.md` 與 `design-decisions.md` `627eb12`、roadmap `6d007d1`、決策 PD-04、PD-05、PD-07、PD-08、PD-10；研究見 [2026-09-29-practice-skeleton](../../../docs/research/2026-09-29-practice-skeleton.md)。

## What Changes

**提案，待 Project Lead 談定範圍。**

程式 repo `cross-node-file-transfer`：

- **建置**：Java 21 的 Maven 多模組，只有 parent pom 與 #2 需要的 core 模組；乾淨 clone 上 `mvn -B verify` 會建置並執行測試（PD-04；研究 F6、F7、F10）。
- **CI 必要 checks**：PR 與推上新 commit 時，對 PR 目前的 head 執行建置與測試；必要 check 的名稱記在程式 repo。
- **工程規則**：程式 repo 自己的 `AGENTS.md`，以 `CLAUDE.md` 引用它；單獨 clone 程式 repo 時就讀得到（研究 F3、A1）。

root repo `cross-node-root`：只有本 change 的文件，不改 root 的 `AGENTS.md`。

### 不做

- 任何產品行為：寫入、Finalize、ingest、同步、HTTP 端點、DB schema，都屬之後的 Feature。
- #2 用不到的模組（sync-service、library starter、cli）：到用得到的 Feature 再建。
- Oracle Free 的 CI job：第一個用到 DB 的 Feature 再加。
- CD、部署、監控設定。
- 改 root 的 `AGENTS.md`、`CLAUDE.md`。

## Capabilities

### New Capabilities

- `engineering-baseline`：開發與交付本產品必須成立的工程條件（PD-07）。不是產品行為；之後改 CI 或工程規則的 Feature 以 MODIFIED 修改它。

### Modified Capabilities

無。

## Impact

- 程式 repo：新增 `pom.xml`、core 模組、`.github/workflows/` 的 CI、`AGENTS.md`、`CLAUDE.md`、`.gitignore`；開一個 PR。
- root repo：本 change 的文件；root PR 就是 `feature/practice-skeleton`。
- 跨 Feature 的共用限制（core-guarantees、service-objectives）是產品行為，本 Feature 不碰（研究 A2）。

## 待決與依賴

| ID | 問題 | 是否阻擋 Design | 決策者 |
| --- | --- | --- | --- |
| Q-1 | 範圍：上面「What Changes」與「不做」 | 是 | Project Lead |
| Q-2 | 程式 repo 的 `AGENTS.md` 用哪份內容起頭：root 的版本（含 Commit 訊息規範，研究 F3）、gigaxfer 新版（F5 `b4ea97e5…`），或 PD-05 釘的舊版（`f69d669a…`） | 是：決定 EB 工程規則的內容 | Project Lead |
| Q-3 | commit 訊息檢查（hook、CI job）屬不屬於本 Feature（研究 U2） | 是：影響必要 checks 的集合 | Project Lead |
| Q-4 | 程式 repo 是 private，GitHub 無法強制必要 check（研究 F2）；必要 check 是否只由流程判定 | 否：影響驗收寫法，不影響設計 | Project Lead |
| Q-5 | 決策紀錄沒有依 loop-engineering D63 記下「確認 roadmap 並選定 #1」（研究 F12）；本練習以 Project Lead 2026-09-29 的指示視為選定 | 否 | Project Lead |

依賴：無上游 Feature。需要程式 repo 的 GitHub Actions 可用。

## SA 確認

尚未確認。
