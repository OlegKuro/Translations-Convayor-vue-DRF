<template>
  <div class="mt-3">
    <v-row justify="end">
      <v-btn
        @click="create"
        small
        color="primary"
      >
        Create
      </v-btn>
    </v-row>
  </div>
</template>

<script>
    export default {
      name: 'UsersIndex',
      async fetch() {
        const {data} = await this.$axios.get('/users/');
        this.users = data;
      },
      data() {
        return {
          users: [],
        }
      },
      methods: {
        create() {
          this.$router.replace({name: 'users-create'});
        }
      }
    }
</script>
