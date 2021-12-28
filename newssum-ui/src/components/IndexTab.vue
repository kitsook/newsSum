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
            :checked="subscriptions.has(source.path)">
        {{ source.desc }}
      </li>
    </ul>
  </b-tab>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import NewsSource from "../models/NewsSource";
import Loading from "../components/Loading.vue";
import Logger from "../services/Logger";

@Component({
  components: {
    Loading,
  },
})
export default class IndexTab extends Vue {
  @Prop({ default: new Set<string>() }) subscriptions!: Set<string>;
  @Prop({ default: [] as NewsSource[] }) sources!: NewsSource[];

  created() {
  }

  @Watch('sources')
  onSourcesChanged(value: NewsSource[], oldValue: NewsSource) {
  }

  @Watch('subscriptions')
  onSubscriptionsChanged(value: { [name: string]: number; }, oldValue: { [name: string]: number; }) {
  }
}
</script>

<style>
#news-sources {
  margin: 10px;
}
</style>