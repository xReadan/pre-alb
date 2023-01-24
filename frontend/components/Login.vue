<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Login</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field name="email" label="Email" type="text" v-model="email">
                            </v-text-field>
                            <v-text-field name="password" label="Password" type="password" v-model="password">
                            </v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="loginHandler">Login</v-btn>
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
            email: '',
            password: ''
        }
    },
    methods: {
        async loginHandler() {
            const data = {
                'email': this.email,
                'password': this.password
            };
            try {
                // Request login
                const response = await this.$auth.loginWith('local', { data: data })
                // If no error is caught, set username to storage
                this.$auth.$storage.setUniversal('username', response.data.username)
                // If no error is caught, set tokens to storage
                await this.$auth.setUserToken(response.data.access_token, response.data.refresh_token)
            } catch (error) {
                console.log(error.message)
            }
        }
    }
}
</script>

<style scoped>

</style>