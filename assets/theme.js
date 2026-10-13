/**
 * Light/dark theme toggle for static Teach lesson pages.
 */
(function () {
  'use strict';

  var root = document.documentElement;
  var storageKey = 'teach-theme';
  var colorScheme = window.matchMedia
    ? window.matchMedia('(prefers-color-scheme: dark)')
    : null;

  function readPreference() {
    try {
      var value = window.localStorage.getItem(storageKey);
      return value === 'light' || value === 'dark' ? value : null;
    } catch (error) {
      return null;
    }
  }

  function savePreference(value) {
    try {
      window.localStorage.setItem(storageKey, value);
    } catch (error) {
      // Theme switching still works for this page when storage is unavailable.
    }
  }

  function currentTheme() {
    var explicitTheme = root.getAttribute('data-theme');
    if (explicitTheme === 'light' || explicitTheme === 'dark') {
      return explicitTheme;
    }
    return colorScheme && colorScheme.matches ? 'dark' : 'light';
  }

  function updateButton(button) {
    var isDark = currentTheme() === 'dark';
    var targetName = isDark ? '浅色' : '深色';
    var icon = button.querySelector('.theme-toggle__icon');
    var text = button.querySelector('.theme-toggle__text');

    button.setAttribute('aria-label', '切换到' + targetName + '模式');
    button.setAttribute('title', '切换到' + targetName + '模式');
    if (icon) {
      icon.textContent = isDark ? '☀\uFE0E' : '☾';
    }
    if (text) {
      text.textContent = targetName;
    }
  }

  function announce(status, theme) {
    status.textContent = '';
    window.setTimeout(function () {
      status.textContent = '已切换到' + (theme === 'dark' ? '深色' : '浅色') + '模式';
    }, 50);
  }

  function mountToggle() {
    if (document.querySelector('[data-theme-toggle]')) {
      return;
    }

    var button = document.createElement('button');
    var icon = document.createElement('span');
    var text = document.createElement('span');
    var status = document.createElement('div');

    button.type = 'button';
    button.className = 'theme-toggle';
    button.setAttribute('data-theme-toggle', '');

    icon.className = 'theme-toggle__icon';
    icon.setAttribute('aria-hidden', 'true');
    text.className = 'theme-toggle__text';

    status.className = 'theme-status sr-only';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.setAttribute('aria-atomic', 'true');

    button.appendChild(icon);
    button.appendChild(text);
    document.body.appendChild(button);
    document.body.appendChild(status);
    updateButton(button);

    button.addEventListener('click', function () {
      var nextTheme = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', nextTheme);
      savePreference(nextTheme);
      updateButton(button);
      announce(status, nextTheme);
    });

    var followSystemChange = function () {
      // A manual choice intentionally overrides later system-theme changes.
      if (!root.hasAttribute('data-theme')) {
        updateButton(button);
      }
    };
    if (colorScheme) {
      if (colorScheme.addEventListener) {
        colorScheme.addEventListener('change', followSystemChange);
      } else if (colorScheme.addListener) {
        colorScheme.addListener(followSystemChange);
      }
    }

    window.requestAnimationFrame(function () {
      root.classList.add('theme-ready');
    });
  }

  var savedTheme = readPreference();
  if (savedTheme) {
    root.setAttribute('data-theme', savedTheme);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountToggle);
  } else {
    mountToggle();
  }
})();
