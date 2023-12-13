<style scoped lang="scss">

.comment {
  display: flex;
  flex-direction: row;
}

.comment-side {
  display: flex;
  flex-direction: column;
  margin-right: 0.75rem;

  align-items: center;

  .profile-img {
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

  .bi-pencil {
    font-size: 0.6rem;
    line-height: 0.8rem;
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

.editForm {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  button {
    width: fit-content;
  }
}

.replies {
  margin-top: 1rem;
}

.vl {
  background-color: gray;
  border-radius: 0.2rem;
  height: 100%;
  width: 0.15rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>

<template>
  <div v-if="isSkeleton" class="comment placeholder-glow">
    <div class="comment-side">
      <div class="placeholder profile-img"></div>
    </div>
    <div class="comment-content">
      <div class="user-details">
        <span class="placeholder col-1"></span>
        <span class="placeholder col-1"></span>
      </div>

      <span class="placeholder col-4"></span>

    </div>
  </div>


  <div v-if="!isSkeleton && comment" class="comment">
    <div class="comment-side">
      <img
          class="profile-img"
          src="https://static.vecteezy.com/system/resources/previews/007/404/147/original/cute-penguin-sleeping-cartoon-icon-illustration-animal-love-icon-concept-isolated-premium-flat-cartoon-style-vector.jpg"
          alt="user profile picture"/>
      <div v-if="comment.replies?.length > 0" class="vl"/>
    </div>
    <div class="comment-content">
      <div class="user-details">
        <p class="username">{{ user?.username }}</p>
        <p class="date">{{ displayDate }}</p>
        <i v-if="comment.updated_date" class="bi-pencil" data-bs-toggle="tooltip" data-bs-placement="top"
           :data-bs-title="`Edited at ${comment.updated_date}`"></i>

      </div>

      <div v-if="inEditMode" class="editForm">
        <textarea class="form-control form-multiline" :placeholder="comment.comment_text"
                  v-model="editedText"></textarea>
        <button @click="editComment" class="btn btn-primary">Save</button>
      </div>
      <span v-else>{{ comment.comment_text }}</span>


      <div class="comment-actions">
        <button v-if="!inEditMode" @click="toggleReplyForm">{{ replyFormOpen ? 'Cancel' : 'Reply' }}</button>
        <button v-if="isOwned" @click="toggleEditMode">{{ inEditMode ? 'Cancel' : 'Edit' }}</button>
        <button v-if="isOwned &&!inEditMode">Delete</button>
      </div>

      <PostCommentView v-if="replyFormOpen" @comment-posted="postComment" :reply-to="comment.id"/>

      <div class="replies">
        <ArticleCommentView v-for="reply in comment.replies ?? []" :key="reply.id" :comment="reply"
                            @comment-posted="postComment" @comment-edited="onCommentEdited"/>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue'
import ArticleComment, {UpdateComment} from "../utils/models/ArticleComment";
import {Tooltip} from "bootstrap";
import PostCommentView from "../components/PostCommentView.vue";
import User from "../utils/models/User.ts";
import {useAuthStore} from "../../auth.ts";

export default defineComponent({
  name: "ArticleCommentView",
  components: {PostCommentView},
  emits: ['comment-posted', 'comment-edited'],
  setup() {
    const authStore = useAuthStore()

    return {authStore}
  },
  props: {
    comment: {
      type: Object as PropType<ArticleComment>,
    },
    isSkeleton: {
      type: Boolean,
    }
  },
  data() {
    return {
      replyFormOpen: false,
      inEditMode: false,
      editedText: ""
    }
  },
  computed: {
    displayDate(): string {
      return "Now";
    },
    user(): User {
      return this.comment?.user as User;
    },
    isOwned(): boolean {
      return (this.comment?.user as User)?.id === this.authStore?.user?.id;
    }
  },
  mounted() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new Tooltip(tooltipTriggerEl));
    this.editedText = this.comment?.comment_text ?? ""
  },
  methods: {
    toggleEditMode() {
      this.inEditMode = !this.inEditMode;
      if (this.inEditMode) {
        this.editedText = this.comment?.comment_text ?? ""
      }
    },
    toggleReplyForm() {
      this.replyFormOpen = !this.replyFormOpen;
    },
    postComment(comment: UpdateComment) {
      this.replyFormOpen = false;
      this.$emit('comment-posted', comment as UpdateComment);
    },
    editComment() {
      this.inEditMode = false;
      this.$emit('comment-edited', {
        text: this.editedText,
        reply_to: this.comment?.parent_comment,
        id: this.comment?.id
      } as UpdateComment)
    },
    onCommentEdited(comment: UpdateComment) {
      this.$emit('comment-edited', comment as UpdateComment);
    }
  }
})
</script>