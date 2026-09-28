# configuration Specification

## Purpose

版本化設定的發布、啟用與退回。

原 spec §4 要求的結果（見 [系統能力](../../../../project-intent.md#系統能力原-spec-4)）：Versioned desired state、本地持久化與安全啟用。

來源：gigaxfer `docs/spec.md` v0.3 §13（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: CFG-01 Configuration Flow

設定採 versioned desired state，流程為：

1. 建立設定變更並驗證。
2. 發布不可變的 Version N。
3. Node 取得設定並執行本地相容性及有效性驗證。
4. 持久化候選設定與恢復所需資訊。
5. 啟用完整版本；成功後回報 active version。
6. 啟用失敗時保留／恢復 LKG，留下失敗原因。

每個 Node 至少保存 Active Config 及可恢復的 LKG。設定啟用不得留下混合版本；啟用中 crash 後須恢復至一個完整有效版本。

可更新項目限於不改變資料同步義務的操作參數，例如 retry、rate limits 與 reconciliation schedule。不得透過設定更新靜默消除 backlog。

#### Scenario: T15 Invalid config

- **WHEN** Invalid config
- **THEN** Active config 不受影響

#### Scenario: T26 Config activation failure / crash

- **WHEN** Config activation failure / crash
- **THEN** 保留或恢復完整有效版本，不遺失義務

#### Scenario: AC-CFG-02

- **THEN** Activation failure 保留或恢復 LKG

#### Scenario: AC-CFG-03

- **THEN** CP unavailable 時既有設定持續工作，重啟亦可恢復

#### Scenario: AC-CFG-05

- **THEN** 啟用中 crash 後使用完整有效設定，不遺失既有義務

#### Scenario: AC-CFG-01

- **THEN** Invalid／不相容／超出第一版範圍的設定不影響 active config

#### Scenario: AC-CFG-04

- **THEN** 可追蹤發布者、發布時間、版本、各 Node 採用／失敗狀態
