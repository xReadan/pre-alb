<template>
    <v-container flluid>
        <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
                <v-card class="elevation-12">
                    <v-toolbar dark color="primary">
                        <v-toolbar-title>Personal Informations</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <div class="col-md-12 avatar-section">
                            <div v-if="$auth.user.avatar">
                                <img :src="$auth.user.avatar">
                            </div>
                            <div v-else>
                                <img src="~/assets/default_user.png">
                            </div>
                        </div>
                        <v-form>
                            <v-file-input :rules="rules" accept="image/png, image/jpeg, image/bmp"
                                placeholder="Pick an avatar" prepend-icon="mdi-camera" label="Avatar"
                                @change="filesChange">
                            </v-file-input>
                            <v-text-field name="email" label="Email" type="text" v-model="email" disabled>
                            </v-text-field>
                            <v-text-field name="username" label="Username" type="text" v-model="username">
                            </v-text-field>
                            <v-text-field name="old_password" label="Old Password" type="password"
                                v-model="old_password">
                            </v-text-field>
                            <v-text-field name="new_password" label="New Password" type="password"
                                v-model="new_password">
                            </v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="settingsHalder">Update</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>
<script>
export default {
    //View only for authenticated users
    middleware: 'auth',
    data() {
        return {
            rules: [
                value => !value || value.size < 2000000 || 'Avatar size should be less than 2 MB!',
            ],
            email: this.$auth.user.email,
            username: this.$auth.user.username,
            avatar: null,
            old_password: '',
            new_password: ''
        }
    },
    methods: {
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
            this.avatar = data;
        },
        async settingsHalder() {
            const data = {
                'id': this.$auth.user.id,
                'avatar': this.avatar,
                'username': this.username,
                'email': this.email,
                'old_password': this.old_password,
                'new_password': this.new_password
            }
            try {
                const res = await this.$axios.post('/update-user-settings', data);
                await this.$auth.fetchUser()
                this.$router.push('/');
            } catch (error) {
                console.log(error.message);
            }
        }
    }
}
</script>

<style scoped>
.avatar-section div {
    text-align: center;
}

.avatar-section img {
    width: 150px;
}
</style>