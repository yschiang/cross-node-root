# replication Specification

## Purpose

跨 Node 的非同步複製、同步義務與其狀態。

原 spec §4 要求的結果（見 [系統能力](../../../../project-intent.md#系統能力原-spec-4)）：依固定同步對象執行非同步傳輸及發布。

來源：gigaxfer `docs/spec.md` v0.3 §7、§14（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: RR-01 Asynchronous Replication

Replication 不屬於 Application 的 synchronous transaction。Local Ready 成功不代表任一 Target 已 Ready。

#### Scenario: T01 Normal replication

- **WHEN** Normal replication
- **THEN** 全部 Required targets 最終取得完整、可讀資料

### Requirement: RR-02 Durable Work & Obligation Recovery

已建立 task 的狀態必須持久化，Process crash、Agent / Host restart、Service upgrade 不得遺失未完成工作。

尚未建立 task 的已接受檔案，也必須可重新發現並重建全部同步義務。不得只依 task table 是否有紀錄判斷資料完整性。

Replication obligation 的權威狀態由 Source Node 擁有並持久化；Target Node 只保存 Completion evidence，供 Source 在完成紀錄遺失時查證收斂，不得成為義務的唯一保存處（見 ADR-0001）。

#### Scenario: T06 Replication process crash

- **WHEN** Replication process crash
- **THEN** Restart 後 unfinished work 恢復

#### Scenario: T07 Host restart

- **WHEN** Host restart
- **THEN** 接受的義務與必要狀態不遺失

#### Scenario: T18 Source Ready 後、task 建立前 crash

- **WHEN** Source Ready 後、task 建立前 crash
- **THEN** 自動重建全部 Required targets 的義務

### Requirement: RR-03 Idempotency

允許 at-least-once execution。Duplicate trigger、重試及重啟後執行同一義務，不得造成額外正式資料、內容破壞或錯誤狀態。

Target 已發布但完成紀錄尚未保存時 crash，恢復後須可查證並收斂；不能只因缺少完成紀錄便假設 Target 不存在。

#### Scenario: T09 Duplicate trigger

- **WHEN** Duplicate trigger
- **THEN** 同義務重複執行不造成額外正式資料或 corruption

#### Scenario: T19 Target publish 後、完成紀錄保存前 crash

- **WHEN** Target publish 後、完成紀錄保存前 crash
- **THEN** 查證後正確收斂，不重複發布或破壞內容

### Requirement: RR-04 Retry & Isolation

Temporary failure 自動 retry，須避免 tight loop、retry storm 與恢復時瞬間過載。單一 Target 的失敗不得阻塞其他 Target。

持續失敗必須呈現原因、次數、最後嘗試時間與下一步；超出一般 retry 可處理範圍時進入 BLOCKED／QUARANTINED。

#### Scenario: T12 Target storage unavailable

- **WHEN** Target storage unavailable
- **THEN** 不阻塞其他 Target 與健康本地獨立交易

#### Scenario: T17 Persistent bad task

- **WHEN** Persistent bad task
- **THEN** Quarantine 可見並計入未完成量與 age

### Requirement: RR-05 Controlled Catch-up

Backlog 須持久保存，恢復後自動 drain，並控制 recovery rate。持續有新流量時，仍須在約定負載範圍內於恢復期限完成故障期間 backlog。

Recovery、reconciliation 與正常 replication 的合計資源使用不得使正常本地交易超出已約定的 SLO。

#### Scenario: T16 Large backlog recovery

- **WHEN** Large backlog recovery
- **THEN** Controlled drain，無 recovery storm，正常交易符合 SLO

#### Scenario: T24 持續新流量 + backlog recovery

- **WHEN** 持續新流量 + backlog recovery
- **THEN** 在約定期限完成故障 backlog，正常交易符合 SLO

### Requirement: RR-06 Operational States

Replication state 至少以 File identity × Target 為粒度。

| State | Meaning |
| --- | --- |
| PENDING | 已知義務尚未開始 |
| IN_PROGRESS | 傳輸中 |
| VERIFYING | 驗證、持久化或發布結果確認中 |
| COMPLETED | 此 Target 已達到完整完成條件 |
| RETRY_WAIT | 暫時失敗，等待下一次重試 |
| BLOCKED | 已知外部條件、受控暫停或結果待確認等阻礙，須顯示原因與恢復條件 |
| QUARANTINED | 一般 retry 無法解決，例如持續完整性失敗、metadata 不合法、持續權限問題或內容衝突 |

整份檔案完成代表所有 Required targets 都已完成。BLOCKED、QUARANTINED、pause 及結果待確認均不免除同步義務，須計入 backlog 與未完成時間。

UNKNOWN / PENDING_CONFIRMATION 是 operation outcome；可映射至上述狀態，但必須明確顯示待確認原因。

#### Scenario: T17 Persistent bad task

- **WHEN** Persistent bad task
- **THEN** Quarantine 可見並計入未完成量與 age
