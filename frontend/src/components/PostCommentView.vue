<template>
  <form @submit.prevent="submit">
    <div class="mb-3">
      <textarea class="form-control form-multiline" placeholder="Write your comment here" v-model="text"></textarea>
    </div>
    <div class="mb-3 buttons-view">
      <button class="btn btn-primary" type="submit">Post</button>
    </div>
  </form>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import  {UpdateComment} from "../utils/models/ArticleComment";

export default defineComponent({
  name: "PostCommentView",
  emits: ['comment-posted'],
  props: {
    replyTo: {
      type: Number
    }
  },
  data() {
    return {
      text: ""
    }
  },
  methods: {
    async submit() {
      this.$emit('comment-posted', { text: this.text, reply_to: this.replyTo } as UpdateComment);
      this.text = "";
    }
  }
})
</script>