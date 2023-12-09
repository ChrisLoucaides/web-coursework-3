<template>
  <div>
    <h2>Redirecting to login...</h2>
  </div>
</template>

<script>
export default {
  name: 'DjangoLoginPage',
  beforeRouteEnter(to, from, next) {
    window.location.href = 'http://localhost:8000/login/';
  },
};
</script>

<style scoped>
</style>
