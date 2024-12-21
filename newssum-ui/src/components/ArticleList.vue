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
          <b-col cols="auto" v-b-toggle="'accordion-' + index" @click="toggle_article(index, article)" v-if="isSuggestionAvail">
            <b-icon icon="chevron-down" class="when-open"></b-icon>
            <b-icon icon="chevron-right" class="when-closed"></b-icon>
          </b-col>
          <b-col>
            <a :href="article.url"
              :class="index%2 == 0? 'list-group-item-secondary' : 'list-group-item-light'"
              class="list-group-item list-group-item-action" target="_blank">
              <div class="text-primary">{{ article.title? article.title.replace(re, '') : '' }}</div>
              <div>{{ article.abstract? article.abstract.replace(re, '') : '' }}</div>
            </a>
          </b-col>
        </b-row>
        <b-row v-if="article.url">
          <b-col cols="auto"></b-col>
          <b-col>
            <b-collapse :id="'accordion-' + index">
              <b-card class="border-0">
                <Loading v-if="article.suggestions === undefined"/>
                <div v-if="article.suggestions && article.suggestions.length == 0">No suggestions</div>
                <ul>
                  <li v-for="(suggestion, suggestion_idx) in article.suggestions" :key="suggestion_idx">
                    <a :href="suggestion.url" target="_blank">
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

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import NewsArticle from "../models/NewsArticle";
import SuggestionsApi from "../services/SuggestionsApi";
import Loading from "../components/Loading.vue";

@Component({
  components: {
    Loading,
  },
})
export default class ArticleList extends Vue {
  @Prop({ default: [] as NewsArticle[] }) articles!: NewsArticle[];
  @Prop({ default: false}) isSuggestionAvail!: boolean;

  re = /(<([^>]+)>)/g

  toggle_article(index: number, article: NewsArticle) {
    if (article.suggestions === undefined) {
      SuggestionsApi.getSuggestions(article.title).then((suggestions) => {
        Vue.set(article, "suggestions", suggestions);
      });
    }
  }
}
</script>

<style scoped>
  .collapsed > .when-open,
  .not-collapsed > .when-closed {
    display: none;
  }
</style>