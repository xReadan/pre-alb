<template>
    <v-app id="page">
        <div class="background-image"></div>
        <Menu />
        <v-main>
            <v-container fill-height>
                <Nuxt />
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
export default {

}
</script>

<style scoped>
#page {
    font-family: 'Quicksand';
}
.background-image {
    position: absolute;
    background-image: url('~/assets/images/background.jpg');
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    filter: blur(4px);
    -webkit-filter: blur(4px);
    height: 100%;
    width: 100%;
}
</style>