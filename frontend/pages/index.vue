<template>
  <v-container flluid>
    <v-layout align-center justify-center>
      <v-flex xs12 sm12 md12>
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Select an awesome location for your next trip!</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-row class="custom-index-row">
                <!-- Location -->
                <v-flex xs12 sm12 md6>
                  <v-text-field name="location" label="Where do you want to go?" type="text" v-model="location">
                  </v-text-field>
                </v-flex>
                <!-- From -->
                <v-flex xs12 sm12 md3>
                  <v-menu v-model="menu_from" :close-on-content-click="false" :nudge-right="40"
                    transition="scale-transition" offset-y min-width="auto">
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field v-model="date_from" label="From" prepend-icon="mdi-calendar" readonly v-bind="attrs"
                        v-on="on"></v-text-field>
                    </template>
                    <v-date-picker v-model="date_from" @input="menu_from = false" :min="min_date"></v-date-picker>
                  </v-menu>
                </v-flex>
                <!-- To -->
                <v-flex xs12 sm12 md3>
                  <v-menu v-model="menu_to" :close-on-content-click="false" :nudge-right="40"
                    transition="scale-transition" offset-y min-width="auto">
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field v-model="date_to" label="To" prepend-icon="mdi-calendar" readonly v-bind="attrs"
                        v-on="on"></v-text-field>
                    </template>
                    <v-date-picker v-model="date_to" @input="menu_to = false" :min="min_date"></v-date-picker>
                  </v-menu>
                </v-flex>
              </v-row>
            </v-form>
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
      menu_from: '',
      location: '',
      menu_from: '',
      date_from: '',
      menu_to: '',
      date_to: '',
      min_date: (new Date).toISOString().split('T')[0]
    }
  },
  mounted () {
    console.log(Date.now())
  }
}
</script>
<style scoped>
.custom-index-row {
  padding: 0 18px;
}
.custom-index-row .flex {
  padding: 0 12px;
}
</style>
