# cross-node-root

產品 cross-node-file-transfer（跨 Node 的交易檔案同步框架）的 root repo。這是 [Loop Engineering](https://github.com/yschiang/loop-engineering) 的示範專案：從 Project 層的規劃，到多個 feature 的交付，都保留文件、決策、worktree、PR 與 gate 的歷程。

依 loop-engineering D61，規劃放在這個 root repo，程式放在服務 repo：

```text
cross-node-root/                 ← 本 repo：規劃、spec、決策、共用規則、ticket
├── repos.yaml                   ← 服務 repo 清單
├── scripts/sync-repos           ← 依清單 clone 或更新服務 repo
└── repos/                       ← 服務 repo（不進本 repo 的版控）
    └── cross-node-file-transfer/  ← 程式：core library 與 sync service
```

Feature 的 ticket 開在本 repo；一個 Feature 動到哪些 repo，就在每個 repo 各開一個 PR，都連到同一張 ticket。

## 怎麼開始

1. **取得 root**：`git clone https://github.com/yschiang/cross-node-root.git`
2. **拉服務 repo**：`scripts/sync-repos`。缺的 clone，乾淨的更新，有未提交修改的不動。
3. **安裝 skills**：在 [loop-engineering](https://github.com/yschiang/loop-engineering) 執行 `./setup.sh`，它會把 `project-lead`、`research-codebase`、Matt Pocock 與 Superpowers 的 skills 裝好，並檢查 OpenSpec CLI 的版本。再在本 repo 執行 `scripts/check-skills` 確認沒有缺。`orchestrate` 還在 loop-engineering 實作中，可用前由人協調。
4. **照流程工作**：讀 loop-engineering 的[使用指南](https://github.com/yschiang/loop-engineering/blob/main/docs/guide/user-guide.md)，每一步的細節查[參考手冊](https://github.com/yschiang/loop-engineering/blob/main/docs/guide/reference.md)。
5. **看現在做到哪**：[Roadmap](docs/roadmap.md) 與下方的目前狀態。

需求與設計匯入自 gigaxfer（commit `4e9cba4`），本專案重新實作。

| 要了解什麼 | 入口 |
| --- | --- |
| 為什麼做、做到哪裡為止 | [Project intent](docs/project-intent.md) |
| 還沒實作的需求 | [SA 輸入](docs/research/2026-09-28-import/README.md) |
| 已實作的行為 | [`openspec/specs/`](openspec/specs/)（第一個 Feature archive 後才有內容） |
| 進行中的 Feature | [`openspec/changes/`](openspec/changes/) |
| 共用詞彙 | [CONTEXT](CONTEXT.md) |
| 設計 | [設計文件](docs/design/README.md) · [ADR](docs/adr/) |
| 交付順序 | [Roadmap](docs/roadmap.md) |
| 決策 | [專案決策](docs/decisions.md) |
| 服務 repo | [`repos.yaml`](repos.yaml) · [`scripts/`](scripts/) |
| 匯入與演練紀錄 | [匯入紀錄](docs/research/2026-09-28-import-from-gigaxfer.md) · [project-lead 演練](docs/research/2026-09-28-project-lead-rehearsal.md) |

目前狀態：Project 層待 Project Lead 確認設計方案與 roadmap；下一個是 Feature [#1 專案骨架](https://github.com/yschiang/cross-node-root/issues/1)。
