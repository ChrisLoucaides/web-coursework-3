<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-success">
            <div class="container">
                <router-link class="navbar-brand" :to="{ name: 'Main Page' }"><img src="./assets/Sky%20News%202.png"
                                                                                   alt="" style="width: 10em;">
                </router-link>

                <button @click="logout" class="btn btn-danger ml-auto">Logout</button>
            </div>
        </nav>

        <main class="container pt-4">
            <RouterView class="flex-shrink-0"/>
        </main>
    </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {RouterView} from 'vue-router';
import {useAuthStore} from '../auth.ts';

export default defineComponent({
    components: {RouterView},
    name: 'app',
    data() {
        return {
            currentYear: new Date().getFullYear(),
        };
    },
    methods: {
        logout() {
            const authStore = useAuthStore();
            authStore.logout();
            this.$router.push({name: 'Django Login'});
        },
    },
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;400;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css');

body {
    font-family: 'Nunito', sans-serif !important;
}
</style>
