# control-plane Specification

## Purpose

跨 Node 共用的管理面，以及 Data Plane 不依賴它即時運作。

來源：gigaxfer `docs/spec.md` v0.3 §11、§12（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: CP-01 Control Plane Requirements

Control Plane 管理初始固定 topology / target policy、可調整的 operational policy、設定版本及整體可視性。

**第一版不提供運行期間新增、移除 Node 或變更 Required targets 的能力。** 涉及此類變更的設定須被拒絕，不得順帶取消或新增既有同步義務。

Control Plane 不得成為既有 Data Plane 工作的即時必要依賴；全域視圖須顯示各 Node 的狀態更新時間及未知／過期狀態。

#### Scenario: T15 Invalid config

- **WHEN** Invalid config
- **THEN** Active config 不受影響

#### Scenario: T22 嘗試變更固定 topology/targets

- **WHEN** 嘗試變更固定 topology/targets
- **THEN** 設定被拒絕，既有設定與義務保留

#### Scenario: AC-CFG-01

- **THEN** Invalid／不相容／超出第一版範圍的設定不影響 active config

#### Scenario: AC-CFG-04

- **THEN** 可追蹤發布者、發布時間、版本、各 Node 採用／失敗狀態

### Requirement: CP-02 Data Plane Independence

每個 Node 必須具備足夠的持久化 local state，包含有效設定、固定同步義務判斷所需資訊及恢復中的工作狀態。

CP outage 期間允許不能發布新設定。新 Node 的首次初始化不屬於 AC-CP-02 所述的重啟保證。

#### Scenario: T14 Control Plane down

- **WHEN** Control Plane down
- **THEN** 既有 Data Plane 工作及本地查詢繼續

#### Scenario: T23 CP down + Data Plane restart

- **WHEN** CP down + Data Plane restart
- **THEN** 已初始化 Node 從本地設定與狀態恢復

#### Scenario: AC-CP-01

- **THEN** CP shutdown 後，既有 replication、retry、reconciliation 與獨立本地交易繼續

#### Scenario: AC-CP-02

- **THEN** CP 不可用時，既有已初始化 Node 的 Data Plane 重啟後，仍可從本地設定與狀態恢復

#### Scenario: AC-CP-03

- **THEN** 全域資訊中斷時仍可於健康 Node 查詢本地狀態及執行必要受控操作
