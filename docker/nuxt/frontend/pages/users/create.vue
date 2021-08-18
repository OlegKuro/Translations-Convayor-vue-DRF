<template>
  <v-card>
    <v-card-title>
      <v-breadcrumbs class="px-0">
        <v-breadcrumbs-item to="/users" exact>Users</v-breadcrumbs-item>
        <v-icon small>mdi-chevron-right</v-icon>
        <v-breadcrumbs-item to="/users/create" disabled>Create</v-breadcrumbs-item>
      </v-breadcrumbs>
    </v-card-title>
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
  import userFormFields from '../../mixins/user-form-mixin';

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
    mixins: [
      userFormFields,
    ],
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
        if (this.isCreatingNow) {
          return
        }
        if (await this.validateForm('userForm')) {
          return
        }
        this.isCreatingNow = true;
        await this.syncWithBackend('post', '/users/', 'Successfully created new user');
        this.isCreatingNow = false;
      },
    }
  }
</script>
