<template>
  <div>
    <b-tabs content-class="" id="news-tabs">
      <IndexTab :subscriptions="subscriptions" :sources="sources"/>
      <NewsTab v-for="source of showingSources" :key="source.desc" :title="source.desc" :srcUrl="source.path"/>
    </b-tabs>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import NewsTab from './NewsTab.vue';
import IndexTab from './IndexTab.vue';
import NewsSource from "../models/NewsSource";

@Component({
  components: {
    IndexTab,
    NewsTab,
  },
})
export default class NewsPages extends Vue {
  @Prop({ default: new Set<string>() }) subscriptions!: Set<string>;
  @Prop({ default: [] as NewsSource[] }) sources!: NewsSource[];

  showingSources = [] as NewsSource[];

  @Watch('sources')
  onSourcesChanged(newSources: NewsSource[], oldSources: NewsSource[]) {
    this.showingSources = new Array<NewsSource>();
    newSources.forEach(src => {
      if (this.subscriptions.has(src.path)) {
        this.showingSources.push(src);
      }
    });
  }
}
</script>