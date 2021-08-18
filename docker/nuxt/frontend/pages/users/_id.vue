<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between">
      <v-breadcrumbs class="px-0">
        <v-breadcrumbs-item to="/users" exact>Users</v-breadcrumbs-item>
        <v-icon small>mdi-chevron-right</v-icon>
        <v-breadcrumbs-item :to="`/users/${userId}`" exact>{{userId}}</v-breadcrumbs-item>
      </v-breadcrumbs>
      <v-switch
        label="Change password"
        v-model="setPassword"
        dense
      ></v-switch>
    </v-card-title>
    <v-card-text class="px-4">
      <user-model-form
        v-if="this.user"
        v-model="user"
        :disabled="isUpdating"
        :set-password="setPassword"
        ref="userForm"
      ></user-model-form>
    </v-card-text>
    <v-card-actions class="px-4">
      <v-btn
        color="success"
        @click="update"
        :disabled="isUpdating"
      >
        Update
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
    import userFormMixin from '../../mixins/user-form-mixin';

    export default {
      name: "CertainUser",
      async fetch() {
        await this.loadUser();
      },
      mixins: [
        userFormMixin,
      ],
      data() {
        return {
          user: null,
          isUpdating: false,
          setPassword: false,
        }
      },
      computed: {
        userId() {
          return this.$route.params.id;
        },
      },
      methods: {
        async loadUser() {
          const {data} = await this.$axios.get(`/users/${this.userId}`);
          data.roles = data.roles.map(r => r.toString());
          this.user = data;
        },
        async update() {
          if (this.isUpdating) {
            return
          }
          if (await this.validateForm('userForm')) {
            return
          }
          this.isUpdating = true;
          await this.syncWithBackend('patch', '/users/' + this.userId, 'Successfully updated');
          this.isUpdating = false;
        },
      }
    }
</script>
