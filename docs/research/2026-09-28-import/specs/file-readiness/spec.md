# file-readiness Specification

## Purpose

檔案的權威、寫入完成與可見時點，以及 identity 衝突。

原 spec §4 要求的結果（見 [系統能力](../../../docs/project-intent.md#系統能力原-spec-4)）：可持久恢復的 Source Ready 與完整性基準。

來源：gigaxfer `docs/spec.md` v0.3 §6（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: FR-01 Single Authority & Immutable Ready File

File identity = (Source Node, Namespace, Logical key)，具有唯一 Source authority；Source Ready 後內容不再修改。不同內容必須以不同 Logical key 成為新的 File identity，不覆寫既有 Ready 內容。

第一版不提供跨 Node overwrite、append、rename、delete propagation。Replicated copy 保留原始 identity，不得被當作新的來源資料形成循環複製。

#### Scenario: T20 同 identity、不同內容

- **WHEN** 同 identity、不同內容
- **THEN** 偵測衝突，不靜默覆寫

### Requirement: FR-02 Source Ready & Acceptance Boundary

只有完成下列條件，才可向 Application 回報 Ready／finalize SUCCESS：

1. 內容已完整寫入並達到約定的本地持久化條件。
2. Identity、size 與內容完整性基準已建立，且可在故障後恢復。
3. 可恢復地辨識該檔案已被 Framework 接受，並能推導全部 Required targets。
4. 即使 replication task 尚未建立便 crash，仍可重新發現檔案並重建同步義務。

此處是 Framework 對已接受資料承擔同步責任的起點；一般 write 呼叫成功不能取代 Source Ready 的完成確認。

Writing 狀態超過 TTL（operational policy）仍未 Finalize 或 Discard 者，由 Framework 標記 Abandoned 後清理；Abandoned 不產生義務，清理須留下紀錄。

若在接受過程中 crash，恢復後必須能查證結果：已接受者續傳；未接受或未完成者不得誤報 Ready。未能確認者維持可追蹤的待確認狀態。

#### Scenario: T18 Source Ready 後、task 建立前 crash

- **WHEN** Source Ready 後、task 建立前 crash
- **THEN** 自動重建全部 Required targets 的義務

#### Scenario: T29 Source Ready 接受流程中 crash／回覆遺失

- **WHEN** Source Ready 接受流程中 crash／回覆遺失
- **THEN** 可查證是否已接受；重試不形成重複資料或漏同步

### Requirement: FR-03 Target Visibility

Target consumer 只有在 transfer、identity/size/integrity verification、持久化及 publish 全部成功後，才能看到正式資料。

Partial file 不得以正式名稱或正式讀取入口被消費；暫存檔案的清理不得誤刪正在使用或恢復所需的資料。

#### Scenario: T08 Interrupted transfer

- **WHEN** Interrupted transfer
- **THEN** Partial file 不正式可見，恢復後完整發布

#### Scenario: T28 Target consumer 提前讀取

- **WHEN** Target consumer 提前讀取
- **THEN** 已知尚未到齊者回報資料未就緒；不出現 partial data

### Requirement: FR-04 Identity Conflict

同 identity、相同內容的重複操作須安全收斂；同 identity、不同內容或正式目的位置存在衝突時，不得靜默覆寫，須隔離並留下證據。

#### Scenario: T20 同 identity、不同內容

- **WHEN** 同 identity、不同內容
- **THEN** 偵測衝突，不靜默覆寫
