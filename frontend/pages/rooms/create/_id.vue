<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6 class="mx-4">
                <v-card class="elevation-12 structure-card">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Create new room</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
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
                        <v-btn color="primary" @click="saveRoom">Save</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
export default {
    name: 'createRoom',
    middleware: 'auth',
    data() {
        return {
            rules: [
                value => !value || value.size < 2000000 || 'Image size should be less than 2 MB!',
            ],
            room: {
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
            // Add structure id
            this.room.structure_id = parseInt(this.$route.params.id)
            //Build data request
            var data = {
                owner_id: this.$auth.user.id,
                room: this.room
            }
            // Request
            await this.$axios.post('/rooms/create', data).then(function (response) {
                _self.$toast.success('Room created!')
                setTimeout(() => {
                    _self.$router.push('/structures/edit/' + _self.$route.params.id);
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

</style>