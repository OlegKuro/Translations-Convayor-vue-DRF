<template>
  <div class="px-3" @keyup.enter="submit">
    <v-text-field
      label="email"
      v-model="credentials.username"
    ></v-text-field>
    <v-text-field
      label="password"
      type="password"
      v-model="credentials.password"
    ></v-text-field>
    <v-btn
      class="mx-0 mb-4"
      @click="submit"
      :disabled="isRequestProcessing"
      outlined
      color="primarys"
    >
      Login
    </v-btn>
  </div>
</template>

<script>
  export default {
    layout: 'login',
    middleware: 'auth',
    data() {
      return {
        credentials: {
          username: null,
          password: null
        },
        isRequestProcessing: false,
      }
    },
    methods: {
      async submit() {
        try {
          this.isRequestProcessing = true;
          await this.$auth.loginWith(
            'local',
            { data: this.credentials }
            );
          this.$toast.success('Successfully logged in');
          this.$nuxt.$router.go({ path: '/' });
        } catch (e) {
          console.log(e);
          this.$toast.error('Unable to log in');
        } finally {
          this.isRequestProcessing = false;
        }
      }
    }
  }
</script>
