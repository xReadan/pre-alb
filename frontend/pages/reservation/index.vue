<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm12 md12>
                <v-card class="elevation-4">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Your Structures</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="reservaton_list" :items-per-page="5"
                            class="elevation-1">
                            <template v-slot:item.manage="{ item }">
                                <v-chip class="mr-2 manage-chip" @click="delete_reservation(item)" color="error" outlined
                                    v-if="item.can_cancel">
                                    <font-awesome-icon icon="fa-solid fa-trash" />
                                    &nbsp; Cancel Reservations
                                </v-chip>
                            </template>
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
                { text: 'ID', value: 'id' },
                { text: 'Structure', value: 'structure', sortable: 0, align: 'center' },
                { text: 'Address', value: 'address', sortable: 0, align: 'center' },
                { text: 'Period', value: 'period', sortable: 0, align: 'center' },
                { text: 'Manage', value: 'manage', sortable: 0, align: 'center' }
            ],
            reservaton_list: []
        }
    },
    async fetch() {
        var _self = this;
        await this.$axios.post('/reservations/list', { user_id: this.$auth.user.id }).then(function (response) {
            _self.reservaton_list = response.data
        })
    },
    methods: {
        delete_reservation(reservation) {
            var _self = this;
            this.$swal({
                title: 'Confirm Action',
                icon: 'warning',
                html: `Do you want to delete the following reservation><br><br>Structure<br><b>${reservation.structure}</b><br>Period<br><b>${reservation.period}<b>`,
                showCancelButton: true,
                confirmButtonText: 'Delete',
            }).then(function (result) {
                if (result.isConfirmed && result.value) {
                    _self.$axios.post('/reservations/delete', {
                        user_id: _self.$auth.user.id,
                        reservation_id: reservation.id
                    }).then(function (response) {
                        _self.$fetch()
                        _self.$swal({
                            icon: 'success',
                            title: 'Operation completed',
                        })
                    }).catch(function (e) {
                        _self.$toast.error("Somethings went wrong")
                    })
                }
            });
        }
    }
}
</script>

<style scoped>

</style>