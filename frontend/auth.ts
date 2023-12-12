import { defineStore } from 'pinia';
import Cookies from 'js-cookie';
import User from './src/utils/models/User.ts'


export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false,
    user: null as User | null,
  }),
  actions: {
     login(user: User) {
      this.isAuthenticated = true;
      this.user = user;
    },
    logout() {
      this.isAuthenticated = false;
      this.user = null;
      Cookies.remove('user_id');
    },
    loadAuthenticationState() {
      const user_id = Cookies.get('user_id');
      if (user_id) {
        this.isAuthenticated = true;
        this.user = { id: parseInt(user_id), username: '' };
      }
    },
  },
});