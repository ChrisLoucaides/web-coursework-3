<template>
    <main class="container pt-4">
        <div>
            <router-link
                class=""
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
        </div>
        <RouterView class="flex-shrink-0" />
        <div v-for="article in response_data" :key="article">
                <ArticleView
                    :article="(article as Object as Article)">
                </ArticleView>
            </div>
    </main>
</template>

<script lang="ts">

import ArticleView from './components/ArticleView.vue';
import Article from './utils/models/Article.ts';

import { defineComponent,  } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView, ArticleView },
    data() {
        return {
            response_data: ''
        }
    },
    name: "app",
    async mounted() {
        const response = await fetch("http://localhost:8000/articles/")
        this.response_data = await response.json()
        console.log(this.response_data)
    },
});

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700&display=swap');
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css");


body {
  font-family: 'Nunito', sans-serif !important;
}
</style>
