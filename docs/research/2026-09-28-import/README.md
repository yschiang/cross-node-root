# SA 輸入：從 gigaxfer 匯入的需求

**這裡是輸入，不是規格。** 內容描述系統要做到什麼，還沒有任何一條已經實作。

- `specs/<能力>/spec.md`：gigaxfer `docs/spec.md` v0.3（commit `4e9cba4`）依能力拆成 11 份，共 38 條需求，需求 ID 沿用原文。拆法與搬移的檢查見[匯入紀錄](../2026-09-28-import-from-gigaxfer.md)。
- `import_specs.py`：當時的一次性匯入腳本，只保留作紀錄，不要重跑。它會把檔案寫回 `openspec/specs/`，而那裡依 PD-09 只放已實作的行為。

**來歷：這是別人已經做完的 SA 成果，不是本專案的 SA 產出。** gigaxfer 的 `docs/spec.md` v0.3（2026-09-21，狀態 Design baseline）是需求提出者的說明與一段方案討論反覆修訂的結果，domain model 已由 CONTEXT、domain-decisions 與 ADR 釘死；它在進 gigaxfer 版控前就已完成（見 [project intent](../../project-intent.md) 的需求來源）。本專案的 Project Lead 只做拆分與核對，沒有重做 SA，所以 38 條需求可以一次匯入。沒有上游 spec 的專案不會這樣：Project SA 只寫目標、範圍、共用限制與 roadmap，每個 Feature 的需求在 Feature SA 時才經研究與問答寫出來。

**怎麼使用**（PD-09，依 loop-engineering D58）：

1. Roadmap 的每個 Feature 在「相關需求輸入」欄指向這裡的能力。
2. Feature 排進近期時開 change，Feature SA 從這裡挑出這次要做的需求，寫進 change 的 spec delta：`openspec/specs/` 還沒有的用 ADDED，已經有的用 MODIFIED。需求可以只帶入這次要做的部分，其餘留給之後的 Feature。
3. Feature 驗收並 merge 之後 archive，這些需求才進入 `openspec/specs/`，代表系統已經做得到。

跨 Feature 的共用限制（`core-guarantees`、`service-objectives`）列在 [project intent](../../project-intent.md#跨-feature-的共用限制)，每次 Feature SA 都要檢查。

這份輸入的內容只在 gigaxfer 基準改變時更新（例如 PD-02 的 gigaxfer D58）；Feature 帶入 change 時的細化寫在 change 裡，不回頭改這裡。
