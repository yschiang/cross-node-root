# 設計文件

本目錄的設計文件與 `docs/adr/` 從 gigaxfer 原樣複製（commit `4e9cba4`），不改寫。這就是本專案沿用的高層設計：

| 文件 | 內容 |
| --- | --- |
| [網頁版](https://yschiang.github.io/cross-node-root/)（[原始檔](system-design-v2.html)） | system-design.md 的網頁版，最好先看這份；由 `.github/workflows/pages.yml` 發布到 GitHub Pages |
| [system-design.md](system-design.md) | 系統設計：設計目標與量測、元件、資料流、故障處理 |
| [design-decisions.md](design-decisions.md) | System Design 決策紀錄（D1～D57） |
| [domain-decisions.md](domain-decisions.md) | Spec v0.3 的領域決策紀錄 |
| [monitoring.md](monitoring.md) | Observability：指標與門檻 |
| [traceability.md](traceability.md) | Requirement → Design → Test 對照 |
| [ADR-0001](../adr/0001-source-owned-obligation-and-clock.md) | Replication obligation 由 Source Node 擁有，時戳以 Source Node 時鐘為準 |
| [ADR-0002](../adr/0002-target-pull-over-http.md) | 傳輸採 Target pull over HTTP，Target 端無持久狀態 |
| [ADR-0003](../adr/0003-git-as-control-plane.md) | 沒有 Control Plane process：git repo 為設定真相 |

gigaxfer 另有較舊的渲染版 `system-design.html`，沒有複製。內文提到的 `docs/spec.md` 章節，現在對應 [SA 輸入](../research/2026-09-28-import/README.md) 裡的能力，對照見 [匯入紀錄](../research/2026-09-28-import-from-gigaxfer.md)。

gigaxfer 的 PR #11（設計裁定 D58）尚未合併，這裡不含它的修改。

## 留給 System／Software Design（原 spec §21.2）

- Component、Java class / package、thread model。
- Queue、transfer protocol、database technology / schema。
- Reconciliation algorithm、integrity algorithm 與 state persistence 實作。
- NFS client、mount、HA、deployment 與 resource isolation 實作。
- UI implementation、library packaging 與 API signatures。

設計者須提交 Requirement→Design→Test 對照，說明如何封閉 Source Ready／task、Target publish／completion record 等故障窗口，並提出容量與 SLO 數值供驗收。

**最終驗收原則：任何一個 Node 在約定範圍內暫時停機，其他健康 Node 仍能完成獨立本地交易；故障解除後，系統自動且可驗證地補齊全部同步義務。**
