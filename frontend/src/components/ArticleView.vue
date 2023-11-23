<template>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{{ article.title }}</h5>
            <p class="card-text"> {{ article.content }}</p>
            <p class="card-text"><small class="text-muted">{{ article.category }}</small></p>
        </div>
    </div>
</template>
  
<style scoped lang="scss"></style>
  
<script lang="ts">
import { defineComponent, PropType } from 'vue'
import Article from "../lib/models/Article";

export default defineComponent({
    name: "ArticleView",
    props: {
        article : {
            type: Object as PropType<Article>,

        }
    },
    computed: {
        displayDate(): string {
            return "Now";
        }
    }
})
</script>