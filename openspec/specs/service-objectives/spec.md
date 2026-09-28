# service-objectives Specification

## Purpose

服務目標與驗收參數。表中標為 TBD 的數字在正式驗收前必須補齊。

來源：gigaxfer `docs/spec.md` v0.3 §18（commit `4e9cba4`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。

## Requirements

### Requirement: SLO-01 SLO / Service Objectives

**正式驗收前須完成本表所有 TBD；不能以 TBD 宣告生產就緒。**

| Objective / Parameter | Requirement |
| --- | --- |
| Supported Target downtime | 24 hours |
| Workload envelope | 每套部署 ≤10 Node；每 Node 每日 ≥10⁵ 檔案；檔案 MB 級；推算單一 Target 24 小時累積 10²–10³ GB。持續／尖峰 files/sec、bytes/sec、file size distribution、最大檔案大小：TBD |
| Local availability & latency | 正常、單一 Target 停機及 recovery 期間的成功率與 P95/P99 latency：TBD |
| Normal replication freshness | Source→Target P95 / P99 replication lag：TBD |
| Accepted obligation durability | 定義故障測試中，已接受且仍有有效資料來源的義務遺失數 = 0 |
| Integrity | 注入的缺漏／損壞於約定檢查範圍及時限內被發現；錯誤完成數 = 0 |
| Recovery | 24 小時 downtime 後，在持續新流量下完成故障期間 backlog 的期限：TBD |
| Reconciliation | Shallow check 週期、Deep check 完整覆蓋週期（= T30 最長偵測時間）、可修復差異恢復期限：TBD |
| Capacity | 保留容量、暫存空間、state 容量、告警及拒絕新寫入門檻：TBD |
| Unknown outcome | 必要服務恢復後的查證期限：TBD |
| Measurement | 時間來源 = Source Node 時鐘（無跨 Node 時鐘誤差參數）；統計窗口與樣本規則：TBD |

永久 Source Storage 毀損後零資料損失不在第一版保證內。Replication freshness 與災難 RPO 不得混用；如未來納入永久毀損保護，另訂 RPO 與保護機制。

Reconciliation、Recovery 時限的起訖點及例外條件必須明列。已知人工處理障礙可獨立分類，但原始 elapsed age 不得停止或被重設以掩蓋等待。

#### Scenario: AC-SLO-01（由本需求原文轉寫）

- **THEN** **正式驗收前須完成本表所有 TBD；不能以 TBD 宣告生產就緒。**
