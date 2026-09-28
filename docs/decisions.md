# 專案決策

本專案的決策紀錄。ID 用 `PD-`，避免和匯入的設計決策（`docs/design/design-decisions.md` 的 D1–D57）混淆。ID 用過不改、不刪；被取代的決策標明由哪一條取代。

本專案依 loop-engineering 的 D56 建立：Project 層先以 project-lead skill 進行，第一個真正的 feature 等 orchestrate 可用後走 feature loop。

## 現行

| ID | 決策 | 來源 |
| --- | --- | --- |
| PD-01 | gigaxfer `docs/spec.md` v0.3 拆成 11 個能力規格，放在 `openspec/specs/`，需求 ID 沿用原文。拆法與搬移結果見 [匯入紀錄](research/2026-09-28-import-from-gigaxfer.md)。**依 PD-09**：拆分結果是 SA 輸入，已搬到 `docs/research/2026-09-28-import/specs/` | Lead 回答「ok 11 個」（2026-09-28） |
| PD-02 | 以 gigaxfer main `4e9cba4` 為匯入基準。gigaxfer PR #11（設計裁定 D58）合併後，用一個 change 套用它的差異；被否決就不套。**依 PD-09**：受影響的需求還沒實作時，直接更新 SA 輸入；已實作的才開 change。**依 PD-11**：D58 不等 PR #11 合併，直接採用 | Lead 回答「先用 main」（2026-09-28） |
| PD-03 | 這次 demo 以 M1 為完成目標，在 M1 驗收時收尾。順序為 M1 → M2；Phase 0 是 M1 的第一個切片，不是獨立的 milestone（依 PD-08，即 Feature #1 專案骨架）。M2 只列 feature，是否繼續等 M1 完成後再決定 | Lead 回答「是：demo 在 M1 驗收時收尾」（2026-09-28） |
| PD-04 | 技術棧沿用匯入設計（design-decisions D38、D9）：Java 21、Maven 多模組、Spring Boot；sync service 用內嵌 HTTP 伺服器、JPA 與 Actuator；DB 為 Oracle，本機與單元測試用 H2 Oracle mode，CI 用 Oracle Free container | Lead 回答「Q4 沿用」（2026-09-28） |
| PD-05 | Phase 0 只做三件事：Maven 多模組骨架、CI 的必要 checks、工程規則；由人協調完成，歷程標明「人工協調」（loop-engineering D56）。工程規則採用 gigaxfer 工作目錄中的本機 `AGENTS.md`（未進 gigaxfer 版控；sha256 `f69d669a97424657ef78c9fc9a4ebb3d123257d5886aa4a688d8ce7fdff77316`），在 Phase 0 複製進本 repo。第一個 feature 切片為 F1（依 PD-08，即 Feature #2 Finalize 協議） | Lead 回答「Q5 ok」（2026-09-28） |
| PD-06 | Phase 0 改名為 **F0（專案骨架）**，和 F1–F7 同一套編號，避免「有 Phase 0 沒有 Phase 1」。PD-03、PD-05 中的 Phase 0 即 F0。**由 PD-08 取代** | Lead 回答「OK 照你建議」（2026-09-28） |
| PD-07 | 沒有產品行為的工程類 Feature（例如 #1 專案骨架、之後的 CI 或工程規則調整）也走 OpenSpec change，spec delta 寫在 `engineering-baseline` 能力；它記錄可單獨驗收的工程條件，不是產品行為，ID 前綴 EB | Lead 回答「ok 用 engineering-baseline」（2026-09-28）；起因是 OpenSpec 1.13.1 要求每個 change 至少一個 spec delta |
| PD-08 | **工作層級採 loop-engineering D57：Milestone → Feature → Task。** Feature 是自成一體、能單獨驗收、一個 PR 做得完的變更，對應一個 change 與一張 ticket；結果可以由系統其他部分或工程條件觀察，不一定要外部使用者看得到。Feature 以 ticket 編號識別，不用 F 編號（匯入設計的故障窗口已用 F1–F33）；task 寫在 `tasks.md`，不開 ticket。Roadmap 只列 Milestone 與 Feature，Feature 另標所屬的交付能力。取代 PD-06；專案骨架是 Feature #1 | Lead 表示「就三層吧，認知四層有點多了，而且和原生工具不合」，並補充 Feature 的價值「可以用系統看得到的價值或是驗收條款來證明，不一定要外部 user，只要是 self contained」（2026-09-28） |
| PD-09 | **需求依 loop-engineering D58 放置。** gigaxfer 匯入的 11 個能力是 SA 輸入，放在 `docs/research/2026-09-28-import/specs/`；`openspec/specs/` 只由 archive 寫入，第一個 Feature archive 前是空的。Feature SA 從輸入挑出這次要做的需求，寫進 change 的 spec delta（還沒有的用 ADDED，已有的用 MODIFIED）。跨 Feature 的共用限制（core-guarantees、service-objectives）列在 project intent。修訂 PD-01 的位置與 PD-02 的套用方式 | Lead 追問「還未實現的需求/plan 現在的流程放在哪」，指出「這很重要，我們釐清一下到底怎麼樣，不然整個流程混了」，並同意改寫方向（2026-09-28） |
| PD-10 | **採 loop-engineering D61 的 root repo 結構。** GitHub 上原本的 `cross-node-file-transfer` 改名為 `cross-node-root`，保留規劃的歷史與 ticket；另開新的 `cross-node-file-transfer` 放程式，列在 `repos.yaml`，由 `scripts/sync-repos` 拉進 `repos/`。產品名稱仍是 cross-node-file-transfer。Feature 的 ticket 開在 root；一個 Feature 動到哪些 repo，就在每個 repo 各開一個 PR | Lead 表示「我想要改成一個 root repo，然後用 cross-xxxxx 拉進來當一個 repos」，選 A 並指定「root 叫 cross-node-root」，確認執行 GitHub 改名與建 repo（2026-09-28） |
| PD-11 | **gigaxfer D58 不等 PR #11 合併，直接採用。** D58 是 Lead 2026-09-25 在 gigaxfer 做的設計裁定，PR #11 只是尚未合併。#2 Finalize 協議開 SA 前，把 D58 套進 SA 輸入與匯入設計；來源取 gigaxfer PR #11 head `2a0ab7f` 的文件，不取程式。受影響的 Feature：Finalize 協議（③ 宣告年齡用 `source_ready_at`、⑤ ESTALE、⑥ Discard）、掃描 ingest（② ingest 重讀比對）、清道夫（④ 19 天為固定常數）、sync-service 骨架（⑦ DB 時間一律 UTC、⑧ Oracle 前提）。修訂 PD-02，關閉 Q-GIGAXFER-D58 | Lead 選「A」（2026-09-28）。A 為「不等合併：D58 已是 Lead 裁定的內容，#2 開 SA 前把 D58 套進 SA 輸入和匯入設計，只取 PR #11 head `2a0ab7f` 的文件，不取程式」 |
| PD-12 | **對帳在 M1 獨立成一個 Feature。** 從 gigaxfer P03 拆出全量對帳掃：從 Source Ready 集合與 Policy 推導應有義務，補回漏掉的通知與 crash 後沒建立的義務（RC-01；T11、T18），排在掃描 ingest 之後；掃描 ingest 只做增量掃與 ingest。找出遺失或損壞的副本（Source 對帳、Target 自查，RC-02～04）要搭配修復才有用，留在 M2 的副本自動修復 | Lead 表示「對帳很重要」，對「M1 拆成獨立的 Feature，排在掃描 ingest 之後；找出遺失或損壞留在 M2」回答「可以」（2026-09-28） |
| PD-13 | **Ops 整組放在 M2，M1 不加 ops Feature。** OPS-01 Operational Readiness（`/status` 十題）與 OPS-03 受控操作（pause／resume、release、retry、ack、ops_audit）都屬 M2 的事故告警與追蹤（gigaxfer P11）。`/pending` 的 pause 過濾也移到 M2，和 pause 指令一起做。代價：M1 期間被隔離的義務，要到 M2 才有指令解除 | Lead 回答「Operation Readiness 在 M2」（2026-09-28），回應的提案為「M1 不加 ops Feature，暫停過濾跟 ops 一起放到 M2」 |

## 待決

| ID | 問題 | 影響 |
| --- | --- | --- |
| ~~Q-GIGAXFER-D58~~ | ~~gigaxfer PR #11 是否合併~~ | 已由 PD-11 關閉：不等合併，直接採用 D58 |
| Q-GIT-SERVER | 設定 repo 放哪種 git server（匯入設計 D17 事實「git server 種類未定」；ADR-0003 以 git 當 control plane） | 只影響正式部署時設定怎麼發布（review 即授權、CD 送設定），不擋 M1；正式部署前決定。Lead 同意列為待決（「OK」，2026-09-28） |
