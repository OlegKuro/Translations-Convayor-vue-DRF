<template>
  <v-card>
    <v-card-title>Create new user:</v-card-title>
    <v-card-text class="px-4">
      <user-model-form
        v-model="user"
        :disabled="isCreatingNow"
        ref="userForm"
      ></user-model-form>
    </v-card-text>
    <v-card-actions class="px-4">
      <v-btn
        color="success"
        @click="create"
        :disabled="isCreatingNow"
      >
        Create
      </v-btn>
      <v-btn
        color="error"
        @click="clear"
        :disabled="isCreatingNow"
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
      password: null,
      repeatPassword: null,
      roles: [],
    }
  }

  export default {
    name: "create",
    data() {
      return {
        user: userFields(),
        isCreatingNow: false,
      }
    },
    methods: {
      clear() {
        this.user = userFields();
        this.$refs.userForm.$v.$reset();
      },
      async create() {
        this.$refs.userForm.$v.$reset();
        await this.$nextTick();
        this.$refs.userForm.$v.$touch();
        if (this.$refs.userForm.$v.$invalid) {
          return
        }
        try {
          this.isCreatingNow = true;
          await this.$axios.post('/users/', this.prepareUserFields());
          this.$toast.success('New user created');
          this.$router.replace({name: 'users'});
        } catch (e) {
          console.error(e);
        } finally {
          this.isCreatingNow = false;
        }
      },
      prepareUserFields() {
        const user = cloneDeep(this.user);
        delete user.repeatPassword;
        return user
      },
    }
  }
</script>
