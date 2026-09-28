## ADDED Requirements

### Requirement: EB-01 乾淨 clone 可建置與測試

程式 repo `cross-node-file-transfer` SHALL 可以在乾淨的 clone 上，以 Java 21 執行 `mvn -B verify` 完成建置並執行全部測試。除了 Maven 從套件庫下載依賴，不依賴開發者本機預先存在的檔案或設定。Maven 專案 SHALL 只有 parent pom 與 core 模組；之後的 Feature 需要新模組時，以 MODIFIED 修改本需求。

#### Scenario: AC-EB-01 乾淨環境建置通過

- **WHEN** 在沒有本機 Maven 套件快取的環境 clone 程式 repo，並以 Java 21 執行 `mvn -B verify`
- **THEN** 建置成功，每個有測試原始碼的模組，其測試都被執行且通過

#### Scenario: AC-EB-02 模組只有 parent 與 core

- **WHEN** 列出 `mvn -B verify` 建置的 Maven 模組
- **THEN** 只有 parent pom 與 core 模組

#### Scenario: AC-EB-03 測試失敗使建置失敗

- **WHEN** 任一模組有測試失敗
- **THEN** `mvn -B verify` 以非零狀態結束，失敗的測試不被忽略或略過

#### Scenario: AC-EB-04 測試沒被執行使建置失敗

- **WHEN** 有測試原始碼的模組在建置中沒有執行任何測試
- **THEN** `mvn -B verify` 以非零狀態結束，不把「沒有執行測試」當成通過

### Requirement: EB-02 PR 必要 checks 由 GitHub 強制

程式 repo SHALL 是 public，讓 GitHub 可以強制 branch protection。程式 repo 的每個 PR SHALL 在 CI 上執行必要 checks，並只以 PR 目前 head 的結果判定。必要 checks SHALL 至少包含一個建置與測試的 check：它對每個 PR 的 head 都實際執行 `mvn -B verify`，不因任何條件被略過或回報 neutral，建置或測試失敗時回報失敗。必要 check 的名稱 SHALL 記在程式 repo，並設為 `main` 的 branch protection 必要 status checks；任一必要 check 失敗、被取消、逾時或尚未完成時，PR 不能 merge 進 `main`，repo 管理者也不能略過。GitHub 把 skipped 與 neutral 視為滿足必要 check，所以建置與測試的 check 不得出現這兩種結果。

#### Scenario: AC-EB-05 程式 repo 是 public

- **WHEN** 查詢程式 repo 在 GitHub 上的可見度
- **THEN** 可見度是 public

#### Scenario: AC-EB-06 新 commit 重跑必要 checks

- **WHEN** PR 建立，或推上新 commit
- **THEN** CI 對 PR 目前的 head 執行全部必要 checks，舊 head 的結果不算數

#### Scenario: AC-EB-07 必要 check 沒有成功時不能 merge

- **WHEN** 任一必要 check 失敗、被取消、逾時或尚未完成，由 repo 管理者嘗試 merge 該 PR
- **THEN** GitHub 拒絕 merge

#### Scenario: AC-EB-11 建置與測試的 check 不被略過

- **WHEN** 任何 PR 建立或推上新 commit，包括只改文件的 PR
- **THEN** 建置與測試的 check 實際執行 `mvn -B verify`，回報成功或失敗，不回報 skipped 或 neutral

#### Scenario: AC-EB-12 建置或測試失敗使必要 check 失敗

- **WHEN** PR 的 head 有建置錯誤，或有測試失敗
- **THEN** CI 的執行紀錄顯示該 head 執行了 `mvn -B verify`，必要 check 回報失敗

#### Scenario: AC-EB-08 記錄的必要 checks 與 GitHub 設定一致

- **WHEN** 比對程式 repo 記錄的必要 check 名稱與 `main` 的 branch protection 必要 status checks
- **THEN** 兩者的名稱集合相同

### Requirement: EB-03 程式 repo 的工程規則

程式 repo SHALL 在根目錄提供工程規則 `AGENTS.md`，供在程式 repo 寫碼、審查或執行 loop 的 agent 遵守；單獨 clone 程式 repo 就讀得到，不依賴 root repo。`AGENTS.md` SHALL 以 root repo 的 `AGENTS.md` 為底稿，只在兩處不同：scope 表換成程式 repo 的 Java package，並刪去「本 repo 是 root repo」的說明。程式 repo 裡的 agent 工具指令檔（本 Feature 只有 `CLAUDE.md`）SHALL 只引用 `AGENTS.md`，不另外複製或改寫規則內容。

#### Scenario: AC-EB-09 單獨 clone 讀得到工程規則

- **WHEN** 只 clone 程式 repo，不取得 root repo
- **THEN** 根目錄有 `AGENTS.md`；repo 裡的 agent 工具指令檔只有 `CLAUDE.md`，它只引用 `AGENTS.md`，不包含另一份規則內容

#### Scenario: AC-EB-10 與 root 規則只差兩處

- **WHEN** 比對程式 repo 的 `AGENTS.md` 與 root repo `AGENTS.md`（blob `c93055be4c32`）
- **THEN** 差異只有 scope 表與 root repo 的說明兩處
