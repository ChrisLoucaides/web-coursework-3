import { useAuthStore } from '../../auth.ts';
import type { NavigationGuard } from 'vue-router';
import Cookies from "js-cookie";
import API from '../utils/api.ts';

export const authGuard: NavigationGuard = async (_to, _from, next) => {
    const authStore = useAuthStore();

    const user_id = Cookies.get('user_id');

    if (user_id) {
        const response = await API.fetchUser()
        authStore.login(response);
    } else {
        authStore.logout();
    }

    if (authStore.isAuthenticated) {
        next();
    } else {
        next({ name: 'Django Login' });
    }
};