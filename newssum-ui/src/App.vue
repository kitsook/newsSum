<template>
  <div id="app">
    <NewsPages :sources="this.newsSources"
        :subscriptions="subscriptions"
        :appVersion="appVersion"
        @subscriptionChanged="subscriptionChanged"
        :isSuggestionAvail="this.isSuggestionAvail"
        :showTab="showTab" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewsPages from './components/NewsPages.vue';
import Subscriptions from './services/Subscriptions';
import NewsSumApi from "./services/NewsSumApi";
import SuggestionsApi from "./services/SuggestionsApi";
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
  appVersion = "";
  showTab = Subscriptions.getLastRead();
  isSuggestionAvail = false;

  created() {
    this.subscriptions = Subscriptions.subscriptions;

    SuggestionsApi.isAvailable().then((isAvailable) => {
      this.isSuggestionAvail = isAvailable;
    });

    NewsSumApi.getSources().then((sources) => {
      Logger.log("Loaded news sources");
      this.newsSources = sources;
    }).catch((resp) => {
      Logger.log("Got errors when trying to retrieve news sources");
    });

    NewsSumApi.getAppProperties().then((props) => {
      this.appVersion = props.get("GAE_VERSION")? props.get("GAE_VERSION")! : "";
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
  margin: 40px 20px 20px 20px;
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
