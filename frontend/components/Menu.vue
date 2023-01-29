<template>
    <v-navigation-drawer absolute permanent app left class="custom-menu">
        <template v-slot:prepend>
            <div class="logo">
                <img src="~/assets/images/logo.png">
            </div>
            <div>
                <div class="text-center welcome">
                    <h3>Welcome to PreAlb</h3>
                </div>
            </div>
            <v-divider></v-divider>
            <v-list-item two-line v-if="$auth.loggedIn">
                <v-list-item-avatar class="menu-avatar">
                    <div v-if="$auth.user.avatar">
                        <img :src="$auth.user.avatar">
                    </div>
                    <div v-else>
                        <img src="~/assets/images/default_user.png">
                    </div>
                </v-list-item-avatar>
                <v-list-item-content>
                    <v-list-item-title>
                        <NuxtLink to="/user/settings" class="logged-username">{{ $auth.user.username }}</NuxtLink>
                    </v-list-item-title>
                    <v-list-item-subtitle>
                        <a @click="logout">Logout</a>
                    </v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-list-item two-line v-else>
                <v-list-item-content>
                    <v-list-item-title>Hello user!</v-list-item-title>
                    <v-list-item-subtitle>
                        <NuxtLink to="/login">Login</NuxtLink> or <NuxtLink to="/signup">Signup</NuxtLink>
                    </v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
        </template>

        <v-divider></v-divider>

        <v-list dense>
            <v-list-item class="main-menu">
                <NuxtLink to="/">
                    <div class="menu-icon">
                        <font-awesome-icon icon="fa-solid fa-house" />
                    </div>
                    <v-list-item-content>
                        <v-list-item-title>Home</v-list-item-title>
                    </v-list-item-content>
                </NuxtLink>
            </v-list-item>
            <v-list-item class="main-menu" v-if="$auth.loggedIn && $auth.user.type === 'Owner'">
                <NuxtLink to="/structures">
                    <div class="menu-icon">
                        <font-awesome-icon icon="fa-solid fa-hotel" />
                    </div>
                    <v-list-item-content>
                        <v-list-item-title>My Structures</v-list-item-title>
                    </v-list-item-content>
                </NuxtLink>
            </v-list-item>
            <v-list-item class="main-menu" v-if="$auth.loggedIn">
                <NuxtLink to="/reservation">
                    <div class="menu-icon">
                        <font-awesome-icon icon="fa-solid fa-calendar-days" />
                    </div>
                    <v-list-item-content>
                        <v-list-item-title>My Reservetion</v-list-item-title>
                    </v-list-item-content>
                </NuxtLink>
            </v-list-item>
            <v-list-item class="main-menu" v-if="$auth.loggedIn">
                <NuxtLink to="/notifications">
                    <div class="menu-icon">
                        <font-awesome-icon icon="fa-solid fa-triangle-exclamation"  class="new-notification" v-if="new_notifications"/>
                        <font-awesome-icon icon="fa-solid fa-message" />
                    </div>
                    <v-list-item-content>
                        <v-list-item-title>Notifications</v-list-item-title>
                    </v-list-item-content>
                </NuxtLink>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
export default {
    name: 'Menu',
    data() {
        return {
            new_notifications: false
        }
    },
    watch: {
        '$auth.loggedIn': function(val) {
            if(val) {
                this.$fetch()
            }
        }
    },
    async fetch() {
        if (this.$auth.loggedIn) {
            var _self = this
            await this.$axios.post('/notifications/check', { user_id: this.$auth.user.id }).then(function (response) {
                _self.new_notifications = response.data
            })
        }
    },
    methods: {
        async logout() {
            try {
                await this.$auth.logout();
            } catch (error) { }
        }
    },
}
</script>

<style scoped>
.custom-menu {
    background-color: rgb(65 90 119 / 80%);
}

.custom-menu a {
    text-decoration: none;
    color: #e0e1dd;
    font-weight: bold;
}

.custom-menu div {
    color: #e0e1dd !important;
}

.logo img {
    width: 100%;
}

.welcome {
    margin-bottom: 12px;
}

.logged-username {
    font-size: 18px;
    font-weight: 100 !important;
}

.menu-avatar img {
    width: 100%;
}

.menu-icon svg {
    padding: 0 12px;
    vertical-align: bottom;
}

.main-menu a {
    border-radius: 8px;
    width: 100%;
    display: flex;
}

.main-menu a:hover {
    background-color: rgb(65 90 119 / 100%);
    ;
}
.new-notification{
    color: red;
    padding: 0 !important;
    font-size: 12px;
    position: absolute;
    top: 7px;
    left: 35px;
}
</style>