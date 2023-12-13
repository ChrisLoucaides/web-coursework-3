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
import ArticleView from "../components/ArticleView.vue";
import {useAuthStore} from "../../auth.ts";
import Article from "../utils/models/Article";
import User from "../utils/models/User"
import API from '../utils/api'

declare const Buffer


export default defineComponent({
    components: {ArticleView},

    setup() {
        const authStore = useAuthStore()

        return {authStore}
    },
    data() {
        return {
            response_data: [] as Article[],
            current_user_data: {} as User,
            date_of_birth: Date,
            email: '',
            profile_picture: Image,
            preferences: [] as String[],
            checkedPrefs: [] as String[],
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
        async getUpdatedDetails() {
            const response = await fetch("http://localhost:8000/articles/")
            this.response_data = await response.json()
            console.log(this.response_data)
        },
        handleFileChange(event: Event) {
            const input = event.target as HTMLInputElement;
            this.profile_picture = input.files?.[0];
            console.log(this.profile_picture)
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
            console.log(typeof(this.profile_picture))
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
                this.response_data = await API.fetchArticles()
            }
        },
    },

})
</script>


<style scoped></style>