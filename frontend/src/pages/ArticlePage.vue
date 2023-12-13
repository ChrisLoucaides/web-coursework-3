<script lang="ts">
import {defineComponent} from 'vue'
import Article from "../utils/models/Article.ts";
import API from "../utils/api.ts";
import Pill from "../components/Pill.vue";
import ArticleCommentView from "../components/ArticleCommentView.vue";
import ArticleComment from "../utils/models/ArticleComment.ts";
import PostCommentView from "@/components/PostCommentView.vue";

export default defineComponent({
  name: "ArticlePage",
  components: {PostCommentView, ArticleCommentView, Pill},
  data() {
    return {
      isLoading: true,
      article: null as Article | null,
      error: null as string | null,
      comments: [] as ArticleComment[]
    }
  },
  async mounted() {

    this.isLoading = true;
    const articleId: number = Number.parseInt(this.$route.params.id as string);

    const article = await API.fetchArticle(articleId);
    if (article) {
      this.article = article;
      this.isLoading = false;

      const comments = await API.fetchCommentsForArticle(articleId);
      this.comments = comments;
    } else {
      this.isLoading = false;
      this.error = "Failed to retrieve article. It may have been deleted."
    }
  }
})
</script>

<template>
  <div class="loading" v-if="isLoading"></div>
  <div class="error" v-if="error"></div>
  <div class="article" v-if="!isLoading && !error && article">
    <h3>{{ article.title_text }}</h3>
    <div class="pills">
      <Pill :text-content="article.category"/>
      <Pill left-icon="bi bi-chat" :text-content="article.comment_count.toString()"/>
    </div>

    <div class="content">
      <span>{{ article.content_text }}</span>
    </div>

    <div class="comments">
      <hr>
      <h5>Comments:</h5>
      <PostCommentView />
      <ArticleCommentView v-for="comment in comments" :key="comment.id" :comment="comment"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
.article {

  h3 {
    font-weight: bold;
  }

  .pills {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
  }

  .content {
    margin-top: 1rem;
  }

  .comments {
    margin-top: 1rem;
  }
}
</style>