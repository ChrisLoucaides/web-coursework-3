<template>
  <div>
    <h2>Redirecting to login...</h2>
  </div>
</template>

<script>
import {defineComponent} from "vue";

export default defineComponent({
  name: 'DjangoLoginPage',
  beforeRouteEnter(to, from, next) {
    window.location.href = 'http://localhost:8000/login/';
  },
});
</script>

<style scoped>
</style>
