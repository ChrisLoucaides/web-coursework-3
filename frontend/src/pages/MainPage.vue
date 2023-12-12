<template>
  <!-- Button trigger modal -->
  <div class="EditProfile">
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
      Edit Profile
    </button>
  </div>


  <div v-for="article in response_data" :key="article.id">
    <ArticleView :article="(article as Article)">
    </ArticleView>
  </div>

  <!-- Modal -->
  <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
    aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="staticBackdropLabel">Edit Profile</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <label for="birthday">Birthday:</label><br>
          <input type="date" id="birthday" name="birthday" v-model="date_of_birth" required><br><br>
          <label for="email">Email:</label><br>
          <input type="text" id="email" name="email" v-model="email" required><br><br>
          <label for="profile_picture">Profile picture:</label><br>
          <input type="file" id="img" name="img" accept="image/*" required><br><br>

          <label for="preferences">Preferences (Your current preferences are {{ authStore.user?.preferences }})</label><br>
          <div class="preferences">
            <input type="checkbox" id="Finance" name="FinanceBox" v-model="checkedPrefs" value="Finance">
            <label for="FinanceCheckbox">Finance</label><br>

            <input type="checkbox" id="Technology" name="TechnologyBox" v-model="checkedPrefs" value="Technology">
            <label for="TechnologyCheckbox">Technology</label><br>

            <input type="checkbox" id="Sport" name="SportBox" v-model="checkedPrefs" value="Sport">
            <label for="SportCheckbox">Sport</label><br>
          </div>

        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="updateDetails">Confirm Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ArticleView from "../components/ArticleView.vue";
import { useAuthStore } from "../../auth.ts";
import Article from "../utils/models/Article";
import API from '../utils/api'


export default defineComponent({
  components: { ArticleView },

  setup() {
    const authStore = useAuthStore()

    return { authStore }
  },
  data() {
    return {
      response_data: [] as Article[],
      date_of_birth: '',
      email: '',
      profile_picture: Image,
      preferences: [] as String[],
      checkedPrefs: [],
    }
  },
  async mounted() {
    if (this.authStore.isAuthenticated) {
      console.log(this.authStore.user)
      const response = await API.fetchArticles()
      console.log(response)
      this.response_data = response
    } else {
      console.log("No user")
    }
  },
  methods: {
    async getUpdatesDetails() {
      const response = await fetch("http://localhost:8000/articles/")
      this.response_data = await response.json()
      console.log(this.response_data)
    },
    async updateDetails() {
      console.log(this.checkedPrefs);

      // const authStore = useAuthStore();
      // const response = await fetch('http://localhost:8000/api/update_person', {
      //   method: 'PUT',

      //   body: JSON.stringify({
      //     "id": authStore.$id,
      //     "birthday": this.date_of_birth,
      //     "email": this.email,
      //     // "image": this.profile_picture,
      //     "preferences": this.checkedPrefs
      //   })
      // })

      // console.log(response)

      // await this.getUpdatesDetails()
    },
  },

})
</script>


<style scoped></style>