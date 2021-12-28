<template>
  <div class="list-group">
    <a v-for="(article, index) in articles" :key="index" :href="article.url"
        :class="article.url? (index%2 == 0? 'list-group-item-dark' : 'list-group-item-light') : 'active'"
        class="list-group-item list-group-item-action" target="_blank">
      <h6>{{ article.title }}</h6>
      <small>{{ article.abstract? article.abstract.replace(re, '') : '' }}</small>
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