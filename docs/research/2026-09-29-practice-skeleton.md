---
date: 2026-09-29T07:30:00+08:00
researcher: Project Lead Agent（Claude Code，feature-to-spec 練習）
repository: yschiang/cross-node-root（root）＋ yschiang/cross-node-file-transfer（程式）
topic: 練習：roadmap #1 專案骨架的 SA 研究
tags: [research, practice-skeleton, engineering-baseline, feature-to-spec]
git_commit: df2046d（root，feature/practice-skeleton，基準 origin/main 51042fe）；8902354（程式 repo main）
branch: feature/practice-skeleton
working_tree: clean
status: complete
last_updated: 2026-09-29
last_updated_by: Project Lead Agent
---

# 練習：專案骨架的 SA 研究

## 問題

roadmap #1「專案骨架」要交付什麼、落在哪個 repo、依賴什麼；既有草稿 `project-skeleton` 的待決 Q-4、Q-5 現在有哪些新證據。

## 結論

1. 程式 repo 目前只有 README，骨架（Maven、CI、工程規則）全部要從零建。
2. root 的 `AGENTS.md` 已由 PR #3 放入，並寫明服務 repo 各自有自己的 `AGENTS.md`；這讓 Q-4 的方向有了已合併的依據，Q-5 的比較對象也變成三份。
3. 程式 repo 是 private，GitHub 目前的方案不能查或設 branch protection、ruleset，所以「必要 check」無法由 GitHub 強制，只能由流程（PR Pass 讀 CI 結果）判定。

## 事實

| # | 事實 | 證據 |
| --- | --- | --- |
| F1 | 程式 repo `cross-node-file-transfer` 只有 `README.md`，一個 commit | `repos/cross-node-file-transfer` 於 `8902354`；`git ls-remote` 只有 `main` |
| F2 | 程式 repo 是 private；查 branch protection 與 rulesets 都回 403「Upgrade to GitHub Pro or make this repository public」 | `gh api repos/yschiang/cross-node-file-transfer/branches/main/protection`、`/rulesets`（2026-09-29） |
| F3 | root 的 `AGENTS.md` 寫「本 repo 是 root repo…程式在 `repos.yaml` 列的服務 repo，各自有自己的 AGENTS.md」，並含 Commit 訊息規範與 root 的 scope 表 | [AGENTS.md](../../AGENTS.md)（`d34dc44`，blob `c93055be4c32`） |
| F4 | root 的 `AGENTS.md` 來自 loop-engineering `templates/AGENTS.md`，由 `setup.sh --project` 在 repo 沒有時放入 | loop-engineering `setup.sh` 第 8–11、247 行（`102623f`） |
| F5 | PD-05 釘的工程規則是 gigaxfer 工作目錄的舊版 `AGENTS.md`（sha256 `f69d669a…`）；gigaxfer 工作目錄現在的版本已加 Commit 訊息規範，sha256 `b4ea97e5…`，仍未進 gigaxfer 版控 | [decisions.md](../decisions.md) PD-05；`shasum -a 256`（2026-09-29） |
| F6 | 技術棧：Java 21、Maven 多模組、Spring Boot；DB 為 Oracle，本機 H2 Oracle mode，CI 用 Oracle Free container | PD-04；匯入設計 D9、D38 |
| F7 | gigaxfer P00 建置假設：Maven 3.9、Java 21（LTS）、JUnit 5、AssertJ | gigaxfer `4e9cba4` `docs/superpowers/plans/P00-roadmap.md` 第 25–32 行 |
| F8 | gigaxfer CI 只有一個 job：JDK 21（temurin）、`mvn -B -ntp verify`，觸發於 PR 與 push main；gigaxfer 工作目錄另有未 commit 的 `commit-messages` job 與 `scripts/hooks/commit-msg` | gigaxfer `4e9cba4` `.github/workflows/ci.yml`；gigaxfer 工作目錄 `git diff` |
| F9 | root 只有 `pages.yml`（部署設計網頁），沒有建置用 CI | `.github/workflows/` |
| F10 | 下一個 Feature #2 Finalize 協議只需要 core（library 端的寫入、finalize、discard） | [roadmap](../roadmap.md) #2 列；匯入設計 §1 元件表 |
| F11 | 既有草稿 `project-skeleton` 已決定：新能力 `engineering-baseline`（PD-07）、只建 parent 與 core（Q-2）、AGENTS.md 原樣複製只改三處（Q-3） | `openspec/changes/project-skeleton/proposal.md` |
| F12 | roadmap 標 #1 為「近期，SA 草稿完成」；決策紀錄沒有依 loop-engineering D63 記下「確認 roadmap、選定 #1」的條目 | [roadmap](../roadmap.md)；[decisions.md](../decisions.md) |

引用版本：project intent `6d007d1`（blob `097798be3263`）、roadmap `6d007d1`（blob `d21009053387`）、高層設計 `system-design.md` `627eb12`（blob `836f6b49721d`）、`design-decisions.md` `627eb12`（blob `c846ef5577fe`）、決策紀錄 `6d007d1`（blob `9b17857dfea9`）。

## 假設

- A1：Claude Code 從子目錄啟動時會往上層讀 `CLAUDE.md`；Codex 從 git repo 根目錄往下找 `AGENTS.md`，從程式 repo 啟動讀不到 root 的規則（依各工具文件，未在本機實測）。不論結果，程式 repo 單獨 clone（CI、其他開發者）時沒有 root 可讀。
- A2：跨 Feature 的共用限制（core-guarantees、service-objectives）都是產品行為，骨架不碰。

## 未知

- U1：程式 repo 的工程規則要用哪份內容起頭（F3 的 root 版、F5 的 gigaxfer 新版，或 PD-05 的舊版）。
- U2：commit 訊息檢查（hook、CI job）是否屬於本 Feature。
- U3：「必要 check」在 GitHub 無法強制時（F2），驗收時怎麼判定。
