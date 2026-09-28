# Project intent：cross-node-file-transfer

來源：gigaxfer `intent.md` 與 `docs/spec.md` v0.3 §1、§1.1、§4、§21.1（commit `4e9cba4`），內容原樣搬入。需求原文在 [SA 輸入](research/2026-09-28-import/README.md)，由各 Feature 的 change 帶入 spec（PD-09）。

## 需求意圖（原 intent.md）

日期：2026-09-23。本文記錄需求意圖；具體契約與驗收條件由 [能力規格](research/2026-09-28-import/README.md) 承接。

## Problem

一筆交易可能用到前面處理步驟產生的檔案，而那個步驟可能發生在另一個資料中心（DC）。**複製的目的，是讓後續處理所在的 DC 能取得交易所需的檔案。**

- **正常運作**：交易跨 DC 處理時，能使用前序步驟產生的檔案。
- **維修或災難**：希望其他 DC 仍能維持交易運作，不因故障 DC 無法提供檔案而停擺。
- **故障恢復**：補齊尚未完成的複製，恢復副本一致性。

**現行考量的兩種方式**

以下是需求提出者的方案評估，實際可用性與成本仍需設計及驗收確認。

| 方式 | 好處 | 主要顧慮 |
| --- | --- | --- |
| **ETL loader 在各 DC 間互相複製** | 實作正確且必要副本已到位時，各 DC 可使用自己的副本，具備高可用性的潛力 | M×N 傳輸關係難管理；自行實作容易漏掉送達追蹤與恢復；複製及補傳流量可能拖垮系統 |
| **Local first，shared DC fallback** | 優先讀本地，缺資料時向共用 DC 取得，實作較簡單 | 本地缺檔時依賴共用 DC；在極高可用性要求下，這項依賴可能成為限制 |

希望保留第一種方式「各 DC 持有必要副本」的好處，把容易實作錯誤的部分交給共用框架處理。

**NFS 存取缺少共用抽象層**

目前應用程式透過 File gateway，或由 client 自行操作 NFS。依現行使用經驗：

- **File gateway**：效率與可靠性未達需求。
- **Client 自行操作**：每個應用都要面對 NFS 的錯誤、逾時及恢復語意，HA／負載分配也難以正確處理。
- **缺乏共用能力**：不同 client 重複處理相同問題，接入與維護成本高，也容易出現不一致的行為。

## Proposed outcome

建立一套**容易接入、可重複使用的 framework**，讓應用專注在交易處理：

- **副本可供本地使用**：讓需要檔案的 DC 持有必要副本，降低交易對其他 DC 即時可用性的依賴。
- **複製有交代**：追蹤哪些資料尚未送達；故障後能重試、補傳與校驗，不能靜默漏檔。
- **流量可控制**：日常複製與故障補傳不應耗盡資源、拖垮交易服務。
- **NFS 行為有一致契約**：提供共用存取介面，集中處理發布、讀取、錯誤與恢復，讓 client 不必各自處理同一套細節。
- **接入成本低**：既有應用透過共用 library／服務接入，不必各自再造 loader 與可靠性機制。

## Affected users and systems

- **交易應用與開發團隊**：需要取得前序處理檔案，並接入共用的存取與複製能力。
- **各 DC 的應用、NAS／NFS 與複製服務**：承接檔案讀寫、傳輸與恢復。
- **維運與基礎設施團隊**：負責維修、故障處理、儲存環境與恢復驗收。

## Constraints

- 整合既有跨 DC 交易與 NAS／NFS 環境，降低既有應用的接入成本。
- 日常複製與故障補傳不得耗盡資源、拖垮交易服務。
- 現有 spec 的本地持續運作保證，以所需資料已在本地可用為前提；不保證 Source 永久毀損後零資料損失。

## Open questions

- **災難下的保證**：必要副本尚未到達、Source 永久毀損時，允許什麼資料損失或交易等待？
- **拓撲與範圍**：DC、Node 與「部署範圍」如何對應？[第一版範圍](#第一版範圍原-spec-11) 目前不支援跨部署範圍同步，需要確認與本意圖的跨 DC 情境是否一致。
- **存取與驗收**：Framework 對 NFS HA／負載分配負責到哪裡？如何證明可用性、傳輸量與接入成本符合需求？

---

需求來源：需求提出者的說明與 [跨 DC 資料同步框架討論](https://chatgpt.com/share/6ab2db59-0814-83ee-91b9-1af10458e1a3)。分享內容包含早期方案與 spec 草稿，具體技術契約以 repo 內適用的規格及最新設計修訂為準。

章節格式參照 [The AI-Native SDLC playbook 的 intent.md 範例](https://claude.com/blog/the-ai-native-sdlc-playbook)。

## 跨 Feature 的共用限制

以下需求約束每一個 Feature，還沒有實作。每次 Feature SA 都要檢查這次的行為碰到哪幾條；第一個讓某條成立的 Feature 用 ADDED 把它帶進自己的 spec，之後的 Feature 用 MODIFIED 擴充（PD-09）。

| 能力 | 需求 | 原文 |
| --- | --- | --- |
| core-guarantees | DG-01 Node Independence、DG-02 Local-First Availability、DG-03 Eventual Consistency、DG-04 No Silent Data Loss、DG-05 Operational Resilience、DG-06 End-to-End Critical Acceptance | [SA 輸入](research/2026-09-28-import/specs/core-guarantees/spec.md) |
| service-objectives | SLO-01 SLO / Service Objectives；表中 TBD 的數值是待決，不補數字 | [SA 輸入](research/2026-09-28-import/specs/service-objectives/spec.md) |

本文下面的「第一版範圍」與「第一版功能範圍外」也適用於每一個 Feature。

## 系統目的（原 spec §1）

建立共用的 Cross-Node File Synchronization Framework，使多個 Node 之間的檔案能持續、可靠地非同步同步，並在 Node、Network、Storage 或服務暫時故障後，自動且可驗證地恢復一致性。

**核心保證：在本 Node 的必要服務、Storage、容量正常，且交易所需資料已於本地可用時，其他 Node 的停機不得阻塞本地交易。故障解除後，系統自動補齊未完成的同步義務。**

## 第一版範圍（原 spec §1.1）

| 項目 | 決定 |
| --- | --- |
| File lifecycle | Ready 後內容不可變；不支援 overwrite、append、rename、delete 的跨 Node 同步 |
| 遠端資料未抵達 | 明確回報資料未就緒；由業務流程等待或重試，不影響其他獨立交易 |
| Supported downtime | 以單一 Target 連續停機 24 小時作為容量與恢復驗收情境 |
| 容量耗盡 | 提早告警；不得靜默清除待同步資料；無法安全接受新寫入時明確拒絕 |
| 故障保護 | 保證暫時故障後的恢復；不保證 Source Storage 永久毀損後零資料損失 |
| Topology | 固定的 Phase（Node）集合，≤10 Node，任一 Node 可為自身資料的 Source；第一版不支援跨部署範圍同步，也不支援運行期間新增、移除或變更同步對象 |
| Identity 與 Policy 登錄 | Namespace 與 Data class 須於 Policy 預先登錄；未登錄者於 write 時明確拒絕，不得接受後靜默不同步 |
| Source 資料刪除 | Framework 不刪除、不提供刪除 Source 資料的動詞；Source 保存由現有 NAS 管理政策負責 |

## 系統能力（原 spec §4）

Framework 提供下列系統能力：

| 能力 | 必須提供的結果 |
| --- | --- |
| Standard Storage Access | 統一存取、完成寫入、結果查證與錯誤語意 |
| Local readiness | 可持久恢復的 Source Ready 與完整性基準 |
| Cross-Node replication | 依固定同步對象執行非同步傳輸及發布 |
| Reconciliation | 獨立發現缺失義務及資料不一致，修復後再驗證 |
| Operations | 可觀測、受控重試、暫停、恢復與故障查證 |
| Configuration Management | Versioned desired state、本地持久化與安全啟用 |

Standard Storage Access contract 應能作為 Application 與 synchronization service 共用的存取邊界；是否包裝成獨立 library、如何部署屬於設計。

## 第一版功能範圍外（原 spec §21.1）

- Ready 檔案的 overwrite、append、rename、delete 跨 Node 同步。
- 多 Node 共同修改同一 File identity 的衝突合併。
- 運行期間新增、移除 Node 或變更同步對象，以及其歷史資料回補策略。
- Source Storage 永久毀損後零資料損失的災難復原保證。
- 跨部署範圍同步（WAN）。
- 依 lot 下一站動態決定 Required targets（routing-based targets）；Policy 維持靜態。
- Source 端刪除動詞（Retire）與 Framework 主導的 Source retention。
