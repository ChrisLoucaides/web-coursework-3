import { defineStore } from 'pinia';
import Cookies from 'js-cookie';

interface User {
  id: number;
  username: string;
  // TODO: WEB-9 do we need any more fields in User here?
}

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