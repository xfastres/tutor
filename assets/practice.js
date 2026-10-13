/**
 * practice.js — tutor（Teach Hybrid v9）学习者页面交互（无依赖）
 *
 * 支持的标记：
 *  1. 预测选择题（一次作答，刷新后保留）
 *     <div class="predict" data-answer="1" data-ok="…" data-no="…" data-task="0008-P1">
 *       <button type="button" data-choice="0">…</button> …
 *       <div class="feedback"></div>
 *     </div>
 *  2. 语义校验（需要 window.TeachChecks[scenario](text) 或 window.SqlMini.run(scenario, text)，
 *     返回 {ok, message, rows?|output?}）
 *     <div class="semantic-check" data-scenario="preserve-depts">
 *       <textarea></textarea> <button type="button" data-run>运行</button>
 *       <pre class="result-view"></pre> <div class="feedback"></div>
 *     </div>
 *  3. 自由作答（只保存，不判分；贴回对话由 Agent 判）
 *     <div class="free"><textarea></textarea><button type="button" data-save>保存</button><div class="feedback"></div></div>
 *  4. 可变题库（需要 window.TeachDrills[name] = function (rng) { return {prompt, choices, answer, explain}; }
 *     answer 为选项下标或选项文本；rng() 返回 [0,1) 随机数）
 *     <div class="drill" data-drill="leftmost-prefix" data-target="5"></div>
 *  5. 答案揭示追踪（打开即记 revealed，证据按 answer_exposed 处理）
 *     <details class="answer" data-task="0008-P3"><summary>看答案</summary>…</details>
 *  6. 导出 / 重置
 *     <div class="export-bar">
 *       <button type="button" data-export-answers>导出作答</button>
 *       <button type="button" data-reset-answers>清空本页作答</button>
 *       <div class="feedback"></div>
 *     </div>
 *     <pre class="export-out"></pre>
 *
 * task_id 来源：元素 data-task → 所在 <section> 内 .label code 文本 → untitled-N。
 * 所有作答存 localStorage['teach-answers:' + location.pathname]，刷新后保留。
 * 导出为 JSON 数组：[{task_id, kind, answer, correct, attempts, revealed, at, detail?}]。
 */
(function () {
  'use strict';

  var KEY = 'teach-answers:' + location.pathname;
  var store = load();
  var untitled = 0;

  function load() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || '{}') || {};
    } catch (e) {
      return {};
    }
  }

  function persist() {
    try {
      localStorage.setItem(KEY, JSON.stringify(store));
    } catch (e) {
      /* 隐私模式等：仅内存保存 */
    }
  }

  function hhmm(iso) {
    var d = iso ? new Date(iso) : new Date();
    return d.toTimeString().slice(0, 5);
  }

  function taskIdOf(el) {
    var explicit = el.getAttribute('data-task');
    if (explicit) {
      return explicit;
    }
    var section = el.closest('section');
    var code = section ? section.querySelector('.label code') : null;
    if (code && code.textContent.trim()) {
      return code.textContent.trim();
    }
    untitled += 1;
    return 'untitled-' + untitled;
  }

  function attemptsOf(id) {
    return store[id] ? store[id].attempts || 0 : 0;
  }

  function record(id, kind, patch) {
    var r = store[id] || {
      task_id: id,
      kind: kind,
      answer: null,
      correct: null,
      attempts: 0,
      revealed: false,
      at: null
    };
    Object.keys(patch).forEach(function (k) {
      r[k] = patch[k];
    });
    r.at = new Date().toISOString();
    store[id] = r;
    persist();
    return r;
  }

  function setFeedback(box, ok, msg) {
    var fb = box.querySelector('.feedback');
    if (!fb) {
      return;
    }
    fb.textContent = msg;
    fb.className = 'feedback ' + (ok === null ? 'note' : ok ? 'ok' : 'bad');
  }

  function pick(box, selector, tag) {
    var found = box.querySelector(selector);
    if (found) {
      return found;
    }
    var created = document.createElement(tag);
    created.className = selector.slice(1);
    box.appendChild(created);
    return created;
  }

  /* 1. predict ------------------------------------------------------------ */
  function initPredict(box) {
    var id = taskIdOf(box);
    var correct = box.getAttribute('data-answer');
    if (correct === null) {
      console.error('practice.js: .predict 缺少 data-answer', box);
      return;
    }
    correct = String(correct);
    var buttons = box.querySelectorAll('button[data-choice]');

    function settle(choice, fromStore) {
      var ok = choice === correct;
      buttons.forEach(function (b) {
        var c = b.getAttribute('data-choice');
        b.disabled = true;
        b.classList.remove('correct', 'wrong');
        if (c === correct) {
          b.classList.add('correct');
        }
        if (!ok && c === choice) {
          b.classList.add('wrong');
        }
      });
      setFeedback(
        box,
        ok,
        ok ? box.getAttribute('data-ok') || '对。' : box.getAttribute('data-no') || '不对，看高亮选项。'
      );
      if (!fromStore) {
        record(id, 'predict', { answer: choice, correct: ok, attempts: attemptsOf(id) + 1 });
      }
    }

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        settle(btn.getAttribute('data-choice'), false);
      });
    });

    var saved = store[id];
    if (saved && saved.kind === 'predict' && saved.answer !== null) {
      settle(String(saved.answer), true);
    }
  }

  /* 2. semantic-check ----------------------------------------------------- */
  function runCheck(scenario, text) {
    if (window.TeachChecks && typeof window.TeachChecks[scenario] === 'function') {
      return window.TeachChecks[scenario](text);
    }
    if (window.SqlMini && typeof window.SqlMini.run === 'function') {
      return window.SqlMini.run(scenario, text);
    }
    return null;
  }

  function initSemantic(box) {
    var id = taskIdOf(box);
    var scenario = box.getAttribute('data-scenario');
    var btn = box.querySelector('button[data-run]');
    var ta = box.querySelector('textarea');
    var out = box.querySelector('.result-view');
    if (!btn || !ta) {
      return;
    }
    var saved = store[id];
    if (saved && saved.kind === 'semantic' && typeof saved.answer === 'string') {
      ta.value = saved.answer;
    }
    btn.addEventListener('click', function () {
      var result = runCheck(scenario, ta.value);
      if (!result) {
        setFeedback(box, null, '本页没有加载校验器；把内容贴回对话由 Agent 判。');
        return;
      }
      if (out) {
        if (result.rows && window.SqlMini && window.SqlMini.renderRows) {
          out.textContent = window.SqlMini.renderRows(result.rows);
        } else {
          out.textContent = result.output || '';
        }
      }
      setFeedback(box, !!result.ok, result.message || (result.ok ? '通过。' : '未通过。'));
      record(id, 'semantic', { answer: ta.value, correct: !!result.ok, attempts: attemptsOf(id) + 1 });
    });
  }

  /* 3. free --------------------------------------------------------------- */
  function initFree(box) {
    var id = taskIdOf(box);
    var ta = box.querySelector('textarea');
    var btn = box.querySelector('button[data-save]');
    if (!ta || !btn) {
      return;
    }
    var saved = store[id];
    if (saved && saved.kind === 'free' && typeof saved.answer === 'string') {
      ta.value = saved.answer;
      setFeedback(box, null, '已保存 ' + hhmm(saved.at));
    }
    btn.addEventListener('click', function () {
      var r = record(id, 'free', { answer: ta.value, correct: null, attempts: attemptsOf(id) + 1 });
      setFeedback(box, null, '已保存 ' + hhmm(r.at) + '，计分以对话为准。');
    });
  }

  /* 4. drill -------------------------------------------------------------- */
  function mulberry32(seed) {
    return function () {
      seed = (seed + 0x6d2b79f5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function initDrill(box) {
    var id = taskIdOf(box);
    var name = box.getAttribute('data-drill');
    var target = parseInt(box.getAttribute('data-target'), 10) || 5;
    var gen = window.TeachDrills && window.TeachDrills[name];
    if (typeof gen !== 'function') {
      box.textContent = 'practice.js: 没有找到题库 window.TeachDrills["' + name + '"]';
      return;
    }
    var rng = mulberry32((Date.now() ^ (id.length * 2654435761)) >>> 0);
    var saved = store[id];
    var stats = (saved && saved.detail) || { streak: 0, best: 0, correct_count: 0 };
    var prompt = pick(box, '.drill-prompt', 'div');
    var choices = pick(box, '.drill-choices', 'div');
    pick(box, '.feedback', 'div');
    var statsEl = pick(box, '.drill-stats', 'p');
    var next = box.querySelector('button[data-next]');
    if (!next) {
      next = document.createElement('button');
      next.type = 'button';
      next.setAttribute('data-next', '');
      next.textContent = '下一题';
      box.appendChild(next);
    }
    var current = null;

    function renderStats() {
      statsEl.textContent =
        '连对 ' + stats.streak + ' / 目标 ' + target +
        ' · 最佳 ' + stats.best +
        ' · 总答对 ' + stats.correct_count +
        (stats.best >= target ? ' · 已达标' : '');
    }

    function answer(i, btn) {
      var ok = typeof current.answer === 'number' ? i === current.answer : current.choices[i] === current.answer;
      choices.querySelectorAll('button').forEach(function (b) {
        b.disabled = true;
      });
      btn.classList.add(ok ? 'correct' : 'wrong');
      stats.streak = ok ? stats.streak + 1 : 0;
      if (ok) {
        stats.correct_count += 1;
      }
      stats.best = Math.max(stats.best, stats.streak);
      setFeedback(box, ok, (ok ? '对。' : '不对。') + (current.explain || ''));
      record(id, 'drill', {
        answer: current.choices[i],
        correct: stats.best >= target,
        attempts: attemptsOf(id) + 1,
        detail: { streak: stats.streak, best: stats.best, correct_count: stats.correct_count }
      });
      renderStats();
      next.disabled = false;
    }

    function nextQuestion() {
      current = gen(rng);
      prompt.textContent = current.prompt;
      choices.innerHTML = '';
      current.choices.forEach(function (c, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = c;
        b.setAttribute('data-choice', String(i));
        b.addEventListener('click', function () {
          answer(i, b);
        });
        choices.appendChild(b);
      });
      setFeedback(box, null, '');
      next.disabled = true;
    }

    next.addEventListener('click', nextQuestion);
    renderStats();
    nextQuestion();
  }

  /* 5. details.answer ----------------------------------------------------- */
  function initAnswer(det) {
    var id = taskIdOf(det);
    if (store[id] && store[id].revealed) {
      det.classList.add('revealed');
    }
    det.addEventListener('toggle', function () {
      if (!det.open) {
        return;
      }
      record(id, store[id] ? store[id].kind : 'answer', { revealed: true });
      det.classList.add('revealed');
    });
  }

  /* 6. export / reset ----------------------------------------------------- */
  function exportAnswers() {
    var list = Object.keys(store).sort().map(function (k) {
      return store[k];
    });
    var json = JSON.stringify(list, null, 2);
    var out = document.querySelector('.export-out');
    if (out) {
      out.textContent = json;
    }
    return json;
  }

  function initExport(btn) {
    var bar = btn.closest('.export-bar') || btn.parentNode;
    btn.addEventListener('click', function () {
      var json = exportAnswers();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(json).then(
          function () {
            setFeedback(bar, null, '已复制到剪贴板，贴回对话即可。');
          },
          function () {
            setFeedback(bar, null, '已生成，请从下方复制。');
          }
        );
      } else {
        setFeedback(bar, null, '已生成，请从下方复制。');
      }
    });
  }

  function initReset(btn) {
    btn.addEventListener('click', function () {
      if (!window.confirm('清空本页保存的作答？')) {
        return;
      }
      store = {};
      persist();
      location.reload();
    });
  }

  /* init ------------------------------------------------------------------ */
  function init() {
    document.querySelectorAll('.predict').forEach(initPredict);
    document.querySelectorAll('.semantic-check').forEach(initSemantic);
    document.querySelectorAll('.free').forEach(initFree);
    document.querySelectorAll('.drill').forEach(initDrill);
    document.querySelectorAll('details.answer').forEach(initAnswer);
    document.querySelectorAll('[data-export-answers]').forEach(initExport);
    document.querySelectorAll('[data-reset-answers]').forEach(initReset);
    document.querySelectorAll('.feedback').forEach(function (fb) {
      fb.setAttribute('role', 'status');
      fb.setAttribute('aria-live', 'polite');
      fb.setAttribute('aria-atomic', 'true');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.TeachPractice = {
    export: exportAnswers,
    records: function () {
      return store;
    }
  };
})();
