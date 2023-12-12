<template>
  <!-- Button trigger modal -->
  <div class="EditProfile">
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
      Edit Profile
    </button>
  </div>


  <div v-for="article in response_data" :key="article">
    <ArticleView :article="(article as Object as Article)">
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
          <input type="date" id="birthday" name="birthday" v-model="birthday" required><br><br>
          <label for="email">Email:</label><br>
          <input type="text" id="email" name="email" v-model="email" required><br><br>
          <label for="profile_picture">Profile picture:</label><br>
          <input type="file" id="img" name="img" accept="image/*" required><br><br>

          <label for="preferences">Preferences:</label><br>
          <div class="preferences">
            <input type="checkbox" id="Finance" name="FinanceBox" value="Finance">
            <label for="FinanceCheckbox">Finance</label><br>

            <input type="checkbox" id="Technology" name="TechnologyBox" value="Technology">
            <label for="TechnologyCheckbox">Technology</label><br>

            <input type="checkbox" id="Sport" name="SportBox" value="Sport">
            <label for="SportCheckbox">Sport</label><br>
          </div>

        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Confirm Changes</button>
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


export default defineComponent({
  components: { ArticleView },

  setup() {
    const authStore = useAuthStore()

    return { authStore }
  },
  data() {
    return {
      response_data: '',
      date_of_birth: '',
      email: '',
      profile_picture: Image,
      preferences: Array<String>,
    }
  },
  async mounted() {
    if (this.authStore.isAuthenticated) {
      console.log(this.authStore.user)
      const response = await fetch("http://localhost:8000/articles/")
      this.response_data = await response.json()
      console.log(this.response_data)
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
      const authStore = useAuthStore();
      const response = await fetch('http://localhost:8000/api/update_person', {
        method: 'PUT',

        body: JSON.stringify({
          "id": authStore.$id,
          "birthday": this.date_of_birth,
          "email": this.email,
          // "image": this.profile_picture,
          "preferences": this.preferences
        })
      })

      console.log(response)

      await this.getUpdatesDetails()
    },
  },

})
</script>


<style scoped></style>