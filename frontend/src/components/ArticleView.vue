<template>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Article Title: {{ article?.title_text }}, ---- id from django: {{ article?.id }}, but the id from our manual entry: {{ article?.article_id }}</h5>
            <p class="card-text"> {{ article?.content_text }}</p>
            <p class="card-text"><small class="text-muted">{{ article?.category }}</small></p>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import Article from "../utils/models/Article";
import ArticleCommentView from './ArticleCommentView.vue';

export default defineComponent({
    name: "ArticleView",
    props: {
        article: {
            type: Object as PropType<Article>,
        }
    },
    computed: {
        displayDate(): string {
            return "Now";
        }
    },
    components: { ArticleCommentView }
})
</script>