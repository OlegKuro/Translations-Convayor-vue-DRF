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
          this.goBack();
        } catch (e) {
          if (e.response.status === 400) {
            const details = await e.response.data;
            if ('email' in details) {
              this.$toast.error(details.email);
            }
          } else {
            this.$toast.error(Object.values(e.response.data).join(' \\ '));
          }
          console.error(e)
        } finally {
          this.isCreatingNow = false;
        }
      },
      goBack() {
        this.$router.replace({name: 'users'});
      },
      prepareUserFields() {
        const user = cloneDeep(this.user);
        delete user.repeatPassword;
        return user
      },
    }
  }
</script>
