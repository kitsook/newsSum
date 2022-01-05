<template>
  <b-tab :title="title" :active.sync="tabIsActive">
    <Loading v-if="newsArticles.length == 0" />
    <ArticleList :articles="newsArticles" />
  </b-tab>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import NewsSumApi from "../services/NewsSumApi";
import Logger from "../services/Logger";
import NewsArticle from "../models/NewsArticle";
import Loading from "../components/Loading.vue";
import ArticleList from "../components/ArticleList.vue";

@Component({
  components: {
    ArticleList,
    Loading,
  },
})
export default class NewsTab extends Vue {
  @Prop() title!: string;
  @Prop() srcUrl!: string;
  @Prop({ default: false }) isActive!: boolean;

  newsArticles = [] as NewsArticle[];
  tabIsActive = false;

  created() {
    NewsSumApi.getArticles(this.srcUrl).then((articles) => {
      this.newsArticles = articles;
    }).catch(resp => {
      Logger.log("Got errors when trying to retrieve articles");
    });
  }

  mounted() {
    this.tabIsActive = this.isActive;
  }
}
</script>