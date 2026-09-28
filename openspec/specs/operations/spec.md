# operations Specification

## Purpose

維運人員需要的查詢、指標與受控操作。

原 spec §4 要求的結果（見 [系統能力](../../../docs/project-intent.md#系統能力原-spec-4)）：可觀測、受控重試、暫停、恢復與故障查證。

來源：gigaxfer `docs/spec.md` v0.3 §15、§16、§17（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: OPS-01 Operational Readiness

Ops 必須能回答：

1. 哪些資料及哪些 Source→Target 義務尚未完成？
2. 最舊未完成義務多久，原因是什麼？
3. 哪個 Node、Storage 或同步服務異常？資訊是否過期？
4. Backlog 有多少檔案、多少 bytes？
5. 哪些工作持續失敗、blocked 或 quarantined？
6. 有哪些 integrity mismatch、衝突或無法恢復的資料？
7. 哪個 Node 正在 catch up，drain rate 與剩餘量如何？
8. 各 Node active config 是哪一版？
9. 最近一次完整檢查涵蓋什麼範圍？還有多少無法確認？
10. 剩餘容量是否足夠承受既定停機及恢復情境？

#### Scenario: AC-CP-03

- **THEN** 全域資訊中斷時仍可於健康 Node 查詢本地狀態及執行必要受控操作

### Requirement: OPS-02 Required Operational Metrics

| 類別 | 最低要求 |
| --- | --- |
| Availability | node_health、storage_health、replication_service_health、local_write_availability / latency |
| Replication | pending_count、unfinished_obligation_count、success/failure rate、retry_count、replication_lag |
| Aging | oldest_unfinished_age，自 Source Ready 起計，涵蓋 blocked / quarantined / paused |
| Integrity | integrity_failure_count、identity_conflict_count、unrecoverable_count |
| Reconciliation | missing_count、mismatch_count、unknown_count、last_complete_scan_time、coverage |
| Recovery | backlog_obligation_count、backlog_bytes、net_backlog_drain_rate、recovery_duration |
| Capacity | usable_free_bytes、protected_source_bytes、temporary_bytes、capacity_alert_status |
| Config / Freshness | active_config_version、activation_failure_count、last_status_update_time |

Oldest unfinished age 與 Replication Lag 為核心指標。若沿用 oldest_pending_age 名稱，仍須涵蓋所有未完成狀態。兩者的起點與終點時戳一律由 Source Node 時鐘打，不做跨 Node 時鐘比對（見 ADR-0001）。

指標至少可依 Source→Target 區分；正常與 recovery 時段分開呈現。完成 lag 的 P95/P99 須搭配未完成量與 age，避免只統計成功工作而掩蓋卡住資料。

Backlog bytes 按未完成 Target 義務加總，不等同 Source 實際占用容量；兩者須分開呈現。Success/failure rate 必須標示分母、時間窗與是否按 attempt 計算。

#### Scenario: AC-OPS-01（由本需求原文轉寫）

- **THEN** 指標至少可依 Source→Target 區分；正常與 recovery 時段分開呈現。

### Requirement: OPS-03 Operational Control

必須提供受控的 status inspection、failed/quarantined task inspection、retry/replay、pause/resume toward a Target、trigger reconciliation 與 active config inspection。

Pause 保留既有義務，新資料仍持續累積待同步工作；resume 後受控恢復。操作需有適當授權，並記錄操作者、時間、範圍、理由與結果。

正常維運不得要求工程師直接修改 backend DB。解除隔離或人工處理未知結果，不得跳過完整性確認直接標記完成。

#### Scenario: T31 Pause / resume toward one Target

- **WHEN** Pause / resume toward one Target
- **THEN** 暫停期間義務保留，其他 Target 正常；resume 後受控追完
