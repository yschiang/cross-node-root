# retention-capacity Specification

## Purpose

同步完成前的資料保留，以及容量不足時的告警與拒絕。

來源：gigaxfer `docs/spec.md` v0.3 §10（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: RT-01 Retention Protection

所有 Required targets 完成驗證前，須保留至少一份可供重傳的有效完整資料，以及重建同步義務所需資訊。

停機滿 24 小時、進入 QUARANTINED 或重試次數達門檻，都不是自動清除的理由。正常清理政策不得刪除仍受保護的資料。

Framework 不刪除 Source 資料，也不提供刪除 Source 資料的動詞；Source 的保存與清理由現有 NAS 管理政策負責，容量規劃（RT-02）以此為前提。本條的「正常清理」只約束 Framework 自身的清理：暫存檔、Abandoned 檔與 Target 端未 Publish 的殘留。

若外部清理刪除了義務未完成的 Source 資料，reconciliation 須報 unrecoverable 並保留證據（DG-04），不視為 Framework 缺陷。跨 Node 刪除與 Source 端刪除動詞（Retire）不在第一版範圍。

#### Scenario: T21 24 小時停機與 retention/容量門檻

- **WHEN** 24 小時停機與 retention/容量門檻
- **THEN** 必要資料不被清除；門檻告警；容量耗盡明確拒絕新寫入

### Requirement: RT-02 Capacity Management

容量評估須涵蓋 24 小時 downtime、新流量、恢復期間保留量、暫存檔案、state / metadata 與必要餘裕。

接近容量門檻時須告警；無法安全接受新寫入時，明確拒絕受影響儲存範圍的新寫入，不得回報成功後丟棄。

容量耗盡的影響範圍須明確呈現；不得透過靜默刪除未完成資料來維持表面 availability。已接受資料仍須保留義務並繼續恢復。

#### Scenario: T21 24 小時停機與 retention/容量門檻

- **WHEN** 24 小時停機與 retention/容量門檻
- **THEN** 必要資料不被清除；門檻告警；容量耗盡明確拒絕新寫入
