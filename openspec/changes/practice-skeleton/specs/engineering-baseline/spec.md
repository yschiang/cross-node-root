## ADDED Requirements

### Requirement: EB-01 乾淨 clone 可建置與測試

程式 repo `cross-node-file-transfer` SHALL 可以在乾淨的 clone 上，以 Java 21 執行 `mvn -B verify` 完成建置並執行全部測試。除了 Maven 從套件庫下載依賴，不依賴開發者本機預先存在的檔案或設定。Maven 專案 SHALL 只有 parent pom 與 core 模組；之後的 Feature 需要新模組時，以 MODIFIED 修改本需求。

#### Scenario: AC-EB-01 乾淨環境建置通過

- **WHEN** 在沒有本機 Maven 套件快取的環境 clone 程式 repo，並以 Java 21 執行 `mvn -B verify`
- **THEN** 建置成功，每個模組的測試都被執行且通過

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

程式 repo SHALL 是 public，讓 GitHub 可以強制 branch protection。程式 repo 的每個 PR SHALL 在 CI 上執行必要 checks，並只以 PR 目前 head 的結果判定。必要 checks SHALL 至少涵蓋 EB-01 的建置與測試：CI 對 PR head 執行 `mvn -B verify`，建置或測試失敗時必要 check 回報失敗。必要 check 的名稱 SHALL 記在程式 repo，並設為 `main` 的 branch protection 必要 status checks；只有在每個必要 check 都實際執行建置與測試並成功時，PR 才能 merge 進 `main`；必要 check 失敗、被取消、逾時、尚未完成、被略過（skipped）或回報 neutral 時都不能 merge，repo 管理者也不能略過。

#### Scenario: AC-EB-05 程式 repo 是 public

- **WHEN** 查詢程式 repo 在 GitHub 上的可見度
- **THEN** 可見度是 public

#### Scenario: AC-EB-06 新 commit 重跑必要 checks

- **WHEN** PR 建立，或推上新 commit
- **THEN** CI 對 PR 目前的 head 執行全部必要 checks，舊 head 的結果不算數

#### Scenario: AC-EB-07 必要 check 沒有成功時不能 merge

- **WHEN** 任一必要 check 失敗、被取消、逾時或尚未完成，由 repo 管理者嘗試 merge 該 PR
- **THEN** GitHub 拒絕 merge

#### Scenario: AC-EB-11 必要 check 被略過或 neutral 時不能 merge

- **WHEN** 建置與測試沒有實際執行，必要 check 回報 skipped 或 neutral，由 repo 管理者嘗試 merge 該 PR
- **THEN** GitHub 拒絕 merge

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
