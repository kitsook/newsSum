<template>
  <ul class="list-group" id="news-sources">
    <li v-for="source in sources" :key="source.path" class="list-group-item border-0">
      <input class="form-check-input me-1" type="checkbox"
          :value="source.path"
          v-model="checkedSources"
          @change="changeSubscription()">
      <img alt="" :src="source.icon" v-if="source.icon" width="16" height="16" /><img alt="" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" v-else height="16" width="16" />&nbsp;{{ source.desc }}
    </li>
  </ul>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue';
import NewsSource from "../models/NewsSource";
import Subscriptions from "../services/Subscriptions";

const props = defineProps<{
  subscriptions: Set<string>,
  sources: NewsSource[]
}>();

const checkedSources = ref<string[]>([]);
const emit = defineEmits(['subscriptionChanged']);

function changeSubscription() {
  Subscriptions.updateSubscription(checkedSources.value);
  emit('subscriptionChanged');
}

onMounted(() => {
  checkedSources.value = Array.from(props.subscriptions);
});

watch(() => props.subscriptions, (newSubscriptions) => {
  checkedSources.value = Array.from(newSubscriptions);
});
</script>

<style>
#news-sources {
  margin: 10px;
}
</style>
