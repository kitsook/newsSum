<template>
  <b-tab :title="title" :active.sync="tabIsActive">
    <template v-slot:title v-if="icon">
      <div>
        <img :src="icon" width="16" height="16" />
        <span>&nbsp;{{ title }}</span>
      </div>
    </template>
    <Loading v-if="newsArticles.length == 0" />
    <ArticleList :articles="newsArticles"
      :isSuggestionAvail="isSuggestionAvail"
      :iconDict="iconDict" />
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
  @Prop({ default: "" }) title!: string;
  @Prop({ default: "" }) srcUrl!: string;
  @Prop({ default: null }) icon!: string;
  @Prop({ default: {}}) iconDict!: Record<string, string>;
  @Prop({ default: false }) isActive!: boolean;
  @Prop({ default: false }) isSuggestionAvail!: boolean;

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