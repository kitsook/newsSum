<template>
  <div class="tabbable">
    <b-tabs content-class="" id="news-tabs">
      <IndexTab :subscriptions="subscriptions"
          :sources="sources"
          @subscriptionChanged="subscriptionChanged"/>
      <NewsTab v-for="source of showingSources"
          :key="source.path"
          :title="source.desc"
          :srcUrl="source.path"
          :isActive="showTab === source.path" />
    </b-tabs>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import NewsTab from './NewsTab.vue';
import IndexTab from './IndexTab.vue';
import NewsSource from "../models/NewsSource";
import Logger from "../services/Logger";

@Component({
  components: {
    IndexTab,
    NewsTab,
  },
})
export default class NewsPages extends Vue {
  @Prop({ default: new Set<string>() }) subscriptions!: Set<string>;
  @Prop({ default: [] as NewsSource[] }) sources!: NewsSource[];
  @Prop({ default: ''}) showTab!: string;

  showingSources = [] as NewsSource[];

  @Watch('subscriptions')
  onSubScriptionsChanged(newSubscriptions: Set<string>, oldSubscriptions: Set<string>) {
    this.refreshShowingSources(newSubscriptions, this.sources);
  }

  @Watch('sources')
  onSourcesChanged(newSources: NewsSource[], oldSources: NewsSource[]) {
    this.refreshShowingSources(this.subscriptions, newSources);
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
</style>