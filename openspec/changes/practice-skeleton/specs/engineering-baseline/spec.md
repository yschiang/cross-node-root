## ADDED Requirements

### Requirement: EB-01 乾淨 clone 可建置與測試

程式 repo `cross-node-file-transfer` SHALL 可以在乾淨的 clone 上，以 Java 21 執行 `mvn -B verify` 完成建置並執行全部測試。除了 Maven 從套件庫下載依賴，不依賴開發者本機預先存在的檔案或設定。

#### Scenario: AC-EB-01 乾淨環境建置通過

- **WHEN** 在沒有本機 Maven 套件快取的環境 clone 程式 repo，並以 Java 21 執行 `mvn -B verify`
- **THEN** 建置成功，每個模組的測試都被執行且通過

#### Scenario: AC-EB-02 測試失敗使建置失敗

- **WHEN** 任一模組有測試失敗
- **THEN** `mvn -B verify` 以非零狀態結束，失敗的測試不被忽略或略過

#### Scenario: AC-EB-03 測試沒被執行使建置失敗

- **WHEN** 有測試原始碼的模組在建置中沒有執行任何測試
- **THEN** `mvn -B verify` 以非零狀態結束，不把「沒有執行測試」當成通過

### Requirement: EB-02 PR 必要 checks 由 GitHub 強制

程式 repo 的每個 PR SHALL 在 CI 上執行必要 checks，並只以 PR 目前 head 的結果判定。必要 checks SHALL 至少涵蓋 EB-01 的建置與測試。必要 check 的名稱 SHALL 記在程式 repo，並設為 `main` 的 branch protection 必要 status checks；任一必要 check 沒有成功時，PR 不能 merge 進 `main`，repo 管理者也不能略過。

#### Scenario: AC-EB-04 新 commit 重跑必要 checks

- **WHEN** PR 建立，或推上新 commit
- **THEN** CI 對 PR 目前的 head 執行全部必要 checks，舊 head 的結果不算數

#### Scenario: AC-EB-05 必要 check 沒有成功時不能 merge

- **WHEN** 任一必要 check 失敗、被取消、逾時或尚未完成，由 repo 管理者嘗試 merge 該 PR
- **THEN** GitHub 拒絕 merge

#### Scenario: AC-EB-06 記錄的必要 checks 與 GitHub 設定一致

- **WHEN** 比對程式 repo 記錄的必要 check 名稱與 `main` 的 branch protection 必要 status checks
- **THEN** 兩者的名稱集合相同，且包含 EB-01 的建置與測試

### Requirement: EB-03 程式 repo 的工程規則

在程式 repo 寫碼、審查或執行 loop 的 agent SHALL 遵守程式 repo 根目錄的 `AGENTS.md`；單獨 clone 程式 repo 就讀得到，不依賴 root repo。`AGENTS.md` SHALL 以 root repo 的 `AGENTS.md` 為底稿，只在兩處不同：scope 表換成程式 repo 的 Java package，並刪去「本 repo 是 root repo」的說明。各 agent 工具的指令檔只引用 `AGENTS.md`，不另外複製或改寫規則內容。

#### Scenario: AC-EB-07 單獨 clone 讀得到工程規則

- **WHEN** 只 clone 程式 repo，不取得 root repo
- **THEN** 根目錄有 `AGENTS.md`，`CLAUDE.md` 只引用它，不包含另一份規則內容

#### Scenario: AC-EB-08 與 root 規則只差兩處

- **WHEN** 比對程式 repo 的 `AGENTS.md` 與 root repo `AGENTS.md`（blob `c93055be4c32`）
- **THEN** 差異只有 scope 表與 root repo 的說明兩處
