<template>
  <v-card>
    <v-card-title>Create new user:</v-card-title>
    <v-card-text class="px-4">
      <user-model-form
        v-model="user"
      ></user-model-form>
    </v-card-text>
    <v-card-actions class="px-4">
      <v-btn
        color="success"
        @click="create"
      >
        Create
      </v-btn>
      <v-btn
        color="error"
        @click="clear"
      >
        Clear
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  import {cloneDeep} from 'lodash';

  function userFields() {
    return {
      email: null,
      password: [null, null],
      roles: [],
    }
  }

  export default {
    name: "create",
    data() {
      return {
        user: userFields(),
      }
    },
    methods: {
      clear() {
        this.user = userFields();
      },
      async create() {
        try {
          await this.$axios.post('/users/', this.prepareUserFields());
          this.$toast.success('New user created');
          this.$router.replace({name: 'users'});
        } catch (e) {
          console.log(e);
        }
      },
      prepareUserFields() {
        const user = cloneDeep(this.user);
        user.password = user.password[0];
        return user
      },
    }
  }
</script>
