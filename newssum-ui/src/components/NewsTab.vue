<template>
  <b-tab :title="title">
    <p>Going to retrieve data from {{ srcUrl }}</p>
  </b-tab>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class NewsTab extends Vue {
  @Prop() private title!: string;
  @Prop() private srcUrl!: string;
}
</script>