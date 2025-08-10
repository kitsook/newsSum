<template>
  <div class="tabbable">
    <BTabs id="news-tabs" v-model:index="showTabIndex" @activate-tab="tabChanged" ref="newsTabs">
      <BTab>
        <template #title>
          <BIconCardChecklist/>
        </template>
        <IndexTab :subscriptions="subscriptions"
          :sources="sources"
          @subscriptionChanged="subscriptionChanged"/>
      </BTab>
      <BTab v-for="source of showingSources" :key="source.path" :title="source.desc" :active="showTab === source.path">
        <template v-slot:title v-if="source.icon">
          <div>
            <img :src="source.icon" width="16" height="16" alt="" />
            <span>&nbsp;{{ source.desc }}</span>
          </div>
        </template>
        <NewsTab
          :srcUrl="source.path"
          :iconDict="iconDict"
          :isSuggestionAvail="isSuggestionAvail" />
      </BTab>

    </BTabs>
    <div
        class="footer"
        v-if="appVersion">
      Version: {{ appVersion }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';
import { BIconCardChecklist } from "bootstrap-icons-vue";
import NewsTab from './NewsTab.vue';
import IndexTab from './IndexTab.vue';
import NewsSource from "../models/NewsSource";
import Subscriptions from '../services/Subscriptions';

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
const newsTabs = ref(null);

const emit = defineEmits(['subscriptionChanged']);

watch(() => props.subscriptions, (newSubscriptions) => {
  refreshShowingSources(newSubscriptions, props.sources);
});

watch(() => props.sources, (newSources) => {
  refreshShowingSources(props.subscriptions, newSources);
});

function tabChanged(newTabId: string, prevTabId: string, newTabIndex: number) {
  if (newTabIndex > 0 && showingSources.value.length > newTabIndex-1) {
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