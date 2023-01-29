<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm12 md12>
                <v-card class="elevation-4">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>{{ structure.name }} - Book from {{ date_from }} to {{
                            date_to
                        }}</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-row>
                            <v-col cols="12" sm="12" md="6">
                                <img :src="structure.image" class="structure-image">
                            </v-col>
                            <v-col cols="12" sm="12" md="6">
                                <div class="structure-description">{{ structure.description }}</div>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="12" sm="12" md="12">
                                <v-data-table :headers="headers" :items="rooms" class="elevation-1" hide-default-footer>
                                    <template v-slot:item.imange_render="{ item }">
                                        <img :src="item.image" class="room-image">
                                    </template>
                                    <template v-slot:item.manage="{ item }">
                                        <v-chip class="mr-2 manage-chip" @click="book(item)" color="primary" outlined>
                                            <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                                        </v-chip>
                                    </template>
                                </v-data-table>
                            </v-col>
                        </v-row>
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
            date_from: '',
            date_to: '',
            structure: {},
            rooms: [],
            headers: [
                { text: 'Image', value: 'imange_render' },
                { text: 'Room', value: 'name', sortable: 0, align: 'center' },
                { text: 'Description', value: 'description', sortable: 0, align: 'center' },
                { text: 'Price (€/day)', value: 'price', sortable: 1, align: 'center' },
                { text: 'Book', value: 'manage', sortable: 0, align: 'center' }
            ],
        }
    },
    async fetch() {
        var _self = this
        // Check params
        if (!this.$route.query.date_from || this.$route.query.date_from == "" || !this.$route.query.date_to || this.$route.query.date_to == "") {
            this.$router.push('/');
        }
        // Set params
        this.date_from = this.$route.query.date_from
        this.date_to = this.$route.query.date_to
        // Fetch data
        await this.$axios.post('/structures/structure', {
            structure_id: parseInt(this.$route.params.id)
        }).then(function (response) {
            _self.structure = response.data
        })
        // Fetch rooms
        await this.$axios.post('/rooms/list', {
            structure_id: parseInt(this.$route.params.id)
        }).then(function (response) {
            _self.rooms = response.data
        })
    },
    methods: {
        compute_days_delta() {
            var date_from = new Date()
            var date_to = new Date(this.date_to)
            return Math.abs(date_from.getDate() - date_to.getDate())
        },
        async book(room) {
            var _self = this;
            var days_delta = this.compute_days_delta()
            var total_price = days_delta * room.price
            var html_text_book = `
            <table style="width: 100%">
                <tr>
                    <td align="left">Structure</td>
                    <td align="right"><b>${this.structure.name}</b></td>
                </tr>
                <tr>
                    <td align="left">Room</td>
                    <td align="right"><b>${room.name}</b></td>
                </tr>
                <tr>
                    <td align="left">From</td>
                    <td align="right"><b>${this.date_from}</b></td>
                </tr>
                <tr>
                    <td align="left">To</td>
                    <td align="right"><b>${this.date_to}</b></td>
                </tr>
                <tr>
                    <td align="left">Total</td>
                    <td align="right"><b>${total_price}€</b> (${room.price}€/day - ${days_delta} days)</td>
                </tr>
            </table>`
            this.$swal({
                title: 'Confirm your booking',
                html: html_text_book,
                showCancelButton: true,
                confirmButtonText: 'Book',
            }).then(function (result) {
                if (result.isConfirmed && result.value) {
                    _self.$axios.post('/reservations/create', {
                        structure_id: _self.structure.id,
                        room_id: room.id,
                        user_id: _self.$auth.user.id,
                        date_from: _self.date_from,
                        date_to: _self.date_to,
                    }).then(function (response) {
                        _self.$toast.success("Reservation requested!", { duration: 2000 })
                        // Clean route params
                        _self.$router.replace({'query': null});
                        // Redirect
                        setTimeout(() => {
                            _self.$router.push('/reservation');
                        }, 1000);
                    }).catch(function (e) {
                        _self.$toast.error("Something went wrong")
                    })
                }
            });
        }
    }
}
</script>

<style scoped>
.room-image {
    padding: 4px;
    width: 240px;
    object-fit: cover;
}

.structure-image {
    width: 100%;
    object-fit: cover;
}

.structure-description {
    font-size: 18px;
    font-weight: 600;
    vertical-align: middle;
    justify-content: center;
    display: flex;
    align-items: center;
    height: 100%;
}
</style>