<template>
    <div class="testArticleContainer">
        <ArticleView :article="article"/>
    </div>
</template>



<style scoped>
.testArticleContainer {
    outline: 1px solid red;
}
</style>
  
<script lang="ts">
import { defineComponent } from 'vue'
import ArticleView from "../components/ArticleView.vue";
import Article from "../lib/models/Article.ts";

export default defineComponent({
    name: "TestArticlePage.vue",
    components: { ArticleView },
    data() {
        return {
            article: {} as Article
        }
    },
    mounted() {
        this.article = {
            id: 1,
            title: 'MY TITLE',
            content: 'MY ARTICLE CONTENT',
            category: 'MY ARTICLE CATEGORY'
        };
    }
})
</script>