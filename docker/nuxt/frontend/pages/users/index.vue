<template>

  <v-card>
    <v-card-title>
      <v-row justify="space-between" class="align-center px-2">
        <v-breadcrumbs class="px-0">
          <v-breadcrumbs-item to="/users" disabled>Users</v-breadcrumbs-item>
        </v-breadcrumbs>
        <v-btn
          @click="create"
          small
          color="primary"
        >
          Create
          <v-icon small class="ml-2">mdi-plus</v-icon>
        </v-btn>
      </v-row>
    </v-card-title>
    <v-card-text>
      <v-data-table
        :headers="headers"
        :loading="loading"
        :items="users"
        :options.sync="paginationOptions"
        :server-items-length="totalUsersCount"
        :footer-props="{
              itemsPerPageOptions: [10, 20, 30, 50],
              prevIcon: 'mdi-chevron-left',
              nextIcon: 'mdi-chevron-right',
        }"
      >
        <template v-slot:item.actions="{item}">
          <v-btn
            @click="edit(item.id)"
            color="secondary"
            fab
            x-small
            title="edit"
          >
            <v-icon x-small>mdi-pencil</v-icon>
          </v-btn>
        </template>
        <template v-slot:item.roles="{item}">
          <v-chip
            v-for="role in item.roles"
            :key="role"
            small
            class="mr-1"
            color="accent"
          >
            {{ROLES_TRANSLATIONS[role]}}
          </v-chip>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
    import {ROLES_TRANSLATIONS} from "../../constants/roles";

    export default {
      name: 'UsersIndex',
      async fetch() {
        await this.loadUsers();
      },
      data() {
        return {
          users: [],
          ROLES_TRANSLATIONS,
          headers: [
            {text: 'Email', sortable: false, value: 'email'},
            {text: 'Roles', sortable: false, value: 'roles'},
            {text: 'Actions', sortable: false, value: 'actions'},
          ],
          loading: false,
          paginationOptions: {
            page: 1,
            itemsPerPage: 20,
          },
          totalUsersCount: 0,
        }
      },
      methods: {
        create() {
          this.$router.replace({name: 'users-create'});
        },
        edit(userId) {
          this.$toast.info(`Editing form for user ${userId} is not implemented yet :C`);
        },
        async loadUsers() {
          if (this.loading) {
          }
          try {
            this.loading = true;
            // prevent overlappings
            const {data} = await this.$axios.get('/users/', {
              params: {
                page: this.paginationOptions.page,
                page_size: this.paginationOptions.itemsPerPage,
              },
            });
            this.users = data.results;
            this.totalUsersCount = data.count;
          } finally {
            this.loading = false;
          }
        }
      },
      watch: {
        paginationOptions: {
          deep: true,
          handler(opts, oldOpts) {
            if (Object.keys(opts).length !== Object.keys(oldOpts).length) {
              return
            }
            this.loadUsers();
          }
        }
      }
    }
</script>
