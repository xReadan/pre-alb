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
        <div class="mx-8">
          <v-row class="filter-row">
            <v-col cols="12" sm="12" md="12" class="header-row">
              <h2>Filters</h2>
            </v-col>
            <v-col cols="12" sm="4" md="3">
              <v-checkbox v-model="filter.restaurants" label="Restaurant" color="success" hide-details></v-checkbox>
            </v-col>
            <v-col cols="12" sm="4" md="3">
              <v-checkbox v-model="filter.pool" label="Swimming pool" color="success" hide-details></v-checkbox>
            </v-col>
            <v-col cols="12" sm="4" md="3">
              <v-checkbox v-model="filter.spa" label="SPA" color="success" hide-details></v-checkbox>
            </v-col>
            <v-col cols="12" sm="4" md="3">
              <v-checkbox v-model="filter.show_all" label="Show even not available" color="success"
                hide-details></v-checkbox>
            </v-col>
          </v-row>
          <v-divider class="my-4"></v-divider>
          <v-row>
            <v-col cols="12" sm="4" md="4" v-for="structure in displayed_structures" :key="structure.id">
              <v-card class="my-4" max-width="374">
                <v-img height="250" :src="structure.image"></v-img>
                <v-card-title>{{ structure.name }}</v-card-title>
                <v-card-text>
                  <div class="my-4 text-subtitle-1">
                    {{ structure.city }} - {{ structure.address }}
                  </div>
                  <div>{{ structure.description }}</div>
                </v-card-text>
                <v-divider class="mx-4"></v-divider>
                <v-card-actions>
                  <div class="mx-2">
                    From {{ structure.min_price }}€
                  </div>
                  <v-spacer></v-spacer>
                  <v-btn v-if="structure.available" color="primary" text
                    @click="$router.push('/reserve/' + structure.id + '?date_from=' + selected_params.date_from + '&date_to=' + selected_params.date_to);">
                    Check & Reserve
                  </v-btn>
                  <v-btn v-else color="primary" text @click="getNotification(structure.id)">
                    Notify when available
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          <v-row v-if="displayed_structures.length == 0">
            <v-card-text class="not-found-card">
              No structures found with the selected criteria
            </v-card-text>
          </v-row>
        </div>
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
      displayed_structures: [],
      available_structures: [],
      selected_params: {},
      filter: {
        restaurants: false,
        pool: false,
        spa: false,
        show_all: false
      },
    }
  },
  watch: {
    filter: {
      deep: true,
      handler(val) {
        // Create filter obj
        var filter_obj = {}
        var filters_active = false
        for (var idx in val) {
          if (idx != "show_all" && val[idx]) {
            filters_active = true
            filter_obj[idx] = true
          }
        }
        // If filters are active, filter
        if (filters_active) {
          if (val.show_all) {
            var structures_filtered = this.$_.where(this.structures_found, filter_obj)
            this.$set(this, 'displayed_structures', structures_filtered)
          } else {
            var structures_filtered = this.$_.where(this.available_structures, filter_obj)
            this.$set(this, 'displayed_structures', structures_filtered)
          }
        } else {
          if (val.show_all) {
            this.$set(this, 'displayed_structures', this.structures_found)
          } else {
            this.$set(this, 'displayed_structures', this.available_structures)
          }
        }
      }
    }
  },
  methods: {
    async fetchStructures(params) {
      var _self = this;
      await this.$axios.post('/structures/search', params).then(function (response) {
        _self.structures_found = response.data
        _self.available_structures = _self.$_.where(response.data, { available: true })
        _self.displayed_structures = _self.$_.where(response.data, { available: true })
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
    },
    async getNotification(structure_id) {
      var _self = this
      if (!this.$auth.loggedIn) {
        this.$toast.error("You must login or create an account before make a reservation!", { duration: 3000 })
        this.$router.push('/login');
      } else {
        var params = {
          structure_id: structure_id,
          user_id: this.$auth.user.id,
          date_from: this.selected_params.date_from,
          date_to: this.selected_params.date_to,
        }
        await this.$axios.post('/notifications/create-request', params).then(function (response) {
          _self.$toast.success(response.data, { duration: 2500 })
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

.filter-row .header-row {
  color: #778DA9;
  padding-top: 16px !important;
  padding-bottom: 0 !important;
}

.filter-row .v-input {
  margin-top: 0 !important;
}

.not-found-card {
  padding: 64px;
  text-align: center;
}
</style>
