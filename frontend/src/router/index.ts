import {createRouter, createWebHistory} from 'vue-router'


import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import TestCommentsPage from '../pages/TestCommentPage.vue';
import TestArticlePage from '../pages/TestArticlePage.vue';
import DjangoLoginPage from "../pages/DjangoLoginPage.vue";
import {authGuard} from "./authGuard.ts";

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''


const router = createRouter({
    history: createWebHistory(base),
    routes: [
        {path: '/', name: 'Main Page', component: MainPage},
        {path: '/other/', name: 'Other Page', component: OtherPage},
        {path: '/testing/comments', name: 'Testing Comments page', component: TestCommentsPage},
        {path: '/testing/articles', name: 'Testing articles page', component: TestArticlePage},
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
