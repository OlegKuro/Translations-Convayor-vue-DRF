<template>
  <v-card>
    <v-card-title>
      <div class="v-flex">
        <span>Task {{task.id}}</span>
      </div>
    </v-card-title>
    <v-card-text class="px-5">
      <v-row class="my-2">
        <v-textarea
          rows="3"
          class="mr-1"
          label="Text to translate"
          outlined
          auto-grow
          counter
        ></v-textarea>
        <v-textarea
          rows="3"
          class="ml-1"
          label="Translation"
          outlined
          auto-grow
          counter
        ></v-textarea>
      </v-row>
      <v-row class="mb-2">
        <datetimepicker
          label="Deadline (optional)"
          :text-field-props="{
            dense: true,
            outlined: true,
          }"
        >
        </datetimepicker>
      </v-row>
      <v-row>
        <v-textarea
          rows="2"
          label="Comment"
          outlined
          auto-grow
          counter
        ></v-textarea>
      </v-row>
      <v-row>
        <v-select
          :items="statesOptions"
          item-value="value"
          item-text="label"
          label="Task state"
          dense
          single-line
          outlined
        ></v-select>
      </v-row>
      <v-row>
        <v-text-field
          label="assigned QA"
          dense
          outlined
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-text-field
          label="Translators"
          dense
          outlined
        ></v-text-field>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        small
        outlined
        color="default"
        @click="$emit('close')"
      >
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  import {TASK_STATES_TRANSLATIONS} from "../constants/task_states";

  export default {
    name: "TaskModelForm",
    model: {
      prop: 'task',
      event: 'change',
    },
    props: {
      task: {
        type: Object,
        required: true,
      },
    },
    computed: {
      statesOptions() {
        const options = [];
        Object.entries(TASK_STATES_TRANSLATIONS).forEach(([state, translation]) => {
          options.push({
            label: translation,
            value: state,
          })
        });
        return options;
      },
    }
  }
</script>
