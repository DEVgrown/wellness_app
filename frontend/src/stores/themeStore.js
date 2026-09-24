import { ref, computed } from 'vue';

const THEME_STORAGE_KEY = 'karina_theme';

const currentTheme = ref('light');

// Initialize from storage or system preference
const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
if (storedTheme) {
  currentTheme.value = storedTheme;
} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  currentTheme.value = 'dark';
}

function applyTheme(theme) {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  localStorage.setItem(THEME_STORAGE_KEY, theme);
}

// Initial application
applyTheme(currentTheme.value);

export const useThemeStore = () => {
  const isDark = computed(() => currentTheme.value === 'dark');

  function toggleTheme() {
    currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
    applyTheme(currentTheme.value);
  }

  function setTheme(theme) {
    if (theme === 'dark' || theme === 'light') {
      currentTheme.value = theme;
      applyTheme(theme);
    }
  }

  return {
    isDark,
    currentTheme,
    toggleTheme,
    setTheme
  };
};
