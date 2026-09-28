# Roadmap

來源：gigaxfer `docs/superpowers/plans/P00-roadmap.md`（commit `4e9cba4`，blob `842509535a6f`）。本專案重新實作，gigaxfer 的 PR、程式與測試結果都不沿用為證據。

**原則**（loop-engineering D57、D58）：roadmap 只有 Milestone 與 Feature 兩層。Feature 是一個自成一體、能單獨驗收、一個 PR 做得完的變更，對應一個 OpenSpec change 與一張 ticket；task 寫在 change 的 `tasks.md`，不上 roadmap。需求原文在 [SA 輸入](research/2026-09-28-import/README.md)，roadmap 只指向它；Feature 排進近期才開 change 寫 spec。M1 的切法來自 gigaxfer 已實作過的計畫，所以整個列出；M2 要不要做等 M1 完成後決定（PD-03），先只寫交付能力。每個 Feature 驗收後回頭調整。

## Milestones

依序是 M1、M2；M1 從 Feature「專案骨架」開始。這次 demo 以 M1 為完成目標，在 M1 驗收時收尾（PD-03）。M1、M2 的交付成果與驗收條件原樣取自 P00。

| Milestone | 交付成果 | 驗收條件 | 交付能力 |
| --- | --- | --- | --- |
| **M1：跨 Node 檔案讀取** | App 發布後，交易能在指定 Node 讀到正確副本。 | 發布 → ingest → Target 下載、驗證與持久化 → Consumer 讀取的端到端路徑通過；完成 P13 對應 NAS 驗收與 P14 基本交付測試。 | 可靠發布來源檔案；拉取並保存指定副本；App 透過 library 讀寫檔案。共用支援：sync-service 骨架、清道夫 |
| **M2：故障恢復與事故追蹤** | 約定故障後，副本恢復可讀，事故與恢復結果可查。 | LOST／CORRUPT、重送、重啟及支援的 DB 還原情境通過；invalid 讀取保護、事故告警與操作稽核正確。恢復限制依 F24b／D56；完成 P13／P14 對應故障與容量驗收。 | 副本自動修復；重建與還原後恢復同步；事故告警與追蹤 |

## M1 的 Feature

「近期」接下來開 change 寫 spec；「暫定」只有名稱、範圍與依賴，到了再寫，也可能重切。「交付能力」只是分組標籤，對應上表 M1 的交付能力：每個 Feature 用自己的 AC 單獨驗收，交付能力是否完整在 M1 驗收時證明。

| Feature | 狀態 | 交付能力 | 內容 | gigaxfer 參考 | 依賴 | 相關需求輸入 | 走法 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [#1](https://github.com/yschiang/cross-node-root/issues/1) 專案骨架 | 近期，SA 草稿完成 | 共用支援 | Maven 多模組、CI 必要 checks、工程規則 | P00 建置假設 | — | 無；新增 `engineering-baseline` 能力（PD-07） | 人工協調（loop-engineering D56） |
| [#2](https://github.com/yschiang/cross-node-root/issues/2) Finalize 協議 | 近期 | 可靠發布來源檔案 | core 的寫入、finalize、discard 協議與冪等重試 | P01 | 專案骨架 | storage-access、file-readiness、integrity | 等 orchestrate 可用後走 feature loop |
| sync-service 骨架 | 暫定 | 共用支援 | 啟動、設定、schema、認證、health | P02 | Finalize 協議 | configuration、control-plane、operations | feature loop |
| 掃描 ingest | 暫定 | 可靠發布來源檔案 | 增量掃描並建立同步義務 | P03（增量掃與 ingest） | sync-service 骨架 | replication、file-readiness | feature loop |
| 對帳 | 暫定 | 可靠發布來源檔案 | 全量對帳掃：從 Source Ready 集合與 Policy 推導應有義務，補回漏掉的通知與 crash 後沒建立的義務（RC-01；T11、T18） | P03（全量對帳掃） | 掃描 ingest | reconciliation | feature loop |
| Source 端點 | 暫定 | 拉取並保存指定副本 | 提供待傳清單、檔案下載與回報 | P04 | 掃描 ingest | replication | feature loop |
| Target puller | 暫定 | 拉取並保存指定副本 | 下載、驗證、發布 | P05 | Source 端點 | replication、integrity、file-readiness | feature loop |
| library starter | 暫定 | App 透過 library 讀寫檔案 | App 透過 library 讀寫與 `/locate` | P10 | Finalize 協議、sync-service 骨架 | storage-access、file-readiness | 可和掃描 ingest 平行 |
| 清道夫 | 暫定 | 共用支援 | 暫存與保留規則 | P09 | 掃描 ingest | retention-capacity | feature loop |

**M1 驗收**：P13、P14 的 M1 子集，跨 Feature 整合驗證，依賴以上全部，主要對照 core-guarantees。Milestone 驗收怎麼控制，loop-engineering 還在討論。

對帳的其餘部分（Source 對帳與 Target 自查：找出遺失或損壞的副本，RC-02～04）要搭配修復才有用，屬 M2 的副本自動修復（P06、P07）（PD-12）。Ops 整組（OPS-01 `/status` 十題；OPS-03 的 pause／resume、release、retry、ack）屬 M2 的事故告警與追蹤（P11），Source 端點的 `/pending` 在 M1 不做 pause 過濾（PD-13）。

library starter 和掃描 ingest 可以在不同 worktree 平行；掃描 ingest → Source 端點 → Target puller 是依賴鏈，若 Q-STACK 核准，可以做成 stacked PR 展示。現行規則下依序開工（loop-engineering D27）。

Feature 不用 F 編號：匯入設計 §6 的故障窗口已經用了 F1–F33。M2 驗收條件裡的 F24b、D56，指匯入設計中的故障情境與 gigaxfer 設計決策，不是本專案的 Feature 或 loop-engineering 的決策。

## 決定

已決定：完成目標與順序（PD-03）、技術棧（PD-04）、專案骨架的範圍（PD-05）、工程類 Feature 的 spec（PD-07）、工作層級與命名（PD-08）、需求放在哪（PD-09）、root 與程式 repo 的結構（PD-10）、gigaxfer D58 直接採用（PD-11）、M1 的對帳 Feature（PD-12）、Ops 放在 M2（PD-13）。
