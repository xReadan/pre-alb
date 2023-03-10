<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6>
                <v-card class="elevation-12 structure-card">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Create new account</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <h1>Basic informations</h1>
                            <v-file-input :rules="rules" accept="image/png, image/jpeg, image/bmp"
                                placeholder="Pick an image" prepend-icon="mdi-camera" label="Image"
                                :error-messages="errorMessages.image" @change="filesChange">
                            </v-file-input>
                            <v-text-field name="name" label="Name" type="text" v-model="structure.name"
                                :error-messages="errorMessages.name">
                            </v-text-field>
                            <v-text-field name="city" label="City" type="text" v-model="structure.city"
                                :error-messages="errorMessages.city">
                            </v-text-field>
                            <v-text-field name="address" label="Address" type="text" v-model="structure.address"
                                :error-messages="errorMessages.address">
                            </v-text-field>
                            <v-text-field name="rooms" label="Number of Rooms" type="number"
                                v-model="structure.rooms" :error-messages="errorMessages.rooms">
                            </v-text-field>
                            <v-textarea auto-grow label="Description" rows="4" row-height="20"
                                v-model="structure.description"></v-textarea>
                        </v-form>
                        <v-form>
                            <h1>Services</h1>
                            <v-row>
                                <v-col cols="12" sm="4" md="4">
                                    <v-checkbox v-model="structure.restaurants" label="Restaurant" color="success"
                                        hide-details></v-checkbox>
                                </v-col>
                                <v-col cols="12" sm="4" md="4">
                                    <v-checkbox v-model="structure.pool" label="Swimming pool" color="success"
                                        hide-details></v-checkbox>
                                </v-col>
                                <v-col cols="12" sm="4" md="4">
                                    <v-checkbox v-model="structure.spa" label="SPA" color="success"
                                        hide-details></v-checkbox>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="createStructure">Create</v-btn>
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
                value => !value || value.size < 2000000 || 'Avatar size should be less than 2 MB!',
            ],
            structure: {
                name: '',
                city: '',
                address: '',
                avatar: '',
                image: '',
                description: '',
                restaurants: false,
                pool: false,
                spa: false
            },
            errorMessages: {
                name: '',
                city: '',
                address: '',
                avatar: '',
                number_of_rooms: '',
                image: '',
                description: ''
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
            this.structure.image = data;
        },
        async createStructure() {
            var _self = this;
            // Reset errors
            this.resetErrors()
            // Add user id
            this.structure.owner = this.$auth.user.id
            // Request
            await this.$axios.post('/structures/create', this.structure).then(function (response) {
                _self.$toast.success('New structure created!')
                setTimeout(() => {
                    _self.$router.push('/structures');
                }, 1300);
            }).catch(function (e) {
                var data = e.response.data;
                for (var idx in data) {
                    _self.errorMessages[idx] = data[idx][0]
                }
            })
        }
    }
}
</script>

<style scoped>
.structure-card h1 {
    text-align: center;
}
</style>