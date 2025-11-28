<template>
  <div class="list-group">
    <div v-for="(article, index) in articles" :key="index">
      <b-container fluid>
        <b-row v-if="!(article.url)">
          <b-col cols="12">
            <div class="active list-group-item list-group-item-action">
              {{ article.title? article.title.replace(re, '') : '' }}
            </div>
          </b-col>
        </b-row>
        <b-row align-v="center" v-if="article.url">
          <b-col cols="auto" v-b-toggle="`accordion-${srcUrl}-${index}`" @click="toggle_article(index, article)" v-if="isSuggestionAvail">
            <BIconChevronDown class="when-open"/>
            <BIconChevronRight class="when-closed"/>
          </b-col>
          <b-col>
            <a :href="article.url"
              :class="index%2 == 0? 'list-group-item-secondary' : 'list-group-item-light'"
              class="list-group-item list-group-item-action" target="_blank">
              <div class="article-title">{{ article.title? article.title.replace(re, '') : '' }}</div>
              <div>{{ article.abstract? article.abstract.replace(re, '') : '' }}</div>
            </a>
          </b-col>
        </b-row>
        <b-row v-if="article.url">
          <b-col cols="auto"></b-col>
          <b-col>
            <b-collapse :id="'accordion-' + srcUrl + '-' + index">
              <b-card class="border-0">
                <LoadingSpinner v-if="article.suggestions === undefined"/>
                <div v-if="article.suggestions && article.suggestions.length == 0">No suggestions</div>
                <ul style="list-style: none;">
                  <li v-for="(suggestion, suggestion_idx) in article.suggestions" :key="suggestion_idx">
                    <a :href="suggestion.url" target="_blank">
                      <img v-if="iconDict[suggestion.source_id]" :src="iconDict[suggestion.source_id]" height=15 :alt="suggestion.source_id" />
                      {{ suggestion.title }}
                    </a>
                  </li>
                </ul>
              </b-card>
            </b-collapse>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import NewsArticle from "../models/NewsArticle";
import SuggestionsApi from "../services/SuggestionsApi";
import LoadingSpinner from "../components/LoadingSpinner.vue";
import { BIconChevronDown, BIconChevronRight } from "bootstrap-icons-vue";


defineProps<{
  srcUrl: string,
  articles: NewsArticle[],
  isSuggestionAvail: boolean,
  iconDict: Record<string, string>
}>();

const re = /(<([^>]+)>)/g;

function toggle_article(index: number, article: NewsArticle) {
  if (article.suggestions === undefined) {
    SuggestionsApi.getSuggestions(article.title).then((suggestions) => {
      article.suggestions = suggestions;
    });
  }
}

</script>

<style scoped>
  [aria-expanded="true"] > .when-closed {
    display: none;
  }
  [aria-expanded="false"] > .when-closed {
    display: inline;
  }
  [aria-expanded="true"] > .when-open {
    display: inline;
  }
  [aria-expanded="false"] > .when-open {
    display: none;
  }

  :global([data-bs-theme="dark"]) .list-group-item-light {
    background-color: var(--bs-gray-900);
    color: var(--bs-body-color);
    border-color: var(--bs-border-color);
  }
  :global([data-bs-theme="dark"]) .list-group-item-secondary {
    background-color: var(--bs-gray-800);
    color: var(--bs-body-color);
    border-color: var(--bs-border-color);
  }

  .article-title {
    color: var(--bs-primary);
  }

  [data-bs-theme="dark"] .article-title,
  [data-bs-theme="dark"] a {
    color: white !important;
  }
</style>
