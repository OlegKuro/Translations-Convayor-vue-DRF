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
              :key="item.name"
              cols="12"
              sm="6"
              md="4"
              lg="3"
            >
              <v-card
                :color="item.color"
              >
                <div class="d-flex flex-no-wrap justify-space-between">
                  <div>
                    <v-card-title
                      class="text-h6 break-word"
                    >
                      {{item.origin | crop}}
                    </v-card-title>

                    <v-card-subtitle v-if="item.deadline">
                      Until {{item.deadline | date_format}}
                    </v-card-subtitle>

                    <v-card-actions>

                      <v-btn
                        outlined
                        color="secondary"
                        rounded
                        small
                      >
                        Actions
                      </v-btn>
                    </v-card-actions>
                  </div>

                  <v-avatar
                    class="ma-3"
                    size="75"
                    tile
                  >
                    <v-chip
                      large
                      :color="TASK_COLORS[item.state]"
                    >
                      {{TASK_STATES_TRANSLATIONS[item.state]}}
                    </v-chip>
                  </v-avatar>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </template>
      </v-data-iterator>
    </v-card-text>
  </v-card>
</template>

<script>
  import indexPageListMixin from '../mixins/index-page-list-mixin';
  import * as moment from 'moment';
  import {TASK_STATES_TRANSLATIONS, TASK_COLORS} from "../constants/task_states";
  import {isString, truncate} from 'lodash';

  export default {
    async fetch() {
      await this.loadTranslations();
    },
    name: "TasksList",
    props: {
      // constant params part
      params: {
        type: Object,
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
      }
    },
    methods: {
      async loadTranslations() {
        if (this.loading) {
          return
        }
        try {
          this.loading = true;
          const {data} = await this.$axios.get('/translations/', {
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
