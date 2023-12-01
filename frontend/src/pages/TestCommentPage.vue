<template>
  <div>
    <div class="testCommentContainer">
      <label>Fetch comments for article id:</label>
      <input type="number" v-bind="articleId">
      <button class="btn btn-primary" @click="fetchForArticle">Load</button>


    </div>
    <div class="comments">
      <ArticleCommentView v-if="loading" :is-skeleton="true"/>
      <ArticleCommentView v-for="comment in comments" :key="comment.id" :comment="comment"/>
    </div>
  </div>
</template>

<style scoped>
.testCommentContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style>

<script lang="ts">
import {defineComponent} from 'vue'
import ArticleCommentView from "../components/ArticleCommentView.vue";
import ArticleComment from "../utils/models/ArticleComment.ts";
import API from "../utils/api.ts";

export default defineComponent({
  name: "TestCommentPage.vue",
  components: {ArticleCommentView},
  data() {
    return {
      comments: [] as ArticleComment[],
      articleId: 1,
      loading: false,
    }
  },
  methods: {
    async fetchForArticle() {
      this.loading = true;
      this.comments = [];
      if (this.articleId) {
        setTimeout(async () => {
          this.comments = await API.fetchCommentsForArticle(this.articleId);
          this.loading = false;
        }, 1500);
      } else {
        this.comments = [];
      }
    }
  }
})
</script>