# storage-access Specification

## Purpose

Application 與同步服務共用的儲存存取邊界。

原 spec §4 要求的結果（見 [系統能力](../../../docs/project-intent.md#系統能力原-spec-4)）：統一存取、完成寫入、結果查證與錯誤語意。

來源：gigaxfer `docs/spec.md` v0.3 §5（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: SR-01 Standardized Access

Application 與 synchronization service 必須遵循統一 Storage Access contract。主要 Client 環境為 Java / Spring Boot。

Contract 須明確定義下列語意；不規定 API signature：

- **write**：須宣告 Namespace、Logical key 與 Data class。Namespace 或 Data class 未於 Policy 登錄者，write 時明確拒絕。
- **Finalize**：Application 明確宣告寫入完成；回傳 SUCCESS（進入 Source Ready）、FAILURE 或 PENDING_CONFIRMATION。close() 或 rename 慣例不得取代 Finalize。
- **Discard**：Application 主動放棄 Writing 檔案；只允許對 Writing 狀態。
- **read / exists**：以完整 File identity（含 Source Node）查詢；回應語意見 SR-06。
- 可重試錯誤與結果待確認的語意見 SR-04。

Logical key 對不同內容唯一（同 lot 重測即新 key）是 Application 的義務；Framework 只負責偵測違反（FR-04）。

#### Scenario: T20 同 identity、不同內容

- **WHEN** 同 identity、不同內容
- **THEN** 偵測衝突，不靜默覆寫

#### Scenario: T29 Source Ready 接受流程中 crash／回覆遺失

- **WHEN** Source Ready 接受流程中 crash／回覆遺失
- **THEN** 可查證是否已接受；重試不形成重複資料或漏同步

### Requirement: SR-02 NFS Protocol Ownership

Application 不實作 NFS protocol stack。NFS connection、mount、protocol retransmission 與 Storage controller HA 由 infrastructure 負責。

Framework 面對 mounted filesystem semantics，負責應用可見的完成條件、故障隔離、結果查證及恢復。Infrastructure 必須提供可驗收的持久化與 HA 行為。

#### Scenario: T13 NFS endpoint/storage failover

- **WHEN** NFS endpoint/storage failover
- **THEN** 不誤報成功；未知結果可追蹤、恢復後可查證；無靜默內容破壞

### Requirement: SR-03 NFSv3 Compatibility

必須在實際 NFSv3 環境驗證 Read / Write、timeout、Storage failover、stale file handle、interrupted I/O、跨 client 的正式發布可見性，以及 endpoint/storage 恢復後的行為。

#### Scenario: T13 NFS endpoint/storage failover

- **WHEN** NFS endpoint/storage failover
- **THEN** 不誤報成功；未知結果可追蹤、恢復後可查證；無靜默內容破壞

#### Scenario: T25 NFS 長時間無回應／結果不明

- **WHEN** NFS 長時間無回應／結果不明
- **THEN** 不誤報成功、不耗盡無關資源，恢復後結果可查證

### Requirement: SR-04 Operation Outcome

| 結果 | 語意 |
| --- | --- |
| SUCCESS | 已確認達到該操作約定的完成與持久化條件 |
| FAILURE | 已確認未完成約定操作；殘留暫存資料不得對 consumer 正式可見 |
| UNKNOWN / PENDING_CONFIRMATION | 尚無法判定結果，須可追蹤並在恢復後查證 |

不得將 timeout 直接解讀為沒有副作用，也不得把未知結果當成成功。查證或重試須保留同一邏輯 operation identity。

多個 HA endpoint 必須代表相同 authoritative filesystem；不同權威 Storage 不得被當成單純 client-side failover。

#### Scenario: T13 NFS endpoint/storage failover

- **WHEN** NFS endpoint/storage failover
- **THEN** 不誤報成功；未知結果可追蹤、恢復後可查證；無靜默內容破壞

#### Scenario: T25 NFS 長時間無回應／結果不明

- **WHEN** NFS 長時間無回應／結果不明
- **THEN** 不誤報成功、不耗盡無關資源，恢復後結果可查證

#### Scenario: T29 Source Ready 接受流程中 crash／回覆遺失

- **WHEN** Source Ready 接受流程中 crash／回覆遺失
- **THEN** 可查證是否已接受；重試不形成重複資料或漏同步

### Requirement: SR-05 I/O Failure Isolation

卡住或反覆重試的 Storage I/O 不得耗盡其他正常工作的資源。Application timeout 不得被直接視為底層 I/O 已終止。

故障恢復後，仍在執行的舊操作不得破壞新操作結果或已發布內容。具體隔離與取消方式留待設計。

#### Scenario: T25 NFS 長時間無回應／結果不明

- **WHEN** NFS 長時間無回應／結果不明
- **THEN** 不誤報成功、不耗盡無關資源，恢復後結果可查證

### Requirement: SR-06 Read Availability

Consumer 透過 contract 以完整 File identity 查詢時：依 Policy 應抵達本 Node 但尚未 Target Ready 者回報 DATA_NOT_READY；依 Policy 不會抵達本 Node 者回報 NOT_EXPECTED；無法查證存在性時回報 UNAVAILABLE／UNKNOWN，不得誤報為已確認不存在。

Consumer 直接讀取 NFS 路徑亦允許，但只能得到「存在／不存在」，且「不存在」不代表「不會來」；Framework 只保證 Publish 為原子、partial 不可見。不提供跨 Source Node 以 (Namespace, Logical key) 查詢；同 key 多 Source 由 Application 在 Logical key 消歧。

本地已 Ready 的資料讀取不得依賴 Remote Node 或 Control Plane。缺少某份遠端資料不得阻塞不依賴它的其他交易。

#### Scenario: T28 Target consumer 提前讀取

- **WHEN** Target consumer 提前讀取
- **THEN** 已知尚未到齊者回報資料未就緒；不出現 partial data
