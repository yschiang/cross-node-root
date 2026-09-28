---
date: 2026-09-28
researcher: Project Lead Agent（Claude，依 loop-engineering 的 project-lead skill 草稿）
repository: cross-node-file-transfer（本機新 repo，尚無 commit 與 remote）
topic: 從 gigaxfer 匯入專案基準：來源版本與能力規格拆法
source_repository: gigaxfer（yschiang/cross-dc-xfer），唯讀引用
source_commit: 4e9cba4cd143cbc2e583b1fda41ba885970025c0（origin/main）
status: complete
last_updated: 2026-09-28
last_updated_note: Lead 確認 Q1、Q2 後完成搬移
---

# 從 gigaxfer 匯入專案基準

依 loop-engineering 的 D56，cross-node-file-transfer 的 Project 層先開始。這份文件是 SA 第一輪：列出要沿用的來源與版本，把 gigaxfer `docs/spec.md` 拆成能力規格。Lead 已確認拆法與版本基準，內容已搬移，結果見文末。

**後續（PD-09）**：拆出的 11 個能力後來改為 SA 輸入，從 `openspec/specs/` 搬到 [`2026-09-28-import/specs/`](2026-09-28-import/README.md)，只改相對連結、內容不變。本文以下提到的 `openspec/specs/` 是匯入當時的位置。

gigaxfer 只讀不改。舊實作的程式、測試與 review 結果不是新實作的證據。

## 來源與版本

以 gigaxfer `origin/main` `4e9cba4`（2026-09-24）為基準。blob 前 12 碼：

| 來源 | blob | 用途 |
| --- | --- | --- |
| `docs/spec.md` v0.3 | `1c1e192f2830` | 需求與驗收，拆成能力規格 |
| `CONTEXT.md` | `6e1de2c798f8` | 領域語言，原樣沿用 |
| `intent.md` | `6cdb9ca66139` | 問題與目標，併入 project intent |
| `docs/design/system-design.md` | `836f6b49721d` | 架構與技術，沿用為設計參考 |
| `docs/design/design-decisions.md` | `c846ef5577fe` | D1–D57 設計決策，沿用 |
| `docs/design/traceability.md` | `82c9c0da6879` | 需求 → 設計 → 測試對照，用來把 T01–T32 掛到需求 |
| `docs/superpowers/plans/P00-roadmap.md` | `842509535a6f` | M1、M2 與 feature 切分，作為 roadmap 起點 |
| `docs/adr/0001`–`0003` | 同 commit | 架構決策，沿用 |

**尚未合併的變更**：gigaxfer PR #11「設計裁定 D58」會改 `spec.md`、`CONTEXT.md`、`system-design.md`、`design-decisions.md` 與 `traceability.md`，見待決 Q2。

## 能力規格拆法（提案）

原則：

- 一個能力是一組會一起改變的行為。`spec.md` 的章節切法已經符合這個原則，所以大致一章一個能力，只把混在一起的部分拆開。
- **沿用原本的需求 ID**（DG、SR、FR、RR、RC、IR、RT、AC-CP、AC-CFG、AC-NODE、T01–T32），讓舊的設計決策與對照表仍能對上。原本沒有 ID 的章節才配新前綴（OPS、SLO）。
- T01–T32 依 `traceability.md` 掛到它主要驗證的需求下，當作該需求的 Scenario；同時驗證多個需求的測試只掛一處，其他需求引用它。

| 原章節 | 去處 | ID |
| --- | --- | --- |
| §1 Purpose、§1.1 第一版範圍、§4 System Scope、§21.1 範圍外 | `docs/project-intent.md`（目標、範圍、不做） | — |
| §2 Terminology | `CONTEXT.md`（原本就以它為準） | — |
| §1.2 保證成立的條件、§3 DG-01–05、§10 的 AC-NODE-01–05、§20 端到端情境 | `openspec/specs/core-guarantees/` | DG；AC-NODE、E2E 為 Scenario |
| §5 SR-01–06 | `openspec/specs/storage-access/` | SR |
| §6 FR-01–04 | `openspec/specs/file-readiness/` | FR |
| §7 RR-01–05、§14 Operational States | `openspec/specs/replication/` | RR |
| §8 RC-01–04 | `openspec/specs/reconciliation/` | RC |
| §9 IR-01–03 | `openspec/specs/integrity/` | IR |
| §10 RT-01–02 | `openspec/specs/retention-capacity/` | RT |
| §11 Control Plane、§12 AC-CP-01–03 | `openspec/specs/control-plane/` | CP |
| §13 AC-CFG-01–05 | `openspec/specs/configuration/` | CFG |
| §15 Readiness、§16 Metrics、§17 Operational Control | `openspec/specs/operations/` | OPS（新配） |
| §18 SLO | `openspec/specs/service-objectives/`；表中 TBD 列為待決，不補數字 | SLO（新配） |
| §19 T01–T32 | 依 `traceability.md` 掛到各能力的需求下 | T |
| §21.2 留給設計 | 設計文件的前言，不屬於 spec | — |

共 11 個能力規格。另外沿用 CONTEXT、project intent、設計文件與 ADR，組成 project baseline。

## 不匯入

- gigaxfer 的程式、測試、PR 與 review 結果：新 repo 要留下自己的 TDD、review 與 CI 證據。
- P01–P14 的實作計畫：它們是舊 repo 的 tasks。新 roadmap 從 P00 的 Milestone → Feature 表出發，各 feature 的 plan 由 Implementer 重新做。
- `goal.md`、`reviewer.md`、夜間 loop 指令：屬於舊流程，只作歷史參考。

## Lead 的決定

2026-09-28，Lead 在 loop-engineering 的對話中回答「ok 11 個，先用 main」：

- **Q1**：採 11 個能力。
- **Q2**：以 gigaxfer main `4e9cba4` 為基準；PR #11 的 D58 列為待套用的差異，合併後用一個 change 套進來，被否決就不套。

## 搬移結果

以 [import_specs.py](2026-09-28-import/import_specs.py) 從 `4e9cba4` 讀原文機械搬移，需求內文逐字保留，只改標題格式。

| 產出 | 內容 |
| --- | --- |
| `openspec/specs/<能力>/spec.md` ×11 | 38 條需求：原有 29 條沿用 ID，9 條是原章節沒有編號、補上新 ID |
| `docs/project-intent.md` | 原 `intent.md` 全文，加上 spec §1、§1.1、§4、§21.1 |
| `CONTEXT.md`、`docs/design/*.md`、`docs/adr/*` | 原樣複製；`docs/design/README.md` 新增，放 §21.2 與來源說明 |
| `openspec/config.yaml` | 語言設定與 loop-engineering D54 的 proposal、specs、design 規則 |

補上新 ID 的 9 條：DG-06（§20 端到端驗收，並放 §19 前言的測試共通條件）、RR-06（§14）、CP-01（§11）、CP-02（§12）、CFG-01（§13）、OPS-01～03（§15～§17）、SLO-01（§18）。

**Scenario 的掛法**：照 `traceability.md`，一個測試驗證幾條需求就掛在幾條需求下，同一個 ID 可能出現多次，代表同一個測試。以下幾處不在對照表裡，由 Project Lead Agent 判斷，Lead 可以更正：

| 項目 | 判斷 | 理由 |
| --- | --- | --- |
| T04 Network partition | 掛在 DG-01 | 對照表沒列；測試內容是故障期間其他 Node 繼續交易 |
| AC-NODE-03 | 掛在 DG-04 | 對照表沒列；內容是停機期間義務與資料不遺失 |
| AC-CFG-01、AC-CFG-04 | 也掛在 CFG-01 | 原文定義在 §13，對照表只列在 §11 |
| AC-OPS-01、AC-SLO-01 | 新增，由需求原句轉寫 | OPS-02（指標）與 SLO-01 在原文沒有任何測試；OpenSpec 要求每條需求至少一個 Scenario |

**沒有搬的原文**：spec 開頭的版本資訊，以及 §1 第三段「本文件定義……留待後續設計」的說明句。§2 名詞表以 `CONTEXT.md` 為準，所以不另外搬。

**沒有匯入的檔案**：`docs/design/system-design.html`、`system-design-v2.html` 等 HTML 呈現檔，以及 `docs/archive/`、`docs/reports/`。

## 驗證

- 腳本的機械檢查：原 29 條需求 ID 全在且不重複；T01–T32 與 13 個 AC 都有 Scenario；匯入章節的每一行非空原文都在輸出中找得到原句。
- `openspec validate --all`：11 passed、0 failed。警告有兩種：需求內文沒有英文 SHALL 或 MUST（原文用「須」「必須」，照原文不改），以及 5 條需求超過 500 字。
- 複製的設計文件內文仍提到 `docs/spec.md` 與舊 repo 路徑，連結會失效；對應關係以本文的拆法表為準。

## 下一輪

Project baseline 已具備：intent、CONTEXT、11 個能力規格、設計與 ADR。下一輪談 roadmap：以 gigaxfer P00 的 M1、M2 與 6 個 feature 為起點，決定 Phase 0 的範圍和第一個 feature。

## 語意審查

逐行比對只能證明原句都在，不能證明意思沒變。所以另外請獨立審查者比對語意：GPT-6 Astra，reasoning xhigh，經 `codex exec -s read-only` 開獨立 session。作者自審同時進行。

第 1 輪結果 `changes_requested`。以下修正都寫在腳本的 `POST_EDITS` 或產生規則裡，重新產出後機械檢查與 `openspec validate` 仍全部通過：

| ID | 問題 | 修正 |
| --- | --- | --- |
| F-01 | LKG 只在原 spec §2 定義，`CONTEXT.md` 沒有，CFG-01 卻用到 | 在 `CONTEXT.md` 補上原定義，標明取自原 spec §2 |
| F-02 | project intent 的兩個連結仍指向已不存在的 `docs/spec.md` | 改連能力規格目錄與本檔「第一版範圍」 |
| F-03 | 標題「不做」少了「第一版」，排除項看起來像永久不做 | 恢復原標題「第一版功能範圍外」 |
| F-04 | CP-02 的「上述重啟保證」原指上方的 AC-CP-02，搬成下方 Scenario 後方向錯了 | 改為「AC-CP-02 所述的重啟保證」 |
| F-05 | Purpose 的「§4 要求的結果」在新檔找不到 §4 | 改寫成「原 spec §4」並連到 project intent 的「系統能力」 |
| 自審 | 原 §19 前言的測試共通條件只留在 DG-06，其他規格的讀者看不到 | 有 T 測試的規格，在來源說明加一句指向 DG-06 |

審查者確認沒有問題的部分：T 與 AC 的掛法符合對照表，四處判斷都保留原意，WHEN／THEN 轉換沒有改變條件，由原句轉寫的兩個 Scenario 沒有新增義務，被省略的標頭狀態句與 §1 第三段都已由 SLO-01 和設計 README 承接。

第 2 輪：同一模型、新的唯讀 session，只覆核上表六項。全部 fixed，修正沒有改變任何需求的意思，也沒有新增要求，沒有新發現，`VERDICT: clean`。匯入到此完成。
