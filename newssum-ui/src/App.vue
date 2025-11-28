<template>
  <div id="app">
    <div class="position-absolute top-0 start-0 p-1">
      <button class="btn btn-link" @click="toggleTheme" :aria-label="theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'">
        <BIconMoon v-if="theme === 'light'" class="fs-7" />
        <BIconSun v-else class="fs-7" />
      </button>
    </div>
    <NewsPages :sources="newsSources"
        :iconDict="iconDict"
        :subscriptions="subscriptions"
        :appVersion="appVersion"
        @subscriptionChanged="subscriptionChanged"
        :isSuggestionAvail="isSuggestionAvail"
        :showTab="showTab" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import NewsPages from './components/NewsPages.vue';
import Subscriptions from './services/Subscriptions';
import NewsSumApi from "./services/NewsSumApi";
import SuggestionsApi from "./services/SuggestionsApi";
import Logger from "./services/Logger";
import NewsSource from "./models/NewsSource";
import { BIconMoon, BIconSun } from 'bootstrap-icons-vue';

const newsSources = ref<NewsSource[]>([]);
const iconDict = ref<Record<string, string>>({});
const subscriptions = ref(new Set<string>());
const appVersion = ref("");
const showTab = ref("");
const isSuggestionAvail = ref(false);
const theme = ref('light');

showTab.value = Subscriptions.getLastRead();
subscriptions.value = Subscriptions.subscriptions;

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-bs-theme', theme.value);
  localStorage.setItem('theme', theme.value);
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    theme.value = savedTheme;
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    theme.value = 'dark';
  }
  document.documentElement.setAttribute('data-bs-theme', theme.value);

  SuggestionsApi.isAvailable().then((isAvailable) => {
    isSuggestionAvail.value = isAvailable;
  });

  NewsSumApi.getSources().then((sources) => {
    Logger.log("Loaded news sources");
    newsSources.value = sources;

    sources.reduce((acc, source) => {
      acc[source.path] = source.icon;
      return acc;
    }, iconDict.value);
  }).catch((resp) => {
    Logger.log("Got errors when trying to retrieve news sources: " + resp);
  });

  NewsSumApi.getAppProperties().then((props) => {
    appVersion.value = props.get("GAE_VERSION")? props.get("GAE_VERSION")! : "";
  });
});

function subscriptionChanged() {
  subscriptions.value = Subscriptions.subscriptions;
}
</script>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 40px 20px 20px 20px;
}

[data-bs-theme="dark"] #app {
  color: var(--bs-white);
}

.tab-pane {
    border-left: 1px solid var(--bs-border-color);
    border-right: 1px solid var(--bs-border-color);
    border-bottom: 1px solid var(--bs-border-color);
    border-radius: 0px 0px 8px 8px;
    padding: 10px;
}

.nav-tabs {
    margin-bottom: 0;
}

</style>