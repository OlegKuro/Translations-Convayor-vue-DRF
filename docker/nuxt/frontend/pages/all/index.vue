<template>
  <v-card>
    <v-card-title>
      <v-row justify="space-between" class="align-center px-2">
        <v-breadcrumbs class="px-0">
          <v-breadcrumbs-item to="/all" disabled>All tasks</v-breadcrumbs-item>
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
      <tasks-list>
      </tasks-list>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    name: "index",
    methods: {
      create() {
        this.$toast.info('Not implemented yet :C');
      }
    }
  }
</script>
