# project-lead skill 演練紀錄

本專案的 Project 層是 loop-engineering `project-lead` skill 草稿的第一次實際演練（loop-engineering D56）。這裡記錄演練中發現的 skill 缺口，Project 層結束後一起修回 skill。

| # | 日期 | 發現 | 證據 | 建議修正 |
| --- | --- | --- | --- | --- |
| 1 | 2026-09-28 | Skill 沒有說明 roadmap 該切多細、何時重切。Agent 先照 P00 把 M1 全部切開，被問到時又直接改成「只切近期」，兩次都沒有依據 | Lead 問「roadmap 是持續演化的文件，何時該切到多細？M1 也不見得不能先切細」；loop-engineering 交接契約只有「近期較細、遠期可粗」一句 | 已處理：SA 指引新增「Roadmap 怎麼規劃」，skill 新增第 4a 步，另收錄[業界做法參考](https://github.com/yschiang/loop-engineering/blob/main/docs/references/roadmap-planning.md)；待 docs PR 合併 |
| 2 | 2026-09-28 | 逐行比對只證明原句都在，不能證明搬移後意思沒變；匯入時有 6 處因為失去上下文而走樣 | [匯入紀錄](2026-09-28-import-from-gigaxfer.md)的「語意審查」 | 在 skill 第 1 步的匯入說明加上：搬移後要做語意比對，特別檢查「上述」「本表」「§N」這類依賴上下文的指代、被拆開的表格與標題，以及只在原文件定義的名詞 |
