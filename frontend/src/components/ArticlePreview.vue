<script lang="ts">
import {defineComponent, PropType} from 'vue'
import ArticleCommentView from "./ArticleCommentView.vue";
import PostCommentView from "./PostCommentView.vue";
import Article from "../utils/models/Article.ts"
import Pill from "../components/Pill.vue";

export default defineComponent({
  name: "ArticlePreview.vue",
  components: {Pill, PostCommentView, ArticleCommentView},
  props: {
    article: {
      type: Object as PropType<Article>,
      required: true
    }
  },
  computed: {
    previewTitle(): string {
      return this.truncate(this.article.title_text);
    },
    previewSubtext(): string {
      return this.truncate(this.article.content_text, 15);
    }
  },
  methods: {
    truncate(input: string, limit: number = 30): string {
      return input.length > limit ? input.substring(0, limit) + '...' : input;
    },
    onClick() {
      console.log(this.article)
      this.$router.push(`article/${this.article.id}`)
    }
  }
})
</script>

<template>
  <div class="articlePreview" @click="onClick">
    <div class="imageCol">
      <img src="../assets/BreakingNews.png"/>
    </div>
    <div class="content">
      <h3>{{ previewTitle }}</h3>
      <span> {{ previewSubtext }}</span>
      <div class="pills">
        <Pill :text-content="article.category"/>
        <Pill left-icon="bi bi-chat" :text-content="article.comment_count.toString()"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .articlePreview {
    background-color: #ffffff;
    border-radius: 0.357rem;
    border: 1px solid grey;
    display: flex;
    flex-direction: row;
    box-shadow: rgba(100, 100, 111, 0.2) 0 7px 29px 0;
    overflow: hidden;
    transition: 0.3s ease-in-out;
    cursor: pointer;
  }

  .articlePreview:hover {
    transform: scale(1.01);
  }

  .imageCol {
    img {
      max-width: 12.5em;
      width: auto;
      height: 100%;
    }
  }

  .content {
    padding: 1rem;

    h3 {
      font-weight: bold;
    }
  }

  .pills {
    display: flex;
    flex-direction: row;
    gap: 1rem;
  }
</style>