# 設計文件

本目錄的設計文件與 `docs/adr/` 從 gigaxfer 原樣複製（commit `4e9cba4`），不改寫。內文提到的 `docs/spec.md` 章節，現在對應 `openspec/specs/` 的能力規格，對照見 [匯入紀錄](../research/2026-09-28-import-from-gigaxfer.md)。

gigaxfer 的 PR #11（設計裁定 D58）尚未合併，這裡不含它的修改。

## 留給 System／Software Design（原 spec §21.2）

- Component、Java class / package、thread model。
- Queue、transfer protocol、database technology / schema。
- Reconciliation algorithm、integrity algorithm 與 state persistence 實作。
- NFS client、mount、HA、deployment 與 resource isolation 實作。
- UI implementation、library packaging 與 API signatures。

設計者須提交 Requirement→Design→Test 對照，說明如何封閉 Source Ready／task、Target publish／completion record 等故障窗口，並提出容量與 SLO 數值供驗收。

**最終驗收原則：任何一個 Node 在約定範圍內暫時停機，其他健康 Node 仍能完成獨立本地交易；故障解除後，系統自動且可驗證地補齊全部同步義務。**
