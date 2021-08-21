<template>
  <v-card>
    <v-card-title>
      <div class="v-flex">
        <span v-if="isCreationMode">
          New task
        </span>
        <span v-if="task.id">Task {{task.id}}</span>
      </div>
    </v-card-title>
    <v-card-text class="px-5">
      <v-row class="my-2">
        <v-textarea
          rows="3"
          :value="task.origin"
          @input="updateField('origin', $event)"
          :readonly="originReadOnly"
          :disabled="disabled"
          class="mr-1"
          label="Text to translate"
          outlined
          auto-grow
          counter
        ></v-textarea>
        <v-textarea
          v-if="!isCreationMode"
          :value="task.translation"
          @input="updateField('translation', $event)"
          :readonly="translationReadOnly"
          :disabled="disabled"
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
          :value="task.deadline"
          @input="updateField('deadline', $event)"
          :disabled="disabled || isDeadlineReadOnly"
          label="Deadline (optional)"
          :text-field-props="{
            dense: true,
            outlined: true
          }"
        >
        </datetimepicker>
      </v-row>
      <template v-if="!isCreationMode">
        <v-row>
          <v-textarea
            :value="task.comment"
            :readonly="isCommentReadOnly"
            @input="updateField('comment', $event)"
            :disabled="disabled"
            rows="2"
            label="Comment"
            outlined
            auto-grow
            counter
          ></v-textarea>
        </v-row>
        <v-row v-if="isAdmin">
          <v-text-field
            :value="task.assigned_qa"
            @input="updateField('assigned_qa', $event)"
            :disabled="disabled"
            label="Assigned QA ID"
            dense
            outlined
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-text-field
            :value="task.translator"
            @input="updateField('translator', $event)"
            :disabled="disabled"
            label="Translator ID"
            dense
            outlined
          ></v-text-field>
        </v-row>
      </template>
    </v-card-text>
    <v-card-actions>
      <v-btn
        v-if="isCreationMode"
        :disabled="disabled"
        small
        outlined
        color="primary"
        @click="create"
      >
        Create
      </v-btn>
      <v-btn
        v-else-if="task.state != TASK_STATES.COMPLETED || isAdmin"
        :disabled="disabled"
        small
        outlined
        color="primary"
        @click="update"
      >
        Update
      </v-btn>
      <v-btn
        small
        :disabled="disabled"
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
  import {TASK_STATES_TRANSLATIONS, TASK_STATES} from "../constants/task_states";
  import {cloneDeep, set} from "lodash";
  import {ROLES} from "../constants/roles";

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
      mode: {
        type: String,
        required: true,
        validator(val) {
          return ['create', 'edit-admin', 'edit'].includes(val);
        },
      },
      disabled: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        TASK_STATES,
      }
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
      isCreationMode() {
        return this.mode === 'create';
      },
      isAdmin() {
        return this.$auth.user.roles.includes(ROLES.ADMIN);
      },
      originReadOnly() {
        return !this.isAdmin;
      },
      translationReadOnly() {
        return !(this.isAdmin
          || (this.$auth.user.id == this.task.translator
          && this.task.state == TASK_STATES.IN_PROGRESS));
      },
      isDeadlineReadOnly() {
        return !this.isAdmin;
      },
      isCommentReadOnly() {
        return !(
          this.isAdmin ||
          (this.task.state == TASK_STATES.VERIFYING && this.$auth.user.id == this.task.assigned_qa) ||
          (this.task.state == TASK_STATES.IN_PROGRESS && this.$auth.user.id == this.task.translator)
        )
      },
    },
    methods: {
      create() {
        this.$emit('create');
      },
      update() {
        this.$emit('update');
      },
      updateField(fieldName, value) {
        const task = cloneDeep(this.task);
        set(task, fieldName, value);
        this.$emit('change', task);
      },
    }
  }
</script>
