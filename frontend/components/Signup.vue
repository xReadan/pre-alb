<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Create new account</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field name="username" label="Username" type="text" v-model="username">
                            </v-text-field>
                            <v-text-field name="email" label="Email" type="text" v-model="email">
                            </v-text-field>
                            <v-text-field name="password" label="Password" type="password" v-model="password">
                            </v-text-field>
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
            username: '',
            email: '',
            password: ''
        }
    },
    methods: {
        async signupHandler() {
            const data = {
                'username': this.username,
                'email': this.email,
                'password': this.password
            }
            try {
                const res = await this.$axios.post('/register', data);
            } catch (error) {
                console.log(error.message);
            }
        }
    }
}
</script>

<style scoped>

</style>