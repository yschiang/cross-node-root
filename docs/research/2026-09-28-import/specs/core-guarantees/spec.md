# core-guarantees Specification

## Purpose

整個系統對 Application 與維運者的核心承諾，以及這些承諾成立的條件。

建立共用的 Cross-Node File Synchronization Framework，使多個 Node 之間的檔案能持續、可靠地非同步同步，並在 Node、Network、Storage 或服務暫時故障後，自動且可驗證地恢復一致性。

**核心保證：在本 Node 的必要服務、Storage、容量正常，且交易所需資料已於本地可用時，其他 Node 的停機不得阻塞本地交易。故障解除後，系統自動補齊未完成的同步義務。**

### 保證成立的條件

- 至少一份可供恢復的有效資料與必要識別資訊仍然存在。
- 故障端的服務、連線與 Storage 最終恢復，權限及資料衝突等阻礙已解除。
- 負載位於已驗收範圍內，並具備足夠保留容量與恢復處理能力。
- 所有需要同步的寫入都遵循 Framework 的 Storage Access 與 Ready contract。
- Node independence 不代表 shared infrastructure 故障時所有 Node 都可保持正常。已確認的跨 Node 共用依賴僅有 Control Plane 與 AD / DNS；各 Phase 擁有獨立 NAS，Storage 不是部署範圍內的 correlated failure domain。設計若新增任何共用依賴，必須補列其故障影響範圍。

24 小時是保證驗收的停機範圍，不是資料保留期限。超過此範圍仍須持續追蹤、告警並嘗試恢復，不得靜默丟棄義務。

**最終驗收原則：任何一個 Node 在約定範圍內暫時停機，其他健康 Node 仍能完成獨立本地交易；故障解除後，系統自動且可驗證地補齊全部同步義務。**

來源：gigaxfer `docs/spec.md` v0.3 §1、§1.2、§3、§10 Maintenance Acceptance、§19 前言、§20（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: DG-01 Node Independence

任一 Node 因 Annual PM、Application shutdown、OS maintenance、Storage maintenance、Network isolation 或 Unexpected failure 不可用時，其他健康 Node 的獨立本地交易須持續符合既定 availability 與 latency SLO。

對故障 Node 的同步工作不得阻塞其他 Target 的工作，也不得耗盡正常交易所需資源。

#### Scenario: T02 Remote Node offline

- **WHEN** Remote Node offline
- **THEN** 健康本地獨立交易符合 SLO

#### Scenario: T03 Annual PM

- **WHEN** Annual PM
- **THEN** 其他健康 Node 的本地交易與非故障路徑同步符合 SLO

#### Scenario: T12 Target storage unavailable

- **WHEN** Target storage unavailable
- **THEN** 不阻塞其他 Target 與健康本地獨立交易

#### Scenario: AC-NODE-01

- **THEN** B shutdown 後，健康 A / C 的獨立本地交易符合 SLO

#### Scenario: AC-NODE-02

- **THEN** A / C 不必連線 B 才能完成本地交易

#### Scenario: T04 Network partition

- **WHEN** Network partition
- **THEN** 本地交易繼續，義務與恢復資料保留

### Requirement: DG-02 Local-First Availability

Application 完成本地交易不得等待 Remote Node、Remote replication 或 Control Plane 成功。

本地 Storage 或可恢復接受條件未達成時，不得宣告寫入成功。非同步複製不免除本地持久化責任。

#### Scenario: T02 Remote Node offline

- **WHEN** Remote Node offline
- **THEN** 健康本地獨立交易符合 SLO

#### Scenario: T14 Control Plane down

- **WHEN** Control Plane down
- **THEN** 既有 Data Plane 工作及本地查詢繼續

#### Scenario: AC-NODE-02

- **THEN** A / C 不必連線 B 才能完成本地交易

### Requirement: DG-03 Eventual Consistency

故障期間保留同步義務與恢復所需資料。故障解除後自動 catch up，並在約定負載及期限內完成，不應要求人工重新搬運資料。

無法由一般 retry 解決的問題須被明確識別；問題解除後可透過受控操作恢復。

#### Scenario: T05 Network recovery

- **WHEN** Network recovery
- **THEN** 自動 catch up 並重新驗證

#### Scenario: T24 持續新流量 + backlog recovery

- **WHEN** 持續新流量 + backlog recovery
- **THEN** 在約定期限完成故障 backlog，正常交易符合 SLO

#### Scenario: AC-NODE-04

- **THEN** B 恢復後自動 catch up，對 C 的同步持續進行

### Requirement: DG-04 No Silent Data Loss

Framework 必須能在定義的檢查範圍及時限內識別 missing file、partial file、corruption、failed/stuck replication、lost trigger、identity conflict 與 Source / Target mismatch。

不得把未驗證或無法確認的狀態標為 COMPLETED／Healthy；無法恢復的損失必須告警並保留證據。

#### Scenario: T10 Integrity mismatch

- **WHEN** Integrity mismatch
- **THEN** 不得標記完成；保存證據並處理

#### Scenario: T11 Lost trigger

- **WHEN** Lost trigger
- **THEN** Reconciliation 發現並補齊，包括完全未建立的 task

#### Scenario: T30 已完成 Target 檔案其後遺失或損壞

- **WHEN** 已完成 Target 檔案其後遺失或損壞
- **THEN** 在定義檢查範圍內被發現；有效來源仍在時可修復

#### Scenario: AC-NODE-05

- **THEN** 對照應有資料集合證明全部必要副本完整；不能僅以 queue 清空證明

#### Scenario: AC-NODE-03

- **THEN** B 停機期間的全部義務與可恢復資料被保留

### Requirement: DG-05 Operational Resilience

須可從 Process / Host restart、Service upgrade、Network partition、暫時 Storage / Remote Node / Control Plane outage、Duplicate trigger 與 Interrupted transfer 自動恢復。

#### Scenario: T06 Replication process crash

- **WHEN** Replication process crash
- **THEN** Restart 後 unfinished work 恢復

#### Scenario: T07 Host restart

- **WHEN** Host restart
- **THEN** 接受的義務與必要狀態不遺失

#### Scenario: T09 Duplicate trigger

- **WHEN** Duplicate trigger
- **THEN** 同義務重複執行不造成額外正式資料或 corruption

#### Scenario: T26 Config activation failure / crash

- **WHEN** Config activation failure / crash
- **THEN** 保留或恢復完整有效版本，不遺失義務

#### Scenario: T32 Service upgrade

- **WHEN** Service upgrade
- **THEN** 有效設定與未完成義務保留，恢復執行

### Requirement: DG-06 End-to-End Critical Acceptance

測試須在約定 workload、容量與實際 NFSv3 條件下執行，保留應有資料清單、故障注入時間、狀態轉移、指標及完整性證據。

| ID | Scenario | Acceptance |
| --- | --- | --- |
| T01 | Normal replication | 全部 Required targets 最終取得完整、可讀資料 |
| T02 | Remote Node offline | 健康本地獨立交易符合 SLO |
| T03 | Annual PM | 其他健康 Node 的本地交易與非故障路徑同步符合 SLO |
| T04 | Network partition | 本地交易繼續，義務與恢復資料保留 |
| T05 | Network recovery | 自動 catch up 並重新驗證 |
| T06 | Replication process crash | Restart 後 unfinished work 恢復 |
| T07 | Host restart | 接受的義務與必要狀態不遺失 |
| T08 | Interrupted transfer | Partial file 不正式可見，恢復後完整發布 |
| T09 | Duplicate trigger | 同義務重複執行不造成額外正式資料或 corruption |
| T10 | Integrity mismatch | 不得標記完成；保存證據並處理 |
| T11 | Lost trigger | Reconciliation 發現並補齊，包括完全未建立的 task |
| T12 | Target storage unavailable | 不阻塞其他 Target 與健康本地獨立交易 |
| T13 | NFS endpoint/storage failover | 不誤報成功；未知結果可追蹤、恢復後可查證；無靜默內容破壞 |
| T14 | Control Plane down | 既有 Data Plane 工作及本地查詢繼續 |
| T15 | Invalid config | Active config 不受影響 |
| T16 | Large backlog recovery | Controlled drain，無 recovery storm，正常交易符合 SLO |
| T17 | Persistent bad task | Quarantine 可見並計入未完成量與 age |
| T18 | Source Ready 後、task 建立前 crash | 自動重建全部 Required targets 的義務 |
| T19 | Target publish 後、完成紀錄保存前 crash | 查證後正確收斂，不重複發布或破壞內容 |
| T20 | 同 identity、不同內容 | 偵測衝突，不靜默覆寫 |
| T21 | 24 小時停機與 retention/容量門檻 | 必要資料不被清除；門檻告警；容量耗盡明確拒絕新寫入 |
| T22 | 嘗試變更固定 topology/targets | 設定被拒絕，既有設定與義務保留 |
| T23 | CP down + Data Plane restart | 已初始化 Node 從本地設定與狀態恢復 |
| T24 | 持續新流量 + backlog recovery | 在約定期限完成故障 backlog，正常交易符合 SLO |
| T25 | NFS 長時間無回應／結果不明 | 不誤報成功、不耗盡無關資源，恢復後結果可查證 |
| T26 | Config activation failure / crash | 保留或恢復完整有效版本，不遺失義務 |
| T27 | Reconciliation 期間 Source / Target 不可讀 | 呈現 unknown 與檢查缺口，不假報一致 |
| T28 | Target consumer 提前讀取 | 已知尚未到齊者回報資料未就緒；不出現 partial data |
| T29 | Source Ready 接受流程中 crash／回覆遺失 | 可查證是否已接受；重試不形成重複資料或漏同步 |
| T30 | 已完成 Target 檔案其後遺失或損壞 | 在定義檢查範圍內被發現；有效來源仍在時可修復 |
| T31 | Pause / resume toward one Target | 暫停期間義務保留，其他 Target 正常；resume 後受控追完 |
| T32 | Service upgrade | 有效設定與未完成義務保留，恢復執行 |

持續有新流量時，不要求任意瞬間所有 queue 都為零；驗收以截止點前的集合完整，以及新流量符合正常 SLO 判定。

測試須可重複通過並保留證據；測試次數與故障注入時點列入正式測試計畫。

#### Scenario: E2E-01 End-to-End Critical Acceptance Scenario

**Given**

- A / B / C 為同一部署範圍內的三個 Phase（Node），各自獨立 NAS，健康，初始固定 Policy 已設定。
- Workload、容量、lag、local transaction 及 recovery SLO 已填妥。
- 使用已知 File identities、size、integrity baseline 建立驗收依據。

**When**

1. 將 B 完整離線 24 小時。
2. A 持續以約定負載產生並成功接受新檔案，本地 Application 持續交易。
3. 驗證往 C 的同步持續正常，往 B 的義務與有效資料完整保留。
4. 在復原 B 前固定「停機期間已接受資料」的截止點與應有集合。
5. 恢復 B，A 繼續產生新流量。
6. 等待受控 catch-up，並執行涵蓋該截止點的 reconciliation 及完整性驗證。

**Then**

- A / C 的健康本地交易全程符合約定 SLO。
- C 的同步符合非故障路徑 SLO，未被 B 拖住。
- B 的停機期間全部義務與有效資料被保留。
- B 自動恢復並在期限內完成該截止點以前的 backlog。
- 復原期間不出現 partial data、錯誤完成或靜默覆寫。
- 應有集合內所有 File identity × Required target 均通過驗證。
- 無未解決的 missing、mismatch、unknown、blocked 或 quarantined 義務；例外不得被排除後宣稱通過。
- 不需人工 re-copy；新流量回到正常 lag SLO。
- Reconciliation 證據涵蓋驗收集合；不能僅憑 backlog counter 歸零宣告通過。
