export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'PreAlb',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', type: 'text/css', href: '//fonts.googleapis.com/css?family=Quicksand:300,400,600,700,800' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '~/assets/css/app.css',
    '@fortawesome/fontawesome-svg-core/styles.css'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/fontawesome',
    { src: '~/plugins/underscore', ssr: false }
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    '@nuxtjs/vuetify'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/toast',
    "vue-sweetalert2/nuxt"
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: 'http://127.0.0.1:8000/api/v1',
  },

  // Auth
  auth: {
    strategies: {
      local: {
        scheme: 'refresh',
        localStorage: {
          prefix: 'auth.'
        },
        token: {
          prefix: 'access_token.',
          property: 'access_token',
          maxAge: 86400,
          type: 'Bearer'
        },
        refreshToken: {
          prefix: 'refresh_token.',
          property: 'refresh_token',
          data: 'refresh',
          maxAge: 60 * 60 * 24 * 15
        },
        user: {
          property: 'user',
          autoFetch: true
        },
        endpoints: {
          login: { url: '/users/login', method: 'post' },
          refresh: { url: '/token/refresh/', method: 'post' },
          user: { url: '/users/user', method: 'get' },
          logout: { url: '/users/logout', method: 'post' }
        },
      }
    }
  },
  //Toast
  toast: {
    position: 'top-center',
    duration: 1300,
    className: 'custom-toastr',
    fitToScreen: true,
    keepOnHover: true
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
