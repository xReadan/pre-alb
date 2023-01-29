<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm12 md12>
                <v-card class="elevation-4">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Notifications</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="notifications" :items-per-page="5"
                            class="elevation-1">
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
export default {
    middleware: 'auth',
    data() {
        return {
            headers: [
                { text: 'Text', value: 'text' },
                { text: 'Sent at', value: 'created_at' }
            ],
            notifications: []
        }
    },
    async fetch() {
        var _self = this;
        await this.$axios.post('/notifications/list', { user_id: this.$auth.user.id }).then(function (response) {
            _self.notifications = response.data
        })
        //Remove new notification icon
        this.$root.$children[2].$refs.menu['_data'].new_notifications = false
    },
}
</script>

<style scoped>

</style>