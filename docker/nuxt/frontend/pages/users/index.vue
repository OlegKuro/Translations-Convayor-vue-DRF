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
        :items="items"
        :options.sync="pagination"
        :server-items-length="total"
        :footer-props="{
              itemsPerPageOptions: [10, 20, 30, 50],
        }"
      >
        <template v-slot:item.actions="{item}">
          <v-btn
            :to="`/users/${item.id}`"
            color="secondary"
            fab
            x-small
            title="edit"
          >
            <v-icon x-small>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            @click="deleteUser(item.id)"
            color="error"
            fab
            x-small
            title="edit"
          >
            <v-icon x-small>mdi-delete-outline</v-icon>
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
  import indexPageListMixin from '@/mixins/index-page-list-mixin';

  export default {
      name: 'UsersIndex',
      async fetch() {
        await this.loadUsers();
      },
      mixins: [
          indexPageListMixin,
      ],
      data() {
        return {
          ROLES_TRANSLATIONS,
          headers: [
            {text: 'Email', sortable: false, value: 'email'},
            {text: 'Roles', sortable: false, value: 'roles'},
            {text: 'Actions', sortable: false, value: 'actions'},
          ],
        }
      },
      methods: {
        create() {
          this.$router.replace({name: 'users-create'});
        },
        deleteUser(userId) {
          this.$toast.error(`Let's be civil to our teammates...`);
          setTimeout(() => {
            this.$toast.info(`No, I haven't implemented user destroying yet`)
          }, 3000);
        },
        async loadUsers() {
          if (this.loading) {
            return
          }
          try {
            this.loading = true;
            // prevent overlappings
            const {data} = await this.$axios.get('/users/', {
              params: {
                page: this.pagination.page,
                page_size: this.pagination.itemsPerPage,
              },
            });
            this.items = data.results;
            this.total = data.count;
          } finally {
            this.loading = false;
          }
        }
      },
      watch: {
        pagination: {
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
