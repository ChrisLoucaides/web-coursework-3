<script lang="ts">
import {defineComponent} from 'vue'
import Article from "../utils/models/Article.ts";
import API from "../utils/api.ts";
import Pill from "../components/Pill.vue";
import ArticleCommentView from "../components/ArticleCommentView.vue";
import ArticleComment, {UpdateComment} from "../utils/models/ArticleComment.ts";
import PostCommentView from "../components/PostCommentView.vue";
import {useAuthStore} from "../../auth.ts";

export default defineComponent({
  name: "ArticlePage",
  components: {PostCommentView, ArticleCommentView, Pill},
  setup() {
    const authStore = useAuthStore()

    return {authStore}
  },
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
  },
  methods: {
    async postComment(comment: UpdateComment) {
      const userId = this.authStore.user?.id;
      const articleId = this.article?.id;

      if (!userId || !articleId) {
        console.log(this.authStore.user, articleId);
        return;
      }


      const isEditing: boolean = !!comment.id;
      let newComment: ArticleComment;
      if (isEditing) {
        newComment = await API.editComment(articleId, comment.id ?? 0, comment.text);
      } else {
        const dto: ArticleComment = {
          comment_text: comment.text,
          created_date: (new Date()).toISOString(),
          id: comment.id ?? 0,
          user: userId,
          parent_comment: comment.reply_to,
          replies: []
        };
        newComment = await API.postComment(articleId, dto);
      }

      if (!newComment.parent_comment) {
        if (isEditing) {
          const index = this.comments.findIndex(c => c.id === newComment.id);
          this.comments[index].comment_text = newComment.comment_text;
          this.comments[index].updated_date = newComment.updated_date;
          return;
        }
        this.comments.unshift(newComment);
      } else {
        this.findAndInsert(newComment, this.comments, isEditing);
      }
    },

    findAndInsert(comment: ArticleComment, comments: ArticleComment[], isEditing: boolean): boolean {
      for (const c of comments) {
        if (c.id === comment.parent_comment) {

          if (isEditing) {
            const index = c.replies.findIndex(c => c.id === comment.id);
            c.replies[index].comment_text = comment.comment_text;
            c.replies[index].updated_date = comment.updated_date;
          } else {
            c.replies.unshift(comment);
          }
          return true;
        }

        if (this.findAndInsert(comment, c.replies, isEditing)) {
          return true;
        }
      }

      return false;
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
      <PostCommentView @comment-posted="postComment"/>
      <ArticleCommentView v-for="comment in comments" :key="comment.id" :comment="comment" @comment-posted="postComment"
                          @comment-edited="postComment"/>
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