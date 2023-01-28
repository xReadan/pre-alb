<template>
    <div>
        <v-card class="elevation-12">
            <v-toolbar dark color="primary">
                <v-toolbar-title>Select an awesome location for your next trip!</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
                <v-form>
                    <v-row class="custom-index-row">
                        <!-- Location -->
                        <v-flex xs12 sm12 md4>
                            <v-text-field name="location" label="Where do you want to go?" type="text"
                                v-model="params.location" :error-messages="errorMessages.location">
                            </v-text-field>
                        </v-flex>
                        <!-- From -->
                        <v-flex xs12 sm12 md3>
                            <v-menu v-model="params.menu_from" :close-on-content-click="false" :nudge-right="40"
                                transition="scale-transition" offset-y min-width="auto">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-text-field v-model="params.date_from" label="From" prepend-icon="mdi-calendar"
                                        readonly v-bind="attrs" v-on="on" :error-messages="errorMessages.date_from"></v-text-field>
                                </template>
                                <v-date-picker v-model="params.date_from" @input="menu_from = false"
                                    :min="min_date"></v-date-picker>
                            </v-menu>
                        </v-flex>
                        <!-- To -->
                        <v-flex xs12 sm12 md3>
                            <v-menu v-model="params.menu_to" :close-on-content-click="false" :nudge-right="40"
                                transition="scale-transition" offset-y min-width="auto">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-text-field v-model="params.date_to" label="To" prepend-icon="mdi-calendar"
                                        readonly v-bind="attrs" v-on="on" :error-messages="errorMessages.date_to"></v-text-field>
                                </template>
                                <v-date-picker v-model="params.date_to" @input="menu_to = false"
                                    :min="min_date"></v-date-picker>
                            </v-menu>
                        </v-flex>
                        <!-- Button -->
                        <v-flex xs12 sm12 md2 text-md-center mt-4>
                            <v-btn color="primary" @click="search">Search</v-btn>
                        </v-flex>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
export default {
    data() {
        return {
            min_date: (new Date).toISOString().split('T')[0],
            errorMessages: {
                location: '',
                date_from: '',
                date_to: ''
            },
            params: {
                location: '',
                menu_from: '',
                date_from: '',
                menu_to: '',
                date_to: ''
            }
        }
    },
    methods: {
        validate_form() {
            var passed = true
            // Check location
            if (this.params.location == "") {
                this.$toast.error("Missing location!")
                this.errorMessages.location = "Location must not be empty"
                passed = false;
            }
            // Check location
            if (this.params.date_from == "") {
                this.$toast.error("Missing date from!")
                this.errorMessages.date_from = "Date from must not be empty"
                passed = false;
            }
            // Check location
            if (this.params.date_to == "") {
                this.$toast.error("Missing date to!")
                this.errorMessages.date_to = "Date to must not be empty"
                passed = false;
            }
            return passed
        },
        search() {
            if(!this.validate_form()) return
            var params = {
                location: this.params.location,
                date_from: this.params.date_from,
                date_to: this.params.date_to
            }
            this.$emit('search', params)
        }
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