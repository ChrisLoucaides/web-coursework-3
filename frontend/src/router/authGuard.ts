import {useAuthStore} from '../../auth.ts';
import type {NavigationGuard} from 'vue-router';
import Cookies from "js-cookie";

export const authGuard: NavigationGuard = async (_to, _from, next) => {
    const authStore = useAuthStore();

    const user_id = Cookies.get('user_id');


    if (user_id) {
       // We want to grab the user from the API ideally here
       authStore.login({id: parseInt(user_id), username: 'TODO: Get whole user?'});
    }

    if (authStore.isAuthenticated) {
        next();
    } else {
        next({name: 'Django Login'});
    }
};