import pathlib

ROOT = pathlib.Path(__file__).parent.parent.resolve()
f = ROOT / 'pages' / 'register.html'
src = f.read_text(encoding='utf-8')

AGENCY_JS = '''
    /* ============================================================
       지사 — 멀티 오픈 운영 지역 선택 UI
    ============================================================ */

    // ── 지사 상태 ──
    var agencyOpenSido   = new Set();
    var agencySelectedGu = new Map();

    // ── 지사 DOM 참조 ──
    var agencySidoEl     = document.getElementById('agency-sido-chips');
    var agencyGuPanelsEl = document.getElementById('agency-gu-panels');
    var agencyTagsEl     = document.getElementById('agency-selected-tags');
    var agencyNoHint     = document.getElementById('agency-no-region-hint');
    var agencyHidden     = document.getElementById('agency-regions-hidden');
    var agencyPanelMap   = {};

    Object.keys(REGION_DATA).forEach(function(sido) {
      var sidoBtn = document.createElement('button');
      sidoBtn.type = 'button';
      sidoBtn.className = 'sido-chip';
      sidoBtn.dataset.sido = sido;
      sidoBtn.setAttribute('aria-expanded', 'false');
      sidoBtn.innerHTML = sido + ' <span class="sido-arrow" aria-hidden="true">&#9660;</span>';
      sidoBtn.addEventListener('click', function() { agencyOnSidoClick(sido, sidoBtn); });
      agencySidoEl.appendChild(sidoBtn);

      var panel = document.createElement('div');
      panel.className = 'gu-panel';

      var inner = document.createElement('div');
      inner.className = 'gu-panel-inner';

      var hdr = document.createElement('div');
      hdr.style.cssText = 'display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;';

      var countBadge = document.createElement('span');
      countBadge.style.cssText = 'font-size:0.75rem;color:#888;font-weight:600;flex:1;';
      countBadge.textContent = sido + ' (0개 선택됨)';

      var allBtn = document.createElement('button');
      allBtn.type = 'button';
      allBtn.className = 'gu-chip gu-chip-all';
      allBtn.textContent = '전체 선택';
      allBtn.addEventListener('click', function() { agencyToggleAll(sido, allBtn, countBadge); });

      hdr.appendChild(countBadge);
      hdr.appendChild(allBtn);

      var divLine = document.createElement('div');
      divLine.className = 'gu-divider';

      var guWrap = document.createElement('div');
      guWrap.className = 'gu-chips';

      REGION_DATA[sido].forEach(function(gu) {
        var key = sido + '-' + gu;
        var chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'gu-chip';
        chip.dataset.key = key;
        chip.textContent = gu;
        chip.setAttribute('aria-pressed', 'false');
        chip.addEventListener('click', function() { agencyToggleGu(key, chip, sido, allBtn, countBadge); });
        guWrap.appendChild(chip);
      });

      inner.appendChild(hdr);
      inner.appendChild(divLine);
      inner.appendChild(guWrap);
      panel.appendChild(inner);
      agencyGuPanelsEl.appendChild(panel);
      agencyPanelMap[sido] = { panel: panel, guChipsWrap: guWrap, allBtn: allBtn, countBadge: countBadge, sidoBtn: sidoBtn };
    });

    function agencyOnSidoClick(sido, btn) {
      var info = agencyPanelMap[sido];
      if (agencyOpenSido.has(sido)) {
        agencyOpenSido.delete(sido);
        info.panel.classList.remove('open');
        btn.classList.remove('active');
        btn.setAttribute('aria-expanded', 'false');
      } else {
        agencyOpenSido.add(sido);
        info.panel.classList.add('open');
        btn.classList.add('active');
        btn.setAttribute('aria-expanded', 'true');
      }
    }

    function agencyToggleGu(key, chip, sido, allBtn, countBadge) {
      if (agencySelectedGu.has(key)) {
        agencySelectedGu.delete(key);
        chip.classList.remove('selected');
        chip.setAttribute('aria-pressed', 'false');
      } else {
        agencySelectedGu.set(key, true);
        chip.classList.add('selected');
        chip.setAttribute('aria-pressed', 'true');
      }
      agencySyncState(sido, allBtn, countBadge);
      agencyRenderTags();
    }

    function agencyToggleAll(sido, allBtn, countBadge) {
      var districts = REGION_DATA[sido];
      var allSel = districts.every(function(d) { return agencySelectedGu.has(sido + '-' + d); });
      var guWrap = agencyPanelMap[sido].guChipsWrap;
      districts.forEach(function(d) {
        var key = sido + '-' + d;
        var chip = guWrap.querySelector('[data-key="' + key + '"]');
        if (allSel) {
          agencySelectedGu.delete(key);
          if (chip) { chip.classList.remove('selected'); chip.setAttribute('aria-pressed', 'false'); }
        } else {
          agencySelectedGu.set(key, true);
          if (chip) { chip.classList.add('selected'); chip.setAttribute('aria-pressed', 'true'); }
        }
      });
      agencySyncState(sido, allBtn, countBadge);
      agencyRenderTags();
    }

    function agencySyncState(sido, allBtn, countBadge) {
      var districts = REGION_DATA[sido];
      var selCount  = districts.filter(function(d) { return agencySelectedGu.has(sido + '-' + d); }).length;
      var allSel    = selCount === districts.length;
      allBtn.classList.toggle('selected', allSel);
      allBtn.textContent = allSel ? '전체 해제' : '전체 선택';
      countBadge.textContent = sido + ' (' + selCount + '\uac1c \uc120\ud0dd\ub428)';
      countBadge.style.color = selCount > 0 ? '#FF5252' : '#888';
      var sb    = agencyPanelMap[sido].sidoBtn;
      var arrow = sb.querySelector('.sido-arrow');
      sb.textContent = sido + (selCount > 0 ? ' (' + selCount + ')' : '') + ' ';
      if (arrow) { sb.appendChild(arrow); }
      else { var a = document.createElement('span'); a.className = 'sido-arrow'; a.setAttribute('aria-hidden','true'); a.innerHTML = '&#9660;'; sb.appendChild(a); }
    }

    function agencyRenderTags() {
      agencyTagsEl.innerHTML = '';
      agencyHidden.value = Array.from(agencySelectedGu.keys()).join(',');
      if (agencySelectedGu.size === 0) { agencyNoHint.style.display = ''; return; }
      agencyNoHint.style.display = 'none';
      showErr('err-agency-region', false);
      agencySelectedGu.forEach(function(_, key) {
        var parts = key.split('-');
        var label = parts[0] + ' \u00b7 ' + parts[1];
        var tag   = document.createElement('span');
        tag.className = 'selected-tag';
        tag.innerHTML = label + '<button type="button" class="tag-remove" aria-label="' + label + ' \uc81c\uac70">\u00d7</button>';
        tag.querySelector('.tag-remove').addEventListener('click', function() { agencyRemoveTag(key); });
        agencyTagsEl.appendChild(tag);
      });
    }

    function agencyRemoveTag(key) {
      agencySelectedGu.delete(key);
      var sido = key.split('-')[0];
      var info = agencyPanelMap[sido];
      if (info) {
        var chip = info.guChipsWrap.querySelector('[data-key="' + key + '"]');
        if (chip) { chip.classList.remove('selected'); chip.setAttribute('aria-pressed','false'); }
        agencySyncState(sido, info.allBtn, info.countBadge);
      }
      agencyRenderTags();
    }

    agencyRenderTags();
'''

MARKER = '    // 초기 렌더\n    renderTags();'
if MARKER not in src:
    print('ERROR: marker not found')
else:
    new_src = src.replace(MARKER, MARKER + '\n' + AGENCY_JS, 1)
    f.write_text(new_src, encoding='utf-8')
    lines = new_src.count('\n')
    print('OK written', lines, 'lines')
