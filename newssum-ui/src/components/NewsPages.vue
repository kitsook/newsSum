<template>
  <div class="tabbable">
    <b-tabs content-class="" id="news-tabs" v-model="showTabIndex" @activate-tab="tabChanged" ref="newsTabs" lazy>
      <b-tab>
        <template #title>
          <BIconCardChecklist/>
        </template>
        <IndexTab :subscriptions="subscriptions"
          :sources="sources"
          @subscriptionChanged="subscriptionChanged"/>
      </b-tab>
      <b-tab v-for="source of showingSources" :key="source.path" :title="source.desc">
        <template v-slot:title v-if="icon">
          <div>
            <img :src="icon" width="16" height="16" alt="" />
            <span>&nbsp;{{ title }}</span>
          </div>
        </template>

        <NewsTab
          :srcUrl="source.path"
          :icon="source.icon"
          :iconDict="iconDict"
          :isActive="showTab === source.path"
          :isSuggestionAvail="isSuggestionAvail" />
      </b-tab>

    </b-tabs>
    <div
        class="footer"
        v-if="appVersion">
      Version: {{ appVersion }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';
import NewsTab from './NewsTab.vue';
import IndexTab from './IndexTab.vue';
import NewsSource from "../models/NewsSource";
import Subscriptions from '../services/Subscriptions';
import { BvEvent } from 'bootstrap-vue-3';

const props = defineProps<{
  subscriptions: Set<string>,
  sources: NewsSource[],
  iconDict: Record<string, string>,
  appVersion: string,
  showTab: string | undefined,
  isSuggestionAvail: boolean
}>();

const showingSources = ref<NewsSource[]>([]);
const showTabIndex = ref(0);
const firstTabChange = ref(true);
const newsTabs = ref(null);

const emit = defineEmits(['subscriptionChanged']);

watch(() => props.subscriptions, (newSubscriptions) => {
  refreshShowingSources(newSubscriptions, props.sources);
});

watch(() => props.sources, (newSources) => {
  refreshShowingSources(props.subscriptions, newSources);
});

function tabChanged(newTabIndex: number, prevTabIndex: number, bvEvent: BvEvent) {
  if (!newsTabs.value) { // not mounted yet
    return;
  }

  if (firstTabChange.value) {
    firstTabChange.value = false;
    const theTabBar = newsTabs.value as any;
    const theActiveTab = theTabBar?.$el.querySelector(`a[aria-posinset="${newTabIndex+1}"]`) as Element;
    if (theActiveTab) {
      theActiveTab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  } else if (newTabIndex > 0 && showingSources.value.length > newTabIndex-1) {
      Subscriptions.setLastRead(showingSources.value[newTabIndex-1].path);
  }
}

function subscriptionChanged() {
  emit('subscriptionChanged');
}

function refreshShowingSources(subscriptions: Set<string>, sources: NewsSource[]) {
  showingSources.value = new Array<NewsSource>();

  sources.forEach(src => {
    if (subscriptions.has(src.path)) {
      showingSources.value.push(src);
    }
  });
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