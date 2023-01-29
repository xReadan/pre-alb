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
                            <v-text-field name="email" label="Email" type="text" v-model="email" :rules="[rules.emailMatch]">
                            </v-text-field>
                            <v-text-field name="password" label="Password" type="password" v-model="password" :rules="[rules.emailMatch]">
                            </v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <div class="register-prompt mx-2">Click <NuxtLink to="/signup">here</NuxtLink> if you don't have an account</div>
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
            password: '',
            rules: {
                emailMatch: true
            }
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
                // Remove errors
                this.rules.emailMatch = true
            } catch (error) {
                this.rules.emailMatch = false
            }
        }
    }
}
</script>

<style scoped>
.register-prompt{
    font-size: 12px;
}
</style>