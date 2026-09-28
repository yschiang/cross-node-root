# 專案決策

本專案的決策紀錄。ID 用 `PD-`，避免和匯入的設計決策（`docs/design/design-decisions.md` 的 D1–D57）混淆。ID 用過不改、不刪；被取代的決策標明由哪一條取代。

本專案依 loop-engineering 的 D56 建立：Project 層先以 project-lead skill 進行，第一個真正的 feature 等 orchestrate 可用後走 feature loop。

## 現行

| ID | 決策 | 來源 |
| --- | --- | --- |
| PD-01 | gigaxfer `docs/spec.md` v0.3 拆成 11 個能力規格，放在 `openspec/specs/`，需求 ID 沿用原文。拆法與搬移結果見 [匯入紀錄](research/2026-09-28-import-from-gigaxfer.md) | Lead 回答「ok 11 個」（2026-09-28） |
| PD-02 | 以 gigaxfer main `4e9cba4` 為匯入基準。gigaxfer PR #11（設計裁定 D58）合併後，用一個 change 套用它的差異；被否決就不套 | Lead 回答「先用 main」（2026-09-28） |
| PD-03 | 這次 demo 以 M1 為完成目標，在 M1 驗收時收尾。順序為 M1 → M2；Phase 0 是 M1 的第一個切片，不是獨立的 milestone。M2 只列 feature，是否繼續等 M1 完成後再決定 | Lead 回答「是：demo 在 M1 驗收時收尾」（2026-09-28） |
| PD-04 | 技術棧沿用匯入設計（design-decisions D38、D9）：Java 21、Maven 多模組、Spring Boot；sync service 用內嵌 HTTP 伺服器、JPA 與 Actuator；DB 為 Oracle，本機與單元測試用 H2 Oracle mode，CI 用 Oracle Free container | Lead 回答「Q4 沿用」（2026-09-28） |
| PD-05 | Phase 0 只做三件事：Maven 多模組骨架、CI 的必要 checks、工程規則；由人協調完成，歷程標明「人工協調」（loop-engineering D56）。工程規則採用 gigaxfer 工作目錄中的本機 `AGENTS.md`（未進 gigaxfer 版控；sha256 `f69d669a97424657ef78c9fc9a4ebb3d123257d5886aa4a688d8ce7fdff77316`），在 Phase 0 複製進本 repo。第一個 feature 切片為 F1 | Lead 回答「Q5 ok」（2026-09-28） |
| PD-06 | Phase 0 改名為 **F0（專案骨架）**，和 F1–F7 同一套編號，避免「有 Phase 0 沒有 Phase 1」。PD-03、PD-05 中的 Phase 0 即 F0 | Lead 回答「OK 照你建議」（2026-09-28） |

## 待決

| ID | 問題 | 影響 |
| --- | --- | --- |
| Q-GIGAXFER-D58 | gigaxfer PR #11 是否合併 | 合併後要開 change 套用 D58；見 PD-02 |
