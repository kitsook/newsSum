<template>
  <div class="tabbable">
    <b-tabs content-class="" id="news-tabs" v-model="showTabIndex" @activate-tab="tabChanged" ref="newsTabs" lazy>
      <IndexTab :subscriptions="subscriptions"
          :sources="sources"
          @subscriptionChanged="subscriptionChanged"/>
      <NewsTab v-for="source of showingSources"
          :key="source.path"
          :title="source.desc"
          :srcUrl="source.path"
          :icon="source.icon"
          :iconDict="iconDict"
          :isActive="showTab === source.path"
          :isSuggestionAvail="isSuggestionAvail" />
    </b-tabs>
    <div
        class="footer"
        v-if="appVersion"
    >
        Version: {{ appVersion }}
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import NewsTab from './NewsTab.vue';
import IndexTab from './IndexTab.vue';
import NewsSource from "../models/NewsSource";
import Subscriptions from '../services/Subscriptions';
import { BvEvent } from 'bootstrap-vue';

@Component({
  components: {
    IndexTab,
    NewsTab,
  },
})
export default class NewsPages extends Vue {
  @Prop({ default: new Set<string>() }) subscriptions!: Set<string>;
  @Prop({ default: [] as NewsSource[] }) sources!: NewsSource[];
  @Prop({ default: {}}) iconDict!: Record<string, string> ;
  @Prop({ default: "" }) appVersion!: string;
  @Prop({ default: ''}) showTab!: string;
  @Prop({ default: false }) isSuggestionAvail!: boolean;

  showingSources = [] as NewsSource[];
  showTabIndex = 0;
  firstTabChange = true;

  @Watch('subscriptions')
  onSubScriptionsChanged(newSubscriptions: Set<string>, oldSubscriptions: Set<string>) {
    this.refreshShowingSources(newSubscriptions, this.sources);
  }

  @Watch('sources')
  onSourcesChanged(newSources: NewsSource[], oldSources: NewsSource[]) {
    this.refreshShowingSources(this.subscriptions, newSources);
  }

  private tabChanged(newTabIndex: number, prevTabIndex: number, bvEvent: BvEvent) {
    if (this.firstTabChange) {
      this.firstTabChange = false;
      const theTabBar = this.$refs.newsTabs as Vue;
      const theActiveTab = theTabBar.$el.querySelector(`a[aria-posinset="${newTabIndex+1}"]`) as Element;
      if (theActiveTab) {
        theActiveTab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    } else if (newTabIndex > 0 && this.showingSources.length > newTabIndex-1) {
        Subscriptions.setLastRead(this.showingSources[newTabIndex-1].path);
    }
  }

  private subscriptionChanged() {
    this.$emit('subscriptionChanged');
  }

  private refreshShowingSources(subscriptions: Set<string>, sources: NewsSource[]) {
    this.showingSources = new Array<NewsSource>();

    sources.forEach(src => {
      if (subscriptions.has(src.path)) {
        this.showingSources.push(src);
      }
    });
  }


}
</script>

<style>
.tabbable .nav-tabs {
   overflow-x: auto;
   overflow-y: hidden;
   flex-wrap: nowrap;
}
.tabbable .nav-tabs .nav-link {
  white-space: nowrap;
}
.footer {
    font-size: 10px;
}
</style>