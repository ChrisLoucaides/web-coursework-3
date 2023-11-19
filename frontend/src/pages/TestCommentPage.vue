<template>
  <div class="testCommentContainer">
      <ArticleCommentView :comment="comment"/>
  </div>
</template>

<style scoped>
.testCommentContainer {
  outline: 1px solid red;
}
</style>

<script lang="ts">
import {defineComponent} from 'vue'
import ArticleCommentView from "../components/ArticleCommentView.vue";
import ArticleComment from "../lib/models/ArticleComment.ts";

export default defineComponent({
  name: "TestCommentPage.vue",
  components: {ArticleCommentView},
  data() {
    return {
      comment: {} as ArticleComment
    }
  },
  mounted() {
    this.comment = {
      id: 1,
      comment_text: 'Test',
      created_date: new Date(),
      parent_comment: null,
      replies: [],
      user: {profile_picture: '', username: 'TestUser'}
    };
  }
})
</script>