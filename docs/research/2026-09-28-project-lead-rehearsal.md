# project-lead skill 演練紀錄

本專案的 Project 層是 loop-engineering `project-lead` skill 草稿的第一次實際演練（loop-engineering D56）。這裡記錄演練中發現的 skill 缺口，Project 層結束後一起修回 skill。

| # | 日期 | 發現 | 證據 | 建議修正 |
| --- | --- | --- | --- | --- |
| 1 | 2026-09-28 | Skill 沒有說明 roadmap 該切多細、何時重切。Agent 先照 P00 把 M1 全部切開，被問到時又直接改成「只切近期」，兩次都沒有依據 | Lead 問「roadmap 是持續演化的文件，何時該切到多細？M1 也不見得不能先切細」；loop-engineering 交接契約只有「近期較細、遠期可粗」一句 | 已處理：SA 指引新增「Roadmap 怎麼規劃」，skill 新增第 4a 步，另收錄[業界做法參考](https://github.com/yschiang/loop-engineering/blob/main/docs/references/roadmap-planning.md)；待 docs PR 合併 |
| 2 | 2026-09-28 | 逐行比對只證明原句都在，不能證明搬移後意思沒變；匯入時有 6 處因為失去上下文而走樣 | [匯入紀錄](2026-09-28-import-from-gigaxfer.md)的「語意審查」 | 在 skill 第 1 步的匯入說明加上：搬移後要做語意比對，特別檢查「上述」「本表」「§N」這類依賴上下文的指代、被拆開的表格與標題，以及只在原文件定義的名詞 |
| 3 | 2026-09-28 | D54 與 skill 假設每個 Feature 都有產品行為，但專案骨架這類工程 Feature 沒有；OpenSpec 1.13.1 規定 change 至少要有一個 spec delta，否則驗證失敗 | 在暫存目錄建立只有 proposal 的 change，`openspec validate` 回報「Ensure change has deltas in specs/」 | 已處理：採 `engineering-baseline` 能力（PD-07）；loop-engineering D57 的 Feature 定義涵蓋可單獨驗收的工程條件（PR #4） |
| 4 | 2026-09-28 | Skill 第 6 步只說「建立 ticket」，沒有 ticket 內容與「可以開工」的門檻；Agent 臨時決定欄位開了兩張 | Lead 問「開 ticket 要用什麼 skill，內容有沒有規範」 | 已處理：loop-engineering D57 定下 ticket 只寫目標、milestone、change 連結與驗收 ID、Blocked by、狀態，change 寫好且通過驗證為就緒；寫進 skill 第 6 步（PR #4）。#1、#2 待照此正規化 |
| 5 | 2026-09-28 | Skill 與 D54 沒有定義工作層級。Agent 先提出四層（Feature 之下再由工程師拆 PBI），和 OpenSpec、Superpowers「一份 spec 拆成 tasks、一個 PR」的原生做法不合 | Lead 表示「就三層吧，認知四層有點多了，而且和原生工具不合」 | 已處理：三層（PD-08、loop-engineering D57）；roadmap 改回 PR 大小的 Feature |
| 6 | 2026-09-28 | 匯入時把還沒實作的 38 條需求放進 `openspec/specs/`，但 OpenSpec 定義那裡是「系統目前的行為」；Agent 會以為需求已經做好，第一個 Feature 的 delta 也沒有東西可以 ADDED | Lead 追問「還未實現的需求/plan 現在的流程放在哪」；OpenSpec [concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)："Specs ... describe how your system currently behaves" | 已處理：需求依狀態放置（PD-09、loop-engineering D58），11 個能力搬到 SA 輸入 |
| 7 | 2026-09-28 | SA 確認與開工確認在 Lead 兼任工程師時變成同一人確認兩次 | Lead 說明「未來 PM 和工程師會逐漸融合」 | 已處理：同一人兼任時合併成一次（loop-engineering D59） |
| 8 | 2026-09-28 | Skill 與流程只假設一個 repo，沒有多個服務 repo 時 spec 放哪、PR 怎麼算、交接包要記哪些版本的規則 | Lead 問「如果現在是 multiple microservice repos」 | 已處理：loop-engineering D61（root repo 加 `repos.yaml`）；示範專案改成 `cross-node-root` 加程式 repo（PD-10） |
