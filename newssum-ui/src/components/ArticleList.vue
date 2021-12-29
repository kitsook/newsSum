<template>
  <div class="list-group">
    <a v-for="(article, index) in articles" :key="index" :href="article.url"
        :class="article.url? (index%2 == 0? 'list-group-item-secondary' : 'list-group-item-light') : 'active'"
        class="list-group-item list-group-item-action" target="_blank">
      <div :class="article.url? 'text-primary' : ''">{{ article.title }}</div>
      <div>{{ article.abstract? article.abstract.replace(re, '') : '' }}</div>
    </a>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import NewsArticle from "../models/NewsArticle";
import Loading from "../components/Loading.vue";

@Component({
  components: {
    Loading,
  },
})
export default class ArticleList extends Vue {
  @Prop({ default: [] as NewsArticle[] }) articles!: NewsArticle[];

  re = /(<([^>]+)>)/g
}
</script>

<style>
</style>