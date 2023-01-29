<template>
  <v-container flluid>
    <v-layout align-center justify-center>
      <v-flex xs12 sm12 md12>
        <Search ref="searchBar"></Search>
      </v-flex>
    </v-layout>
    <v-layout align-center justify-center mt-4 class="search-list" v-if="searched">
      <v-flex xs12 sm12 md12>
        <v-toolbar dark color="primary" class="search-list-header">
          <v-toolbar-title>Structure found</v-toolbar-title>
        </v-toolbar>
        <v-card class="mx-8 my-12" max-width="374" v-for="structure in structures_found" :key="structure.id">
          <v-img height="250" :src="structure.image"></v-img>
          <v-card-title>{{ structure.name }}</v-card-title>
          <v-card-text>
            <div class="my-4 text-subtitle-1">
              {{ structure.city }} - {{ structure.address }}
            </div>
            <!-- <div>Description</div> -->
          </v-card-text>
          <v-divider class="mx-4"></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="reserve(structure.id)">
              Reserve
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-card v-if="structures_found.length == 0">
          <v-card-text class="not-found-card">
            No structures found for the selected location and dates
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'IndexPage',
  data() {
    return {
      searched: false,
      structures_found: [],
      selected_params: {}
    }
  },
  methods: {
    async fetchStructures(params) {
      var _self = this;
      await this.$axios.post('/structures/search', params).then(function (response) {
        _self.structures_found = response.data
      }).catch(function (e) {
        _self.$toast.error("Something went wrong")
      })
    },
    async reserve(structure_id) {
      var _self = this;
      // User must be logged in to reserve
      if (!this.$auth.loggedIn) {
        this.$toast.error("You must login or create an account before make a reservation!", { duration: 3000 })
        this.$router.push('/login');
      } else {
        var params = {
          structure: structure_id,
          user: this.$auth.user.id,
          date_from: this.selected_params.date_from,
          date_to: this.selected_params.date_to,
        }
        await this.$axios.post('/reservations/create', params).then(function (response) {
          _self.$toast.success("Reservation requested!", { duration: 2000 })
          _self.$router.push('/reservation');
        }).catch(function (e) {
          _self.$toast.error("Something went wrong")
        })
      }
    }
  },
  mounted() {
    this.$nextTick(function () {
      var _self = this
      this.$refs.searchBar.$on('search', function (params) {
        _self.searched = true;
        _self.selected_params = params
        _self.fetchStructures(params)
      })
    })
  }
}
</script>
<style scoped>
.search-list {
  background-color: white;
  border-radius: 4px;
}

.search-list-header {
  border-radius: 4px 4px 0 0;
}

.not-found-card {
  padding: 64px;
  text-align: center;
}
</style>
