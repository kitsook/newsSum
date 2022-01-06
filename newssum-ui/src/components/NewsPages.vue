<template>
  <div class="tabbable" ref="tabheaders">
    <b-tabs content-class="" id="news-tabs" v-model="showTabIndex" @activate-tab="tabChanged" lazy>
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
import Subscriptions from '../services/Subscriptions';
import Logger from "../services/Logger";
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
  @Prop({ default: ''}) showTab!: string;

  showingSources = [] as NewsSource[];
  showTabIndex = 0;
  firstTabChange = true;

  $refs!: {
    tabheaders: HTMLElement
  }

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
      if (newTabIndex > 0 && this.showingSources.length > newTabIndex) {
        this.scrollToActiveTab(this.showingSources[newTabIndex].desc);
      }
    } else {
      if (newTabIndex > 0 && this.showingSources.length > newTabIndex-1) {
        Subscriptions.setLastRead(this.showingSources[newTabIndex-1].path);
      }
    }
  }

  private scrollToActiveTab(tabText: string) {
    const headers = this.$refs.tabheaders.querySelector(".nav-tabs");
    let activeTab: Element | undefined = undefined;

    const links = this.$refs.tabheaders.getElementsByClassName('nav-link');
    for (let i = 0; i < links.length; i++) {
      if (links[i].innerHTML === tabText) {
        activeTab = links[i];
      }
    }

    // TODO find a more efficient and accurate way to scroll to the active tab
    if (headers && activeTab) {
      let maxScrollLeft = headers.scrollWidth - headers.clientWidth;
      headers.scrollLeft = 0;
      while(!this.isInViewport(activeTab) && headers.scrollLeft < maxScrollLeft) {
        headers.scrollLeft += maxScrollLeft / 5;
      }
    }
  }

  private isInViewport(element: Element) {
    const rect = element.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
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