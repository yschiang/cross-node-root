# reconciliation Specification

## Purpose

獨立於任務紀錄，找出缺失的義務與不一致並修復。

原 spec §4 要求的結果（見 [系統能力](../../../docs/project-intent.md#系統能力原-spec-4)）：獨立發現缺失義務及資料不一致，修復後再驗證。

來源：gigaxfer `docs/spec.md` v0.3 §8（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。

## Requirements

### Requirement: RC-01 Independent Discovery

Trigger 不得成為完整性的唯一保證。Reconciliation 必須能從可恢復的 Source Ready 集合與固定 policy 推導應有義務，而非只重查既有 tasks。

#### Scenario: T11 Lost trigger

- **WHEN** Lost trigger
- **THEN** Reconciliation 發現並補齊，包括完全未建立的 task

#### Scenario: T18 Source Ready 後、task 建立前 crash

- **WHEN** Source Ready 後、task 建立前 crash
- **THEN** 自動重建全部 Required targets 的義務

### Requirement: RC-02 Coverage

至少須發現 missing target、integrity mismatch、incomplete/stuck replication、lost trigger、從未建立的 task，以及完成紀錄與實際 Target 不一致。

檢查分兩層：每輪對全部義務做 Shallow check（存在性、size、雙方 Integrity baseline 紀錄）；Deep check（重讀內容重算 digest）以滾動方式分批覆蓋，不得每輪全量重讀。Deep check 的完整覆蓋週期即 T30 的偵測時限，且須揭露為 metric。

對 Source 或 Target 無法讀取的範圍，標示無法確認並保留最後有效結果及時間，不得將檢查失敗解讀為一致或資料不存在。

#### Scenario: T11 Lost trigger

- **WHEN** Lost trigger
- **THEN** Reconciliation 發現並補齊，包括完全未建立的 task

#### Scenario: T27 Reconciliation 期間 Source / Target 不可讀

- **WHEN** Reconciliation 期間 Source / Target 不可讀
- **THEN** 呈現 unknown 與檢查缺口，不假報一致

#### Scenario: T30 已完成 Target 檔案其後遺失或損壞

- **WHEN** 已完成 Target 檔案其後遺失或損壞
- **THEN** 在定義檢查範圍內被發現；有效來源仍在時可修復

### Requirement: RC-03 Repair & Re-verify

可修復問題須自動建立或恢復同步工作，完成後重新驗證。衝突與無有效副本等問題須隔離／告警，不得無限制覆寫或無聲 retry。

#### Scenario: T10 Integrity mismatch

- **WHEN** Integrity mismatch
- **THEN** 不得標記完成；保存證據並處理

#### Scenario: T30 已完成 Target 檔案其後遺失或損壞

- **WHEN** 已完成 Target 檔案其後遺失或損壞
- **THEN** 在定義檢查範圍內被發現；有效來源仍在時可修復

### Requirement: RC-04 Inspection Evidence

須記錄每次檢查的範圍、截止點、開始／完成時間、已檢查與未確認數量、差異及修復結果。

對持續新增資料，驗收須使用明確截止點形成應有集合。Shallow check 週期、Deep check 完整覆蓋週期須於正式驗收前定義；Shallow 與 Deep 的覆蓋率分開呈現，不得宣稱涵蓋未實際檢查的資料。

#### Scenario: T27 Reconciliation 期間 Source / Target 不可讀

- **WHEN** Reconciliation 期間 Source / Target 不可讀
- **THEN** 呈現 unknown 與檢查缺口，不假報一致

#### Scenario: AC-NODE-05

- **THEN** 對照應有資料集合證明全部必要副本完整；不能僅以 queue 清空證明
