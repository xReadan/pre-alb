<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md6>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Create new account</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field name="username" label="Username" type="text" v-model="user.username"
                                :error-messages="errorMessages.username">
                            </v-text-field>
                            <v-text-field name="email" label="Email" type="text" v-model="user.email"
                                :error-messages="errorMessages.email">
                            </v-text-field>
                            <v-text-field name="password" label="Password" type="password" v-model="user.password"
                                hint="At least 8 characters" :error-messages="errorMessages.password">
                            </v-text-field>
                            <v-select :items="items" label="Account type" v-model="user.type"
                                :error-messages="errorMessages.type"></v-select>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="signupHandler">Create</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
export default {
    data() {
        return {
            items: ["Client", "Owner"],
            user: {
                username: '',
                email: '',
                password: '',
                type: ''
            },
            errorMessages: {
                username: '',
                email: '',
                password: '',
                type: ''
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
        async signupHandler() {
            var _self = this;
            // Reset errors
            this.resetErrors()
            // Request
            await this.$axios.post('/users/register', this.user).then(function (response) {
                _self.$toast.success('User created successfully')
                setTimeout(() => {
                    _self.$router.push('/login');
                }, 1300);
            }).catch(function (e) {
                var data = e.response.data;
                for (var idx in data) {
                    _self.errorMessages[idx] = data[idx]
                }
            })
        }
    }
}
</script>

<style scoped>

</style>