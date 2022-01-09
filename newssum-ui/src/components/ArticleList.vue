<template>
  <div class="list-group">
    <a v-for="(article, index) in articles" :key="index" :href="article.url"
        :class="article.url? (index%2 == 0? 'list-group-item-secondary' : 'list-group-item-light') : 'active'"
        class="list-group-item list-group-item-action" target="_blank">
      <div :class="article.url? 'text-primary' : ''">{{ article.title? article.title.replace(re, '') : '' }}</div>
      <div>{{ article.abstract? article.abstract.replace(re, '') : '' }}</div>
    </a>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import NewsArticle from "../models/NewsArticle";

@Component
export default class ArticleList extends Vue {
  @Prop({ default: [] as NewsArticle[] }) articles!: NewsArticle[];

  re = /(<([^>]+)>)/g
}
</script>

<style>
</style>