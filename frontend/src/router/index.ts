import {createRouter, createWebHistory} from 'vue-router'


import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';

import DjangoLoginPage from "../pages/DjangoLoginPage.vue";
import {authGuard} from "./authGuard.ts";
import ArticlePage from "../pages/ArticlePage.vue";

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''


const router = createRouter({
    history: createWebHistory(base),
    routes: [
        {path: '/', name: 'Main Page', component: MainPage},
        {path: '/other/', name: 'Other Page', component: OtherPage},
        {path: '/article/:id', name: 'Article Page', component: ArticlePage},
        {path: '/django-login', name: 'Django Login', component: DjangoLoginPage, meta: { redirect: 'http://127.0.0.1:8000/login/'}},
    ]
})


router.beforeEach((to, from, next) => {
    if (to.meta.redirect) {
        window.location.replace(to.meta.redirect as string);
        return;
    }
    else {
        authGuard(to, from, next);
    }
});


export default router
