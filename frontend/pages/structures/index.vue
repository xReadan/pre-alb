<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm12 md12>
                <v-card class="elevation-4">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Your Structures</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="structures_list" :items-per-page="5"
                            class="elevation-1">
                            <template v-slot:item.manage="{ item }">
                                <v-chip class="mr-2 manage-chip" @click="action('reservations', item.id)"
                                    color="success" outlined>
                                    <font-awesome-icon icon="fa-solid fa-calendar-days" />
                                    &nbsp; Check Reservations
                                </v-chip>
                                <v-chip class="mr-2 manage-chip" @click="action('edit', item.id)" color="primary"
                                    outlined>
                                    <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                                    &nbsp; Edit Structure
                                </v-chip>
                                <v-chip class="manage-chip" @click="action('delete', item.id)" color="red" outlined>
                                    <font-awesome-icon icon="fa-solid fa-trash" />
                                    &nbsp; Delete
                                </v-chip>
                            </template>
                        </v-data-table>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="$router.push('/structures/create');">Create New Structure</v-btn>
                    </v-card-actions>
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
                { text: 'ID', value: 'id' },
                { text: 'Name', value: 'name', sortable: 0, align: 'center' },
                { text: 'City', value: 'city', sortable: 0, align: 'center' },
                { text: 'Manage', value: 'manage', sortable: 0, align: 'center' }
            ],
            structures_list: []
        }
    },
    async fetch() {
        var _self = this;
        await this.$axios.post('/structures/list', { id: this.$auth.user.id }).then(function (response) {
            _self.structures_list = response.data
        })
    },
    methods: {
        action: function (type, id) {
            var _self = this;
            if (type == 'delete') {
                this.$swal({
                    title: 'Confirm Action',
                    icon: 'warning',
                    html: `Do you want to delete structure <b>#${id}</b>?`,
                    showCancelButton: true,
                    confirmButtonText: 'Delete',
                }).then(function (result) {
                    if (result.isConfirmed && result.value) {
                        _self.$axios.post('/structures/delete', {
                            user_id: _self.$auth.user.id,
                            structure_id: id
                        }).then(function (response) {
                            _self.$fetch()
                            _self.$swal({
                                icon: 'success',
                                title: 'Operation completed',
                            })
                        })
                    }
                });
            } else {
                this.$router.push(`/structures/${type}/${id}`)
            }
            console.log(type, id)
        }
    }
}
</script>

<style scoped>
.manage-chip {
    cursor: pointer;
}
</style>