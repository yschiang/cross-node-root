# Roadmap

來源：gigaxfer `docs/superpowers/plans/P00-roadmap.md`（commit `4e9cba4`，blob `842509535a6f`）。本專案重新實作，gigaxfer 的 PR、程式與測試結果都不沿用為證據。

**原則**：依 loop-engineering 的 [roadmap 規則](https://github.com/yschiang/loop-engineering/blob/main/docs/workflow/project-lead-sa.md#roadmap-怎麼規劃)，切片清單可以提早列，spec 只寫接下來 1–2 片。M1 的切法來自 gigaxfer 已實作過的計畫，所以整個列出；M2 只列 feature。每個切片驗收後回頭調整。

## Milestones

依序是 M1、M2；M1 從 F0（專案骨架，原稱 Phase 0）開始。這次 demo 以 M1 為完成目標，在 M1 驗收時收尾（PD-03）。M1、M2 的交付成果與驗收條件原樣取自 P00。

| Milestone | 交付成果 | 驗收條件 | 包含的 features |
| --- | --- | --- | --- |
| **M1：跨 Node 檔案讀取** | App 發布後，交易能在指定 Node 讀到正確副本。 | 發布 → ingest → Target 下載、驗證與持久化 → Consumer 讀取的端到端路徑通過；完成 P13 對應 NAS 驗收與 P14 基本交付測試。 | 可靠發布來源檔案；拉取並保存指定副本；App 透過 library 讀寫檔案。共用支援：sync-service 骨架、清道夫 |
| **M2：故障恢復與事故追蹤** | 約定故障後，副本恢復可讀，事故與恢復結果可查。 | LOST／CORRUPT、重送、重啟及支援的 DB 還原情境通過；invalid 讀取保護、事故告警與操作稽核正確。恢復限制依 F24b／D56；完成 P13／P14 對應故障與容量驗收。 | 副本自動修復；重建與還原後恢復同步；事故告警與追蹤 |

各 feature 在 gigaxfer 對應哪些子計畫，見 P00 的對照表，切片時再參考。

## M1 的切片

「近期」接下來就寫 spec；「暫定」只有名稱、範圍與依賴，到了再寫 spec，也可能重切。

| 切片 | 狀態 | 內容 | gigaxfer 對應 | 依賴 | 主要能力規格 | 走法 |
| --- | --- | --- | --- | --- | --- | --- |
| F0 | 近期 | 專案骨架：Maven 多模組、CI 必要 checks、工程規則 | P00 建置假設 | — | — | 人工協調（loop-engineering D56） |
| F1 | 近期 | 可靠發布：core 的 Finalize 協議 | P01 | F0 | storage-access、file-readiness、integrity | 等 orchestrate 可用後走 feature loop |
| F2 | 暫定 | sync-service 骨架：啟動、設定、schema、認證、health | P02 | F1 | configuration、control-plane、operations | feature loop |
| F3 | 暫定 | 掃描 ingest：建立同步義務 | P03 | F2 | replication、reconciliation | feature loop |
| F4 | 暫定 | Source 端點 | P04 | F3 | replication | feature loop |
| F5 | 暫定 | Target puller：下載、驗證、發布 | P05 | F4 | replication、integrity、file-readiness | feature loop |
| F6 | 暫定 | App 透過 library 讀寫檔案 | P10 | F1、F2 | storage-access、file-readiness | 可和 F3 平行 |
| F7 | 暫定 | 清道夫：暫存與保留規則 | P09 | F3 | retention-capacity | feature loop |
| M1 驗收 | 暫定 | P13、P14 的 M1 子集 | P13、P14 | F1–F7 | core-guarantees | 跨切片整合驗證 |

F6 和 F3 可以在不同 worktree 平行進行；F3 → F4 → F5 是天然的依賴鏈，若 Q-STACK 核准，可以做成 stacked PR 展示。現行規則下它們依序開工（loop-engineering D27）。

## 決定

已決定：完成目標與順序（PD-03）、技術棧（PD-04）、F0 的範圍與第一個 feature 切片（PD-05）、F0 的名稱（PD-06）。
