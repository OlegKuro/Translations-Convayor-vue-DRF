<template>
  <v-card>
    <v-card-title>
      <v-row justify="space-between" class="align-center px-2">
        <v-breadcrumbs class="px-0">
          <v-breadcrumbs-item to="/done-tasks" disabled>Completed tasks</v-breadcrumbs-item>
        </v-breadcrumbs>
      </v-row>
    </v-card-title>
    <v-card-text>
      <tasks-list :params="params">
      </tasks-list>
    </v-card-text>
  </v-card>
</template>

<script>
  import {TASK_STATES} from "../../constants/task_states";

  export default {
    name: "index",
    computed: {
      params() {
        return {
          state: [TASK_STATES.COMPLETED],
        }
      }
    }
  }
</script>
