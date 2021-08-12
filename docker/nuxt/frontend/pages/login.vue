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
        }
      }
    },
    methods: {
      async submit() {
        try {
          await this.$auth.loginWith(
            'local',
            { data: this.credentials }
            );
          this.$toast.success('Успешный вход');
          this.$nuxt.$router.go({ path: '/' });
        } catch (e) {
          console.log(e);
          this.$toast.error('Не удалось войти');
        }
      }
    }
  }
</script>
