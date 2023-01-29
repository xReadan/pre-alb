<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6 class="mx-4">
                <v-card class="elevation-12 structure-card">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Create new room</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <div class="col-md-12 avatar-section">
                            <div v-if="room.image" class="room-image">
                                <img :src="room.image">
                            </div>
                            <div v-else class="no-image">
                                <img src="~/assets/images/default_hotel.png">
                            </div>
                        </div>
                        <v-form>
                            <v-file-input :rules="rules" accept="image/png, image/jpeg, image/bmp"
                                placeholder="Pick an image" prepend-icon="mdi-camera" label="Image"
                                :error-messages="errorMessages.image" @change="filesChange">
                            </v-file-input>
                            <v-text-field name="name" label="Name" type="text" v-model="room.name"
                                :error-messages="errorMessages.name">
                            </v-text-field>
                            <v-textarea auto-grow label="Description" rows="4" row-height="20"
                                v-model="room.description" :error-messages="errorMessages.description"></v-textarea>
                            <v-text-field name="rooms" label="Price" type="number" v-model="room.price"
                                :error-messages="errorMessages.price">
                            </v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary"
                            @click="$router.push('/structures/edit/' + $route.params.id)"><font-awesome-icon
                                icon="fa-solid fa-caret-left" /></v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="saveRoom">Update</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
export default {
    name: 'editRoom',
    middleware: 'auth',
    data() {
        return {
            rules: [
                value => !value || value.size < 2000000 || 'Image size should be less than 2 MB!',
            ],
            room: {
                id: this.$route.params.id,
                name: '',
                description: '',
                price: null,
                image: ''
            },
            errorMessages: {
                image: '',
                name: '',
                description: '',
                price: '',
            },
        }
    },
    async fetch() {
        var _self = this;
        var data = {
            owner_id: this.$auth.user.id,
            room_id: this.$route.params.id
        }
        // Request
        await this.$axios.post('/rooms/get', data).then(function (response) {
            _self.room = response.data
        })
    },
    methods: {
        resetErrors() {
            for (var idx in this.errorMessages) {
                this.errorMessages[idx] = ''
            }
        },
        async filesChange(file) {
            /* Make sure file exists */
            if (!file) return;
            /* create a reader */
            const readData = (f) => new Promise((resolve) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(f);
            });
            /* Read data */
            const data = await readData(file);
            this.room.image = data;
        },
        async saveRoom() {
            var _self = this
            this.resetErrors()
            //Build data request
            var data = {
                owner_id: this.$auth.user.id,
                room: this.room
            }
            // Request
            await this.$axios.post('/rooms/edit', data).then(function (response) {
                _self.$toast.success('Room updated!')
                setTimeout(() => {
                    _self.$router.push('/structures/edit/' + _self.room.structure_id);
                }, 1300);
            }).catch(function (e) {
                var data = e.response.data.data;
                console.log(data, e)
                for (var idx in data) {
                    _self.errorMessages[idx] = data[idx]
                }
            })
            console.log(this.room)
        }
    }
}
</script>

<style scoped>
.avatar-section div {
    text-align: center;
}
.room-image img {
    max-width: 100%;
    max-height: 300px;
    border-radius: 12px;
}
.no-image img {
    border: 1px solid #0D1B2A;
    border-radius: 100px;
    width: 200px;
}
</style>