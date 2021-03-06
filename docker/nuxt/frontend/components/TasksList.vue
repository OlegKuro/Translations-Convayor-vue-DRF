<template>
  <v-card class="tasks-list">
    <v-card-title>
      <slot name="head"></slot>
    </v-card-title>
    <v-card-text>
      <v-data-iterator
        :items="items"
        :items-per-page="pagination.itemsPerPage"
        :loading="loading"
        :footer-props="{
              itemsPerPageOptions: [6, 12, 24, 36],
        }"
      >
        <template v-slot:default="{items}">
          <v-row>
            <v-col
              v-for="item in items"
              :key="item.id"
              cols="12"
              sm="6"
              md="4"
              lg="3"
            >
              <v-card
                :color="item.color"
                @click="showModal(item)"
              >
                <div class="d-flex flex-no-wrap justify-space-between">
                  <div class="flex-grow-0">
                    <v-card-title
                      class="text-h6 break-word"
                    >
                      {{item.origin | crop}}
                    </v-card-title>

                    <v-card-subtitle v-if="item.deadline">
                      Until {{item.deadline | date_format}}
                    </v-card-subtitle>

                    <v-card-actions>
                      <task-actions-bar
                        :state="item.state"
                        :translation="item.translation"
                        :disabled="loading"
                        @change="changeTaskState(item, $event)"
                      ></task-actions-bar>
                    </v-card-actions>
                  </div>

                  <div
                    class="d-flex ma-3"
                  >
                    <v-chip
                      large
                      :color="TASK_COLORS[item.state]"
                    >
                      {{TASK_STATES_TRANSLATIONS[item.state]}}
                    </v-chip>
                  </div>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </template>
      </v-data-iterator>
    </v-card-text>
    <v-dialog
      v-model="modalShown"
      persistent
      max-width="50vw"
    >
      <task-edit-model-form
        v-model="selectedTask"
        :mode="editingMode"
        v-if="selectedTask"
        :disabled="loading"
        @close="closeModal"
        @update="updateTask"
      ></task-edit-model-form>
    </v-dialog>
  </v-card>
</template>

<script>
  import indexPageListMixin from '../mixins/index-page-list-mixin';
  import * as moment from 'moment';
  import {TASK_STATES_TRANSLATIONS, TASK_COLORS, TASK_STATES} from "../constants/task_states";
  import {isString, truncate, cloneDeep, get} from 'lodash';
  import {ROLES} from "../constants/roles";

  export default {
    async fetch() {
      await this.loadTasks();
    },
    name: "TasksList",
    props: {
      // constant params part
      params: {
        type: Object,
        default: () => {},
      },
    },
    mixins: [
      indexPageListMixin,
    ],
    data() {
      return {
        pagination: {
          itemsPerPage: 12,
          page: 1,
        },
        TASK_STATES_TRANSLATIONS,
        TASK_COLORS,
        modalShown: false,
        selectedTask: null,
      }
    },
    mounted() {
      this.$socketIO.subscribe('tasks').on('available', this.newTaskAppearedListener.bind(this));
    },
    beforeDestroy() {
      this.$socketIO.socket.removeAllListeners('available');
      this.$socketIO.unsubscribe('tasks');
    },
    computed: {
      editingMode() {
        return this.$auth.user.roles.includes(ROLES.ADMIN) ? 'edit-admin': 'edit';
      },
    },
    methods: {
      newTaskAppearedListener({id, state}) {
        if (get(this.params, 'state', []).includes(state)) {
          this.$toast.info('New available task appeared!');
          this.loadTasks();
        }
      },
      async updateTask() {
        if (this.loading) return;
        try {
          this.loading = true;
          await this.$axios.patch('/translations/' + this.selectedTask.id, this.selectedTask);
          this.loading = false;
          await this.closeModal();
          this.loadTasks();
        } finally {
          this.loading = false;
        }
      },
      async loadTasks() {
        if (this.loading) {
          return
        }
        try {
          this.loading = true;
          const params = new URLSearchParams();
          Object.entries({
            page: this.pagination.page,
            page_size: this.pagination.itemsPerPage,
            ...this.params,
          }).forEach(([key, val]) => {
            if (Array.isArray(val)) {
              val.forEach(arrItem => params.append(key, arrItem));
              return
            }
            params.append(key, val);
          });
          const {data} = await this.$axios.get('/translations/', {
            params,
          });
          this.items = data.results;
          this.total = data.count;
        } finally {
          this.loading = false;
        }
      },
      showModal(task) {
        this.selectedTask = cloneDeep(task);
        this.selectedTask.state = this.selectedTask.state.toString();
        this.modalShown = true;
      },
      async closeModal() {
        this.modalShown = false;
        await this.$nextTick();
        this.selectedTask = null;
      },
      async changeTaskState(item, {state, onSuccess}) {
        this.loading = true;
        if (item.assigned_qa && state === TASK_STATES.NEEDS_QA && item.state === TASK_STATES.IN_PROGRESS) {
          state = TASK_STATES.VERIFYING;
        }
        try {
          await this.$axios.put(`/translations/${item.id}`, {
            ...item,
            state: state,
          });
          item.state = state;
          onSuccess && onSuccess();
        } finally {
          this.loading = false;
        }
        await this.loadTasks();
      },
    },
    filters: {
      date_format(value, format = 'DD.MM.YYYY HH:mm') {
        return moment(value).format(format);
      },
      /**
       * @param {String} value
       * @param {Number} length
       */
      crop(value, length = 30) {
        if (!isString(value)) {
          console.error('Tried to trim not String param');
          return value;
        }
        return truncate(value, {
          length,
        })
      }
    }
  }
</script>

<style lang="scss">
  .tasks-list {
    .v-card {
      cursor: pointer;
      transition: box-shadow 200ms;
      &:hover {
        // elevation-5
        box-shadow: 0px 3px 5px -1px rgb(0 0 0 / 20%), 0px 5px 8px 0px rgb(0 0 0 / 14%), 0px 1px 14px 0px rgb(0 0 0 / 12%) !important;
      }
      .break-word {
        word-break: break-word;
      }
    }
  }
</style>
