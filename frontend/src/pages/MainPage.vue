<template>
  <!-- Button trigger modal -->
  <div class="EditProfile">
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
      Edit Profile
    </button>
  </div>

  <div class="filters">
    <PillFilter v-for="filter in filterCategories" :key="filter" :is-activated="filteredCategory === filter"
                :text-content="filter" @click="setFilter(filter)"/>
  </div>
  <div class="articlePreviews">
    <ArticlePreview
        v-for="article in articles.filter(a => filteredCategory === 'All' || filteredCategory === a.category)"
        :key="article.id" :article="article">
    </ArticlePreview>
    <NoArticles v-if="!isLoading && articles.filter(a => filteredCategory === 'All' || filteredCategory === a.category).length === 0"/>
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
          <input type="date" id="birthday" name="birthday" v-model="date_of_birth"><br><br>
          <label for="email">Email:</label><br>
          <input type="email" id="email" name="email" v-model="email"><br><br>
          <label for="profile_picture">Profile picture:</label><br>
          <input type="file" id="img" name="img" accept="image/*" @change="handleFileChange"><br><br>

          <label for="preferences">Preferences (Your current preferences are {{
              authStore.user?.preferences
            }})</label><br>
          <div class="preferences">
            <input type="checkbox" id="Finance" name="FinanceBox" v-model="checkedPrefs" value="Finance">
            <label for="FinanceCheckbox">Finance</label><br>

            <input type="checkbox" id="Technology" name="TechnologyBox" v-model="checkedPrefs"
                   value="Technology">
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
import {defineComponent} from "vue";
import ArticlePreview from "../components/ArticlePreview.vue";
import {useAuthStore} from "../../auth.ts";
import Article from "../utils/models/Article";
import User from "../utils/models/User"
import API from '../utils/api'
import PillFilter from "../components/PillFilter.vue";
import NoArticles from "../components/NoArticles.vue";

export default defineComponent({
  components: {NoArticles, PillFilter, ArticlePreview},

  setup() {
    const authStore = useAuthStore()

    return {authStore}
  },
  data() {
    return {
      isLoading: true,
      articles: [] as Article[],
      current_user_data: {} as User,
      date_of_birth: Date,
      email: '',
      profile_picture: Image,
      preferences: [] as string[],
      checkedPrefs: [] as string[],
      filteredCategory: '',
      filterCategories: [] as string[]
    }
  },
  async mounted() {
    if (this.authStore.isAuthenticated) {
      await this.fetchArticles()
    } else {
      console.log("No user")
    }
    this.isLoading = false;
  },
  methods: {
    handleFileChange(event: Event) {
      const input = event.target as HTMLInputElement;
      this.profile_picture = input.files?.[0];
      console.log(this.profile_picture)
    },
    async fetchArticles() {
      this.filterCategories = ['All', ...this.authStore.user?.preferences ?? []];
      this.filteredCategory = 'All';
      const resp = await API.fetchArticles();
      this.articles = resp;
    },
    setFilter(filter: string) {
      this.filteredCategory = filter;
    },
    async updateDetails() {
      console.log(this.checkedPrefs);

      const authStore = useAuthStore();

      const data = JSON.stringify({
        // "id": "this.authStore.user?.id",
        "date_of_birth": this.date_of_birth,
        "email": this.email,
        "profile_picture": btoa(this.profile_picture.toString()),
        // "profile_picture": Buffer.from(JSON.stringify(this.profile_picture)).toString('base64'),
        "preferences": this.checkedPrefs,
      })
      console.log(data)
      console.log("DA FIRTST ONES!")
      console.log(typeof (this.profile_picture))
      const response = await API.updatePreferences(data)

      if (response === 200) {
        if (authStore.user != undefined) {
          authStore.user.preferences = this.checkedPrefs
          if (this.date_of_birth != undefined) {
            authStore.user.date_of_birth = new Date(this.date_of_birth.toString())
            console.log(authStore.user.date_of_birth)
          }
          if (this.email != undefined) {
            authStore.user.email = this.email
            console.log(authStore.user.email)
          }
          if (this.profile_picture != undefined) {
            authStore.user.profile_picture = this.profile_picture
            console.log(authStore.user.profile_picture)
          }
        }
        await this.fetchArticles();
      }
    },
  },

})
</script>


<style scoped lang="scss">

.articlePreviews {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filters {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

</style>