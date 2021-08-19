<template>
  <v-app>
    <v-container fill-height>
      <v-layout row wrap align-center justify-center>
        <v-flex sm12 md6 lg-3>
          <h1 class="display-1 mb-4 primary--text">{{ name }}</h1>
          <v-card>
            <v-card-text>
              <h3>Please login to continue...</h3>
            </v-card-text>
            <v-card-text>
              <nuxt/>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
  import {mapState} from 'vuex';

  export default {
    name: "login",
    computed: {
      ...mapState('app', {
        name: 'name',
      })
    },
    beforeMount() {
      this.$vuetify.theme.dark = localStorage.getItem('dark') !== 'false';
    },
  }
</script>
