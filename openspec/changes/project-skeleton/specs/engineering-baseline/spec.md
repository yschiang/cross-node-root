## Purpose

開發與交付本專案必須成立的工程條件：怎麼建置與測試、PR 要通過哪些檢查、在 repo 工作的 agent 遵守哪些規則。它不是產品行為，使用者看不到，但每個 Feature 都依賴它。之後改動 CI 或工程規則的 Feature，以 MODIFIED 修改本規格（PD-07）。

## ADDED Requirements

### Requirement: EB-01 乾淨 clone 可建置與測試

本 repo SHALL 可以在乾淨的 clone 上，以 Java 21 執行 `mvn -B verify` 完成建置與全部測試。除了 Maven 從套件庫下載依賴，不依賴開發者本機預先存在的檔案或設定。

#### Scenario: AC-EB-01 乾淨環境建置

- **WHEN** 在沒有本機 Maven 快取的環境 clone 本 repo，並以 Java 21 執行 `mvn -B verify`
- **THEN** 建置成功，所有模組的測試都被執行且通過

#### Scenario: AC-EB-02 測試失敗使建置失敗

- **WHEN** 任一模組有測試失敗
- **THEN** `mvn -B verify` 以非零狀態結束，不忽略或略過失敗的測試

### Requirement: EB-02 PR 必要 checks

每個 PR SHALL 在 CI 上執行必要 checks，並只以 PR 目前 head 的結果判定。必要 checks SHALL 至少涵蓋 EB-01 的建置與測試。必要 check 的集合由 Lead 核准並記錄在 repo 中；未經核准的 check 不算必要 check。

#### Scenario: AC-EB-03 新 commit 重跑

- **WHEN** PR 建立，或推上新 commit
- **THEN** CI 對目前 head 執行全部必要 checks

#### Scenario: AC-EB-04 非成功不算通過

- **WHEN** 任一必要 check 失敗、被取消、逾時或尚未完成
- **THEN** 該 PR 的 CI 結果不算通過

### Requirement: EB-03 工程規則

在本 repo 寫碼、審查或執行 loop 的 agent SHALL 遵守根目錄的 `AGENTS.md`。`AGENTS.md` 是工程規則的唯一來源；各 agent 工具的專屬指令檔只引用它，不另外複製或改寫規則內容。

#### Scenario: AC-EB-05 各工具讀同一份規則

- **WHEN** 檢查 repo 中各 agent 工具的指令檔，例如 `CLAUDE.md`
- **THEN** 它們只引用 `AGENTS.md`，不包含另一份工程規則內容
