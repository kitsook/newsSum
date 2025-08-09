<template>
  <!-- <b-tab :title="title" :active.sync="tabIsActive"> -->
    <Loading v-if="newsArticles.length == 0" />
    <ArticleList :articles="newsArticles"
      :isSuggestionAvail="isSuggestionAvail"
      :iconDict="iconDict" />
  <!-- </b-tab> -->
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue';
import NewsSumApi from "../services/NewsSumApi";
import Logger from "../services/Logger";
import NewsArticle from "../models/NewsArticle";
import ArticleList from "../components/ArticleList.vue";
import Loading from "../components/LoadingSpinner.vue";

const props = defineProps<{
  srcUrl: string,
  iconDict: Record<string, string>,
  isActive: boolean,
  isSuggestionAvail: boolean
}>();

const newsArticles = ref<NewsArticle[]>([]);
const tabIsActive = ref(false);

onMounted(() => {
  NewsSumApi.getArticles(props.srcUrl).then((articles) => {
    newsArticles.value = articles;
  }).catch(resp => {
    Logger.log("Got errors when trying to retrieve articles: " + resp);
  });
  tabIsActive.value = props.isActive;
});
</script>