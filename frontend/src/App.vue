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
    <footer class="footer fixed-bottom py-3 bg-dark">
        <div class="container text-center text-white">
            <p>&copy; {{ currentYear }} Sky News 2</p>
            <p>Web app developed by:</p>
            <div class="contributors">
                <a href="https://tomk." class="contributor-link">Tom Knighton</a>
                <a href="https://chrisloucaides.com" class="contributor-link">Christos Loucaides</a>
                <a href="https://github.com/AmirH01" class="contributor-link">Amir Hadzic</a>
                <a href="https://github.com/nevadafield" class="contributor-link">Niamh Field</a>
            </div>
        </div>
    </footer>
</template>

<script lang="ts">
import ArticleView from './components/ArticleView.vue';
import {defineComponent} from 'vue';
import {RouterView} from 'vue-router';
import {useAuthStore} from '../auth.ts';

export default defineComponent({
    components: {RouterView, ArticleView},
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

.contributors {
    display: flex;
    align-items: center;
    justify-content: center;
}

.contributor-link {
    margin-right: 2em;
    text-decoration: none;
    color: #36d072;
}

.contributor-link:hover {
    color: #abd5c2;
}

</style>
