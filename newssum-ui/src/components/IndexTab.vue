<template>
  <b-tab>
    <template #title>
      <b-icon-list-check></b-icon-list-check>
    </template>
    <Loading v-if="sources.length == 0"/>
    <ul class="list-group" id="news-sources">
      <li v-for="source in this.sources" :key="source.path" class="list-group-item border-0">
        <input class="form-check-input me-1" type="checkbox"
            :value="source.path"
            v-model="checkedSources"
            @change="changeSubscription()">
        <img :src="source.icon" v-if="source.icon" width="16" height="16" /><img src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" v-else height="16" width="16" />&nbsp;{{ source.desc }}
      </li>
    </ul>
  </b-tab>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import NewsSource from "../models/NewsSource";
import Loading from "../components/Loading.vue";
import Subscriptions from "../services/Subscriptions";

@Component({
  components: {
    Loading,
  },
})
export default class IndexTab extends Vue {
  @Prop({ default: new Set<string>() }) subscriptions!: Set<string>;
  @Prop({ default: [] as NewsSource[] }) sources!: NewsSource[];

  checkedSources = [] as string[];

  changeSubscription() {
    Subscriptions.updateSubscription(this.checkedSources);
    this.$emit('subscriptionChanged');
  }

  created() {
    this.checkedSources = Array.from(this.subscriptions);
  }

  @Watch('subscriptions')
  onSubscriptionsChanged(value: { [name: string]: number; }, oldValue: { [name: string]: number; }) {
    this.checkedSources = Array.from(this.subscriptions);
  }
}
</script>

<style>
#news-sources {
  margin: 10px;
}
</style>