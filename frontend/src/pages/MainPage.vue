<template>

    <div class="d-flex justify-content-center align-items-center ms-auto">
        <!-- Trigger for Profile -->
        <div class="EditProfile me-3">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#prefsModal">
                Edit Profile
            </button>
        </div>

        <!-- Trigger for Profile Picture -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#profilePicModal">
            Edit Profile Picture
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
        <NoArticles
                v-if="!isLoading && articles.filter(a => filteredCategory === 'All' || filteredCategory === a.category).length === 0"/>
    </div>


  <!--Profile Modal -->
    <div class="modal fade" id="profilePicModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Update Profile Picture</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <label for="profile_picture">Profile picture:</label><br>
                    <input type="file" id="profile-picture" name="image" accept="image"
                           @change="handleFileChange"><br><br>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success" @click="updateProfilePicture">Confirm Changes</button>
                </div>
            </div>
        </div>
    </div>

  <!-- Preferences Modal -->
    <div class="modal fade" id="prefsModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
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
                    <button type="button" class="btn btn-success" @click="updateDetails">Confirm Changes</button>
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
import User, {UpdateDetails} from "../utils/models/User";
import API from "../utils/api";
import PillFilter from "../components/PillFilter.vue";
import NoArticles from "../components/NoArticles.vue";
import {Modal} from "bootstrap";

export default defineComponent({
    components: {NoArticles, PillFilter, ArticlePreview},

    setup() {
        const authStore = useAuthStore();

        return {authStore};
    },
    data() {
        return {
            isLoading: true,
            articles: [] as Article[],
            current_user_data: {} as User,
            date_of_birth: null as Date | null,
            email: "",
            profile_picture: null as File | null, // Store the file here
            preferences: [] as string[],
            checkedPrefs: [] as string[],
            filteredCategory: "",
            filterCategories: [] as string[],
        };
    },
    async mounted() {
        if (this.authStore.isAuthenticated) {
            await this.fetchArticles();
        } else {
            console.log("No user");
        }
        this.isLoading = false;
    },
    methods: {
        handleFileChange(event: Event) {
            const input = event.target as HTMLInputElement;
            this.profile_picture = input.files?.[0] ?? null;
            console.log(this.profile_picture);
        },
        async fetchArticles() {
            this.filterCategories = ["All", ...(this.authStore.user?.preferences ?? [])];
            this.filteredCategory = "All";
            const resp = await API.fetchArticles();
            this.articles = resp;
        },
        setFilter(filter: string) {
            this.filteredCategory = filter;
        },
        async updateDetails() {
            const authStore = useAuthStore();

            const data: UpdateDetails = {
                date_of_birth: this.date_of_birth?.toISOString().split('T')[0] ?? '',
                email: this.email,
                preferences: this.checkedPrefs
            };

            const response = await API.updateUser(data);

            if (response === 200) {
                if (authStore.user) {
                    authStore.user.preferences = this.checkedPrefs;
                    if (this.date_of_birth) {
                        authStore.user.date_of_birth = new Date(this.date_of_birth.toString());
                    }
                    if (this.email) {
                        authStore.user.email = this.email;
                    }
                }
                await this.fetchArticles();
                const modal = Modal.getInstance('#prefsModal')
                if (modal) {
                    modal.hide();
                } else {
                    alert('no modal')
                }
            }
        },
        async updateProfilePicture() {
            if (this.profile_picture) {
                const formData = new FormData();
                formData.append("profile_picture", this.profile_picture);

                try {
                    await API.updateProfilePicture(formData);
                    await this.fetchArticles();

                    const modal = Modal.getInstance('#profilePicModal')
                    if (modal) {
                        modal.hide();
                    } else {
                        alert('no modal')
                    }
                } catch (error) {
                    console.error(error);
                }
            } else {
                alert("No profile picture selected");
            }
        },
    },
});
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