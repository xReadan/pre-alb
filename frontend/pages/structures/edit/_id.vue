<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>{{ structure.name }}</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <div class="col-md-12 avatar-section">
                            <div v-if="structure.image" class="structure-image">
                                <img :src="structure.image">
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
                            <v-text-field name="name" label="Name" type="text" v-model="structure.name"
                                :error-messages="errorMessages.name" disabled>
                            </v-text-field>
                            <v-text-field name="city" label="City" type="text" v-model="structure.city"
                                :error-messages="errorMessages.city">
                            </v-text-field>
                            <v-text-field name="address" label="Address" type="text" v-model="structure.address"
                                :error-messages="errorMessages.address">
                            </v-text-field>
                            <v-text-field name="rooms" label="Number of Rooms" type="number" v-model="structure.rooms"
                                :error-messages="errorMessages.rooms">
                            </v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" @click="$router.push('/structures')"><font-awesome-icon
                                icon="fa-solid fa-caret-left" /></v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="updateStructure">Edit</v-btn>
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
            rules: [
                value => !value || value.size < 2000000 || 'Image size should be less than 2 MB!',
            ],
            structure: {
                structure_id: 0,
                owner_id: 0,
                name: '',
                city: '',
                address: '',
                image: '',
                rooms: ''
            },
            errorMessages: {
                name: '',
                city: '',
                address: '',
                image: '',
                number_of_rooms: ''
            },
        }
    },
    async fetch() {
        var _self = this;
        await this.$axios.post('/structures/structure', {
            owner_id: this.$auth.user.id,
            structure_id: parseInt(this.$route.params.id)
        }).then(function (response) {
            _self.structure = response.data
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
            this.structure.image = data;
        },
        async updateStructure() {
            var _self = this;
            // Reset errors
            this.resetErrors()
            // Request
            await this.$axios.post('/structures/update', this.structure).then(function (response) {
                _self.$toast.success('Structure updated!')
                setTimeout(() => {
                    _self.$router.push('/structures');
                }, 1300);
            }).catch(function (e) {
                _self.$toast.success('Something went wrong!')
            })
        }
    }
}
</script>

<style scoped>
.avatar-section div {
    text-align: center;
}

.no-image img {
    border: 1px solid #0D1B2A;
    border-radius: 100px;
    width: 200px;
}

.structure-image img {
    max-width: 100%;
    max-height: 300px;
    border-radius: 12px;
}
</style>