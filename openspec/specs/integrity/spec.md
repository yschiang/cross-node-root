# integrity Specification

## Purpose

內容完整性的基準、完成條件與持續失敗的處理。完整性同時被就緒、複製與對帳使用，所以自成一個能力。

來源：gigaxfer `docs/spec.md` v0.3 §9（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: IR-01 Verification Baseline

Source Ready 時須建立與 File identity 綁定的 size 及內容完整性基準；比對不能僅使用檔名、mtime 或 size。

完整性基準須可恢復且不可在 retry 時任意重算取代原值，以免把事後損壞接受為新基準。具體 digest、儲存方式與驗證演算法留待設計。

#### Scenario: T10 Integrity mismatch

- **WHEN** Integrity mismatch
- **THEN** 不得標記完成；保存證據並處理

#### Scenario: T20 同 identity、不同內容

- **WHEN** 同 identity、不同內容
- **THEN** 偵測衝突，不靜默覆寫

### Requirement: IR-02 Completion Conditions

每個 Target 必須依該基準完成驗證，並確認持久化及發布結果，才可標記 COMPLETED。資訊不足或操作結果待確認時不得完成。

#### Scenario: T08 Interrupted transfer

- **WHEN** Interrupted transfer
- **THEN** Partial file 不正式可見，恢復後完整發布

#### Scenario: T10 Integrity mismatch

- **WHEN** Integrity mismatch
- **THEN** 不得標記完成；保存證據並處理

### Requirement: IR-03 Persistent Integrity Failure

重複 integrity failure 須進入可識別異常狀態，保留 Source、Target、identity、expected/observed 結果與時間。無法自動修復者須告警。

後續檢查發現已完成資料遺失或損壞時，須重新呈現異常與修復義務，保留原完成紀錄及後續發現的歷史。

#### Scenario: T17 Persistent bad task

- **WHEN** Persistent bad task
- **THEN** Quarantine 可見並計入未完成量與 age

#### Scenario: T30 已完成 Target 檔案其後遺失或損壞

- **WHEN** 已完成 Target 檔案其後遺失或損壞
- **THEN** 在定義檢查範圍內被發現；有效來源仍在時可修復
