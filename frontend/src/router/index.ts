import {createRouter, createWebHistory} from 'vue-router'


import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import TestCommentsPage from '../pages/TestCommentPage.vue';
import TestArticlePage from '../pages/TestArticlePage.vue';
import DjangoLoginPage from "../pages/DjangoLoginPage.vue";
import {useAuthStore} from "../../auth.ts";

import Cookies from 'js-cookie';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''


const router = createRouter({
    history: createWebHistory(base),
    routes: [
        {path: '/', name: 'Main Page', component: MainPage, beforeEnter: requireAuth},
        {path: '/other/', name: 'Other Page', component: OtherPage},
        {path: '/testing/comments', name: 'Testing Comments page', component: TestCommentsPage},
        {path: '/testing/articles', name: 'Testing articles page', component: TestArticlePage},
        {path: '/django-login', name: 'Django Login', component: DjangoLoginPage},
    ]
})

async function requireAuth(to, from, next) {
    try {
        const user_id = Cookies.get('user_id');

        const authStore = useAuthStore();

        if (user_id) {
            authStore.login({ id: parseInt(user_id) });

            next({ name: 'Main Page' });
        } else {
            next({ name: 'Django Login' });
        }
    } catch (error) {
        console.error('Error checking authentication status:', error);
        next({ name: 'Django Login' });
    }
}

export default router
