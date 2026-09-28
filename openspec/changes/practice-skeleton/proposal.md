> 練習：本 change 是 `feature-to-spec` 的演練，對應 roadmap 的 #1 專案骨架（ticket #4）。PR 不會 merge；正式的 change `project-skeleton` 與 ticket #1、#2 不受影響。

## Why

之後每個 Feature 都要在程式 repo 寫碼、在 PR 上跑檢查，並由不同 agent 協作。現在程式 repo `cross-node-file-transfer` 只有 README（研究 F1），沒有建置、沒有 CI、也沒有工程規則；下一個 Feature #2 Finalize 協議無處落腳。本 Feature 建立這個起點。

依據：project intent `6d007d1`、高層設計 `system-design.md` 與 `design-decisions.md` `627eb12`、roadmap `6d007d1`、決策 PD-04、PD-05、PD-07、PD-08、PD-10；研究見 [2026-09-29-practice-skeleton](../../../docs/research/2026-09-29-practice-skeleton.md)。

## What Changes

範圍已由 Project Lead 談定（Q-1）。

程式 repo `cross-node-file-transfer`：

- **可見度**：程式 repo 改成 public，GitHub 才能強制 branch protection（Q-4；執行見 Q-6）。
- **建置**：Java 21 的 Maven 多模組，只有 parent pom 與 #2 需要的 core 模組；乾淨 clone 上 `mvn -B verify` 會建置並執行測試（PD-04；研究 F6、F7、F10）。
- **CI 必要 checks**：PR 與推上新 commit 時，對 PR 目前的 head 執行建置與測試；必要 check 的名稱記在程式 repo，並由 `main` 的 branch protection 強制（Q-4）。
- **工程規則**：程式 repo 自己的 `AGENTS.md`，以 root 的 `AGENTS.md` 為底稿（Q-2），以 `CLAUDE.md` 引用它；單獨 clone 程式 repo 時就讀得到（研究 F3、A1）。

root repo `cross-node-root`：只有本 change 的文件，不改 root 的 `AGENTS.md`。

### 不做

- commit 訊息檢查（hook、CI job）：不在本 Feature（Q-3）。
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

- 程式 repo：可見度由 private 改成 public（對外公開，不容易收回；Q-6）；新增 `pom.xml`、core 模組、`.github/workflows/` 的 CI、`AGENTS.md`、`CLAUDE.md`、`.gitignore`；開一個 PR。
- root repo：本 change 的文件；root PR 就是 `feature/practice-skeleton`。
- 跨 Feature 的共用限制（core-guarantees、service-objectives）是產品行為，本 Feature 不碰（研究 A2）。

## 待決與依賴

| ID | 問題 | 是否阻擋 Design | 決策者 |
| --- | --- | --- | --- |
| Q-1 | ~~範圍：上面「What Changes」與「不做」~~ **已決定：照提案，工程規則放在程式 repo 自己的 `AGENTS.md`，root 只放本 change 的文件；commit 訊息檢查不加進範圍** | — | Project Lead 回答「A」（2026-09-29），選項 A 為「照提案；工程規則放進程式 repo，單獨 clone 也讀得到」，否決 B「規則只放 root」與 C「範圍加上 commit 訊息檢查」 |
| Q-2 | ~~程式 repo 的 `AGENTS.md` 用哪份內容起頭~~ **已決定：root 的版本（`AGENTS.md` blob `c93055be4c32`），只改兩處：scope 表換成程式 repo 的 Java package，刪掉「本 repo 是 root repo」的說明**。這偏離 PD-05（採 gigaxfer 工作目錄的 `AGENTS.md`）；練習只記在這裡，不改 main 的決策紀錄，正式走時要另立 PD 取代 PD-05 的這一部分 | — | Project Lead 回答「a」（2026-09-29），選項 A 為「root 的版本，改 scope 表與 root 說明兩處」，否決 B「gigaxfer 新版改三處加 scope 表」與 C「PD-05 釘的舊版」 |
| Q-3 | ~~commit 訊息檢查（hook、CI job）屬不屬於本 Feature~~ **已決定：不屬於**（隨 Q-1 選 A 否決 C）；要做時另開 Feature 以 MODIFIED 修改 `engineering-baseline` | — | 同 Q-1 |
| Q-4 | ~~程式 repo 是 private，GitHub 無法強制必要 check（研究 F2）；必要 check 是否只由流程判定~~ **已決定：把程式 repo 改成 public，以 `main` 的 branch protection 強制必要 checks**（EB-02） | — | Project Lead 回答「B」（2026-09-29），選項 B 為「把服務 repo 改成 public，打開 branch protection 由 GitHub 強制」，否決 A「由流程判定」與 C「升級 GitHub Pro」 |
| Q-6 | 程式 repo 改成 public 由誰、何時執行：改可見度是對外且難收回的操作，不在本練習的授權內 | 否：擋 EB-02 的實作與驗收，不擋 Design | Project Lead |
| Q-5 | 決策紀錄沒有依 loop-engineering D63 記下「確認 roadmap 並選定 #1」（研究 F12）；本練習以 Project Lead 2026-09-29 的指示視為選定 | 否 | Project Lead |

依賴：無上游 Feature。需要程式 repo 的 GitHub Actions 可用；EB-02 需要程式 repo 先改成 public 才能設 branch protection（Q-6）。

## SA 確認

尚未確認。
