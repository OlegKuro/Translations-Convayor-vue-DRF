<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn
        icon
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon
          :title="miniVariant ? 'expand sidebar menu' : 'minify sidebar menu'"
        >
          mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}
        </v-icon>
      </v-btn>
      <v-toolbar-title v-text="user ? user.email : 'anon'" />
      <v-spacer></v-spacer>
      <div>
        <v-btn
          icon
          @click.stop="toggleDarkMode"
          title="switch between light/dark mode"
        >
          <v-icon>{{isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night'}}</v-icon>
        </v-btn>
        <v-btn
          icon
          @click.stop="logout"
          title="logout"
        >
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </div>
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>&copy; Khayatov Oleg</span>
    </v-footer>
  </v-app>
</template>

<script>
  export default {
    data () {
      return {
        clipped: false,
        drawer: false,
        fixed: false,
        items: [
          {
            icon: 'mdi-account-multiple',
            title: 'Users management',
            to: '/users'
          }
        ],
        miniVariant: false,
        right: true,
        user: this.$auth.user,
      }
    },
    computed: {
      isDark() {
        return !!this.$vuetify.theme.dark;
      },
    },
    methods: {
      toggleDarkMode() {
        this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
      },
      async logout() {
        await this.$auth.logout();
        this.$router.go('/');
      },
    }
  }
</script>
