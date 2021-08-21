<template>
  <v-card>
    <v-card-title>
      <v-row justify="space-between" class="align-center px-2">
        <v-breadcrumbs class="px-0">
          <v-breadcrumbs-item to="/all" disabled>All tasks</v-breadcrumbs-item>
        </v-breadcrumbs>
        <v-btn
          @click="createBtn"
          small
          color="primary"
        >
          Create
          <v-icon
            small
            class="ml-2"
          >
            mdi-plus
          </v-icon>
        </v-btn>
      </v-row>
    </v-card-title>
    <v-card-text>
      <tasks-list
        ref="tasksList"
      >
      </tasks-list>
    </v-card-text>
    <v-dialog
      v-model="modalShown"
      persistent
      max-width="50vw"
    >
      <task-edit-model-form
        v-model="task"
        @close="closeModal"
        @create="create"
        :disabled="isCreatingNow"
        mode="create"
      ></task-edit-model-form>
    </v-dialog>
  </v-card>
</template>

<script>
  function newTask() {
    return {
      origin: null,
      deadline: null,
    }
  }

  export default {
    name: "index",
    data() {
      return {
        modalShown: false,
        task: newTask(),
        isCreatingNow: false,
      }
    },
    methods: {
      async createBtn() {
        this.task = newTask();
        this.modalShown = true;
      },
      closeModal() {
        this.modalShown = false;
      },
      async create() {
        if (this.isCreatingNow) return;
        this.isCreatingNow = true;
        try {
          this.isCreatingNow = true;
          await this.$axios.post('/translations/', this.task);
          this.$refs.tasksList.loadTasks();
          this.closeModal();
        } finally {
          this.isCreatingNow = false;
        }
      }
    }
  }
</script>
