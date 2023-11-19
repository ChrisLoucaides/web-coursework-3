<template>
  <div class="comment">
    <div class="comment-side">
      <img
          src="https://static.vecteezy.com/system/resources/previews/007/404/147/original/cute-penguin-sleeping-cartoon-icon-illustration-animal-love-icon-concept-isolated-premium-flat-cartoon-style-vector.jpg"
          alt="user profile picture"/>
    </div>
    <div class="comment-content">
      <div class="user-details">
        <p class="username">{{ comment.user?.username }}</p>
        <p class="date">{{ displayDate }}</p>
      </div>
      <span>{{ comment.comment_text }}</span>
      <div class="comment-actions">
        <button>Reply</button>
        <button>Edit</button>
        <button>Delete</button>
      </div>
    </div>

  </div>
</template>

<style scoped lang="scss">

.comment {
  outline: 1px solid blue;
  display: flex;
  flex-direction: row;
}

.comment-side {
  display: flex;
  flex-direction: column;
  margin-right: 1rem;

  img {
    width: 3rem;
    height: 3rem;
    border-radius: 1.5rem;
    object-fit: cover;
    box-shadow: rgba(0, 0, 0, 0.1) 0 4px 12px;
  }
}

.comment-content {
  width: 100%;
  gap: 0;
}

.user-details {
  display: flex;
  flex-direction: row;

  align-items: flex-end;
  width: 100%;
  gap: 5px;

  padding-top: 0.3rem;
  padding-bottom: 0.3rem;

  .username {
    font-size: 0.9rem;
    line-height: 0.9rem;
    font-weight: bolder;
    margin: 0;
  }

  .date {
    font-size: 0.8rem;
    line-height: 0.75rem;
    color: gray;
    margin: 0;
  }
}

.comment-actions {
  display: flex;
  flex-direction: row;

  gap: 1rem;

  margin-top: 0.5rem;

  button {
    background: none;
    border: none;
    padding: 0;
    color: #3d3b3b;
    font-weight: 400;
    font-size: 0.8rem;
  }
}
</style>

<script lang="ts">
import {defineComponent, PropType} from 'vue'
import ArticleComment from "../lib/models/ArticleComment";

export default defineComponent({
  name: "ArticleCommentView",
  props: {
    comment: {
      type: Object as PropType<ArticleComment>,
      required: true
    }
  },
  computed: {
    displayDate(): string {
      return "Now";
    }
  }
})
</script>