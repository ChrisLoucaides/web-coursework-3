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
        <RouterView class="flex-shrink-0"/>

    </main>
</template>

<script lang="ts">

import ArticleView from './components/ArticleView.vue';
import {defineComponent,} from "vue";
import {RouterView} from "vue-router";


export default defineComponent({
    components: {RouterView, ArticleView},
    name: "app",
});

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700&display=swap');
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css");


body {
    font-family: 'Nunito', sans-serif !important;
}
</style>
