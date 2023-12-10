<template>
  <div v-for="article in response_data" :key="article">
    <ArticleView
        :article="(article as Object as Article)">
    </ArticleView>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import ArticleView from "../components/ArticleView.vue";
import {useAuthStore} from "../../auth.ts";

export default defineComponent({
  components: {ArticleView},
  setup() {
    const authStore = useAuthStore()

    return {authStore}
  },
  data() {
    return {
      response_data: ''
    }
  },
  async mounted() {
    if (this.authStore.isAuthenticated) {
      const response = await fetch("http://localhost:8000/articles/")
      this.response_data = await response.json()
      console.log(this.response_data)
    } else {
      console.log("No user")
    }
  },
})
</script>

<style scoped>
</style>
