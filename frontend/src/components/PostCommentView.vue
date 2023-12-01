<template>
  <form @submit.prevent="submit">
    <div class="mb-3">
      <textarea class="form-control form-multiline" placeholder="Write your comment here" v-bind="text"></textarea>
    </div>
    <div class="mb-3 buttons-view">
      <button class="btn btn-primary" type="submit">Post</button>
    </div>
  </form>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import ArticleComment from "../utils/models/ArticleComment";

export default defineComponent({
  name: "PostCommentView",
  data() {
    return {
      text: ""
    }
  },
  methods: {
    async submit() {
      const newComment: ArticleComment = {
        id: 0,
        user: 1,
        comment_text: this.text,
        created_date: new Date(),
        replies: []
      };

      this.$emit('postComment', newComment);
    }
  }
})
</script>