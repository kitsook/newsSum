<template>
  <div id="app">
    <NewsPages :sources="this.newsSources"
        :subscriptions="subscriptions"
        @subscriptionChanged="subscriptionChanged"
        :showTab="showTab" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewsPages from './components/NewsPages.vue';
import Subscriptions from './services/Subscriptions';
import NewsSumApi from "./services/NewsSumApi";
import Logger from "./services/Logger";
import NewsSource from "./models/NewsSource";

@Component({
  components: {
    NewsPages,
  },
})
export default class App extends Vue {
  newsSources = [] as NewsSource[];
  subscriptions = new Set<string>();
  showTab = Subscriptions.getLastRead();

  created() {
    this.subscriptions = Subscriptions.subscriptions;

    NewsSumApi.getSources().then((sources) => {
      Logger.log("Loaded news sources");
      this.newsSources = sources;
    }).catch((resp) => {
      Logger.log("Got errors when trying to retrieve news sources");
    });
  }

  private subscriptionChanged() {
    this.subscriptions = Subscriptions.subscriptions;
  }
}
</script>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 60px 20px 20px 20px;
}

.tab-pane {
    border-left: 1px solid #ddd;
    border-right: 1px solid #ddd;
    border-bottom: 1px solid #ddd;
    border-radius: 0px 0px 8px 8px;
    padding: 10px;
}

.nav-tabs {
    margin-bottom: 0;
}

</style>
