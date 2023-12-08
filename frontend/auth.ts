import { defineStore } from 'pinia';

interface User {
  id: number;
  username: string;
  //TODO: WEB-9 do we need any more fields in User here?
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    isAuthenticated: false,
    user: null,
  }),
  actions: {
    login(user) {
      this.isAuthenticated = true;
      this.user = user;
    },
    logout() {
      this.isAuthenticated = false;
      this.user = null;
    },
  },
});
