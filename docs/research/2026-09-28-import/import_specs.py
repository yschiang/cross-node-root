"""Import gigaxfer spec.md (origin/main) into OpenSpec capability specs for cross-node-file-transfer.

Verbatim move: requirement bodies are copied as-is; only headings are reformatted for OpenSpec.
Scenarios come from spec §19 (T01-T32) and the AC tables, attached per docs/design/traceability.md.
"""
import os
import re
import shutil
import subprocess
import sys

SRC_REPO = '/Users/johnson.chiang/workspace/gigaxfer'
REV = '4e9cba4cd143cbc2e583b1fda41ba885970025c0'
DST = '/Users/johnson.chiang/workspace/cross-node-file-transfer'


def git_show(path):
    return subprocess.run(['git', '-C', SRC_REPO, 'show', f'{REV}:{path}'],
                          check=True, capture_output=True, text=True).stdout


spec = git_show('docs/spec.md')
trace = git_show('docs/design/traceability.md')
L = spec.split('\n')

# --- section index -----------------------------------------------------------
heads = [(i, len(m[1]), m[2].strip()) for i, l in enumerate(L) if (m := re.match(r'(#{1,6}) (.+)', l))]


def body(title_prefix):
    """Lines between the heading starting with title_prefix and the next heading of any level."""
    for n, (i, lvl, t) in enumerate(heads):
        if t.startswith(title_prefix):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(L)
            return '\n'.join(L[i + 1:end]).strip('\n')
    raise KeyError(title_prefix)


def strip_tables(text):
    return '\n'.join(l for l in text.split('\n') if not l.startswith('|')).strip('\n')


def reqs_in_chapter(chapter_prefix):
    """(id, title, body) for '### XX-NN — Title' headings under a '## N.' chapter."""
    start = next(n for n, h in enumerate(heads) if h[2].startswith(chapter_prefix))
    out = []
    for i, lvl, t in heads[start + 1:]:
        if lvl <= 2:
            break
        m = re.match(r'([A-Z]{2}-\d\d) — (.+)', t)
        if m:
            out.append((m[1], m[2], body(t)))
    return out


def chapter_intro(chapter_prefix):
    start = next(n for n, h in enumerate(heads) if h[2].startswith(chapter_prefix))
    i = heads[start][0]
    j = heads[start + 1][0]
    return '\n'.join(L[i + 1:j]).strip('\n')


# --- acceptance rows ---------------------------------------------------------
tests = {}
for l in body('19. Required Acceptance Tests').split('\n'):
    m = re.match(r'\| (T\d\d) \| (.+?) \| (.+?) \|$', l)
    if m:
        tests[m[1]] = (m[2], m[3])
assert len(tests) == 32, len(tests)

acs = {}
for l in L:
    m = re.match(r'\| (AC-[A-Z]+-\d\d) \| (.+?) \|$', l)
    if m:
        acs[m[1]] = m[2]
assert len(acs) == 13, sorted(acs)

# --- traceability (many-to-many) --------------------------------------------
KEY = {'§11': 'CP-01', '§12': 'CP-02', '§13': 'CFG-01', '§14': 'RR-06', '§15': 'OPS-01',
       '§16': 'OPS-02', '§17': 'OPS-03', '§20': 'DG-06'}
verifies = {}
for l in trace.split('\n'):
    if not l.startswith('| ') or l.startswith('| Requirement') or l.startswith('| ---'):
        continue
    cells = [c.strip() for c in l.strip().strip('|').split('|')]
    first = cells[0].split()[0]
    rid = KEY.get(first, first)
    ids = []
    for tok in re.findall(r'T\d\d|AC-[A-Z]+-\d\d(?:/\d\d)*', cells[2]):
        m = re.match(r'(AC-[A-Z]+-)(\d\d)((?:/\d\d)*)', tok)
        ids += ([m[1] + m[2]] + [m[1] + x for x in m[3].split('/') if x]) if m else [tok]
    verifies[rid] = ids

# Judgement calls, recorded in the import note:
JUDGED = {
    'DG-01': ['T04'],                        # T04 is not listed in traceability.md
    'DG-04': ['AC-NODE-03'],                 # AC-NODE-03 is not listed in traceability.md
    'CFG-01': ['AC-CFG-01', 'AC-CFG-04'],    # defined in §13; traceability lists them under §11 only
}
for rid, extra in JUDGED.items():
    verifies.setdefault(rid, [])
    verifies[rid] += [x for x in extra if x not in verifies[rid]]

# Scenarios transcribed from the requirement's own acceptance sentence (no test exists):
DERIVED = {
    'OPS-02': ('AC-OPS-01', '指標至少可依 Source→Target 區分；正常與 recovery 時段分開呈現。'),
    'SLO-01': ('AC-SLO-01', '**正式驗收前須完成本表所有 TBD；不能以 TBD 宣告生產就緒。**'),
}

# --- §20 end-to-end ------------------------------------------------------------
given = body('Given')
when = body('When')
then_all = body('Then')
then_bullets = '\n'.join(l for l in then_all.split('\n') if l.startswith('- '))
then_rest = '\n'.join(l for l in then_all.split('\n') if not l.startswith('- ')).strip('\n')
e2e_intro_rule = chapter_intro('19. Required Acceptance Tests')
e2e_scenario = f'**Given**\n\n{given}\n\n**When**\n\n{when}\n\n**Then**\n\n{then_bullets}'

# --- §4 capability results -------------------------------------------------------
scope = {}
for l in body('4. System Scope').split('\n'):
    m = re.match(r'\| (.+?) \| (.+?) \|$', l)
    if m and m[1] not in ('能力', '---'):
        scope[m[1]] = m[2]

purpose_line = next(l for l in body('1. Purpose').split('\n') if l.startswith('建立共用'))
core_line = next(l for l in body('1. Purpose').split('\n') if l.startswith('**核心保證'))
final_principle = next(l for l in body('21.2').split('\n') if l.startswith('**最終驗收原則'))


SCOPE_LINK = '原 spec §4 要求的結果（見 [系統能力](../../../docs/project-intent.md#系統能力原-spec-4)）'


def src(sections, has_tests):
    line = f'來源：gigaxfer `docs/spec.md` v0.3 {sections}（commit `{REV[:7]}`）。需求 ID 沿用原文；Scenario 依 `docs/design/traceability.md` 掛上。'
    if has_tests:
        line += 'T 開頭的 Scenario 取自原 §19，共通執行條件見 core-guarantees 的 DG-06。'
    return line


CAPS = [
    ('core-guarantees', '§1、§1.2、§3、§10 Maintenance Acceptance、§19 前言、§20',
     f'整個系統對 Application 與維運者的核心承諾，以及這些承諾成立的條件。\n\n{purpose_line}\n\n{core_line}\n\n### 保證成立的條件\n\n{body("1.2")}\n\n{final_principle}',
     reqs_in_chapter('3. Design Goals') + [('DG-06', 'End-to-End Critical Acceptance',
                                            f'{e2e_intro_rule}\n\n{then_rest}')]),
    ('storage-access', '§5', f'Application 與同步服務共用的儲存存取邊界。\n\n{SCOPE_LINK}：{scope["Standard Storage Access"]}。',
     reqs_in_chapter('5. Storage Access')),
    ('file-readiness', '§6', f'檔案的權威、寫入完成與可見時點，以及 identity 衝突。\n\n{SCOPE_LINK}：{scope["Local readiness"]}。',
     reqs_in_chapter('6. File Identity')),
    ('replication', '§7、§14', f'跨 Node 的非同步複製、同步義務與其狀態。\n\n{SCOPE_LINK}：{scope["Cross-Node replication"]}。',
     reqs_in_chapter('7. Replication') + [('RR-06', 'Operational States', body('14. Operational States'))]),
    ('reconciliation', '§8', f'獨立於任務紀錄，找出缺失的義務與不一致並修復。\n\n{SCOPE_LINK}：{scope["Reconciliation"]}。',
     reqs_in_chapter('8. Reconciliation')),
    ('integrity', '§9', '內容完整性的基準、完成條件與持續失敗的處理。完整性同時被就緒、複製與對帳使用，所以自成一個能力。',
     reqs_in_chapter('9. Integrity')),
    ('retention-capacity', '§10', '同步完成前的資料保留，以及容量不足時的告警與拒絕。',
     reqs_in_chapter('10. Retention')),
    ('control-plane', '§11、§12', '跨 Node 共用的管理面，以及 Data Plane 不依賴它即時運作。',
     [('CP-01', 'Control Plane Requirements', body('11. Control Plane')),
      ('CP-02', 'Data Plane Independence', strip_tables(body('12. Data Plane')))]),
    ('configuration', '§13', f'版本化設定的發布、啟用與退回。\n\n{SCOPE_LINK}：{scope["Configuration Management"]}。',
     [('CFG-01', 'Configuration Flow', strip_tables(body('13. Configuration Flow')))]),
    ('operations', '§15、§16、§17', f'維運人員需要的查詢、指標與受控操作。\n\n{SCOPE_LINK}：{scope["Operations"]}。',
     [('OPS-01', 'Operational Readiness', body('15. Operational Readiness')),
      ('OPS-02', 'Required Operational Metrics', body('16. Required Operational Metrics')),
      ('OPS-03', 'Operational Control', body('17. Operational Control'))]),
    ('service-objectives', '§18', '服務目標與驗收參數。表中標為 TBD 的數字在正式驗收前必須補齊。',
     [('SLO-01', 'SLO / Service Objectives', body('18. SLO'))]),
]


def scenario(sid):
    if sid in tests:
        w, t = tests[sid]
        return f'#### Scenario: {sid} {w}\n\n- **WHEN** {w}\n- **THEN** {t}'
    if sid in acs:
        return f'#### Scenario: {sid}\n\n- **THEN** {acs[sid]}'
    raise KeyError(sid)


def render(name, sections, purpose, reqs):
    has_tests = any(t.startswith('T') for rid, _, _ in reqs for t in verifies.get(rid, []))
    out = [f'# {name} Specification', '', '## Purpose', '', purpose, '', src(sections, has_tests), '', '## Requirements', '']
    for rid, title, text in reqs:
        out += [f'### Requirement: {rid} {title}', '', text, '']
        sids = verifies.get(rid, [])
        for sid in sids:
            out += [scenario(sid), '']
        if rid in DERIVED:
            sid, sentence = DERIVED[rid]
            out += [f'#### Scenario: {sid}（由本需求原文轉寫）', '', f'- **THEN** {sentence}', '']
        if rid == 'DG-06':
            out += ['#### Scenario: E2E-01 End-to-End Critical Acceptance Scenario', '', e2e_scenario, '']
        assert sids or rid in DERIVED or rid == 'DG-06', f'{rid} has no scenario'
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).rstrip('\n') + '\n'


written = {}
for name, sections, purpose, reqs in CAPS:
    text = render(name, sections, purpose, reqs)
    p = os.path.join(DST, 'openspec', 'specs', name, 'spec.md')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(text)
    written[name] = text

# --- project intent --------------------------------------------------------------
intent = git_show('intent.md')
intent_body = intent.split('\n', 1)[1].lstrip('\n')  # drop the original H1
scope_body = body('4. System Scope')
oos = body('21.1')
pi = f'''# Project intent：cross-node-file-transfer

來源：gigaxfer `intent.md` 與 `docs/spec.md` v0.3 §1、§1.1、§4、§21.1（commit `{REV[:7]}`），內容原樣搬入。需求與驗收在 `openspec/specs/`。

## 需求意圖（原 intent.md）

{intent_body.rstrip()}

## 系統目的（原 spec §1）

{purpose_line}

{core_line}

## 第一版範圍（原 spec §1.1）

{body("1.1")}

## 系統能力（原 spec §4）

{scope_body}

## 第一版功能範圍外（原 spec §21.1）

{oos}
'''
os.makedirs(os.path.join(DST, 'docs'), exist_ok=True)
open(os.path.join(DST, 'docs', 'project-intent.md'), 'w', encoding='utf-8').write(pi)

# --- verbatim copies ---------------------------------------------------------------
COPIES = ['CONTEXT.md', 'docs/design/system-design.md', 'docs/design/design-decisions.md',
          'docs/design/domain-decisions.md', 'docs/design/monitoring.md', 'docs/design/traceability.md',
          'docs/adr/0001-source-owned-obligation-and-clock.md', 'docs/adr/0002-target-pull-over-http.md',
          'docs/adr/0003-git-as-control-plane.md']
for c in COPIES:
    p = os.path.join(DST, c)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(git_show(c))

design_readme = f'''# 設計文件

本目錄的設計文件與 `docs/adr/` 從 gigaxfer 原樣複製（commit `{REV[:7]}`），不改寫。內文提到的 `docs/spec.md` 章節，現在對應 `openspec/specs/` 的能力規格，對照見 [匯入紀錄](../research/2026-09-28-import-from-gigaxfer.md)。

gigaxfer 的 PR #11（設計裁定 D58）尚未合併，這裡不含它的修改。

## 留給 System／Software Design（原 spec §21.2）

{body("21.2")}
'''
open(os.path.join(DST, 'docs', 'design', 'README.md'), 'w', encoding='utf-8').write(design_readme)

# --- mechanical checks -------------------------------------------------------------
allout = '\n'.join(written.values()) + '\n' + pi + '\n' + design_readme
req_ids = re.findall(r'^### Requirement: (\S+)', '\n'.join(written.values()), re.M)
src_ids = re.findall(r'^### ([A-Z]{2}-\d\d) —', spec, re.M)
missing_req = [r for r in src_ids if r not in req_ids]
dup_req = sorted({r for r in req_ids if req_ids.count(r) > 1})
missing_tests = [t for t in tests if f'Scenario: {t} ' not in allout]
missing_acs = [a for a in acs if f'Scenario: {a}' not in allout]

# every non-empty source line of imported chapters must appear verbatim somewhere in the output
imported_chapters = ['1. Purpose', '1.1', '1.2', '3. Design Goals', '4. System Scope', '5.', '6.', '7.', '8.', '9.',
                     '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.', '20.', '21.']
dropped = {'本文件定義 System Requirements、Constraints、Operational Readiness、Test Cases 與 Acceptance Criteria。Component、Class、Protocol Implementation、Database Schema 與 Deployment Design 留待後續設計。'}
lost = []
chapter_starts = [n for n, h in enumerate(heads) if h[1] == 2 or h[2].startswith(('1.1', '1.2', '21.1', '21.2'))]
for n, (i, lvl, t) in enumerate(heads):
    if lvl != 2 or not any(t.startswith(c) for c in imported_chapters):
        continue
    nxt = next((heads[k][0] for k in range(n + 1, len(heads)) if heads[k][1] == 2), len(L))
    for line in L[i + 1:nxt]:
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('| ---') or s in dropped:
            continue
        if re.match(r'\| (T\d\d|AC-[A-Z]+-\d\d|ID|能力) \|', s):  # table rows turned into scenarios / headers
            continue
        if s not in allout:
            lost.append(s)

# --- documented post-edits (after the verbatim check; listed in the import record) ---------
POST_EDITS = [
    ('openspec/specs/control-plane/spec.md', '新 Node 的首次初始化不屬於上述重啟保證。',
     '新 Node 的首次初始化不屬於 AC-CP-02 所述的重啟保證。', 'F-04：原表格移為下方 Scenario，「上述」改為明確 ID'),
    ('docs/project-intent.md', '[spec](docs/spec.md)', '[能力規格](../openspec/specs/)',
     'F-02：原 spec 已拆成能力規格'),
    ('docs/project-intent.md', '[spec §1.1](docs/spec.md#11-已確認的第一版範圍)', '[第一版範圍](#第一版範圍原-spec-11)',
     'F-02：§1.1 已搬進本檔'),
    ('CONTEXT.md', '**Data Plane**:',
     '**LKG**:\nLast Known Good configuration，可恢復使用的有效設定。（取自原 spec §2；gigaxfer 的 CONTEXT.md 未收錄）\n\n**Data Plane**:',
     'F-01：原 spec §2 的 LKG 定義'),
]
for rel, old, new, why in POST_EDITS:
    fp = os.path.join(DST, rel)
    t = open(fp, encoding='utf-8').read()
    assert t.count(old) == 1, (rel, old)
    open(fp, 'w', encoding='utf-8').write(t.replace(old, new))
print('post-edits applied:', len(POST_EDITS))

print('capabilities:', len(written))
print('requirements:', len(req_ids), 'source ids:', len(src_ids))
print('missing source requirement ids:', missing_req)
print('duplicate requirement ids:', dup_req)
print('tests without scenario:', missing_tests)
print('ACs without scenario:', missing_acs)
print('source lines not found in output:', len(lost))
for s in lost:
    print('  LOST:', s[:120])
sys.exit(1 if (missing_req or dup_req or missing_tests or missing_acs or lost) else 0)
