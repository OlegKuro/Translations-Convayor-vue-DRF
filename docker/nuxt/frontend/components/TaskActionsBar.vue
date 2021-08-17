<template>
  <v-flex>
    <template v-if="isAdmin">
      <v-select
        :value="state.toString()"
        :items="statesOptions"
        :disabled="disabled"
        @input="changeState($event)"
        item-value="value"
        item-text="label"
        label="Set new task state"
        dense
        hide-details="auto"
        single-line
        outlined
        @click.stop
      ></v-select>
    </template>
    <template v-else>

      <template v-if="state === TASK_STATES.NEW">
        <v-btn
          outlined
          color="secondary"
          rounded
          small
          title="Assign this task to me"
          :disabled="disabled"
          @click="changeState(TASK_STATES.IN_PROGRESS)"
        >
          Start translation
        </v-btn>
      </template>
      <template v-if="state === TASK_STATES.IN_PROGRESS">
        <v-btn
          outlined
          color="success"
          rounded
          small
          title="Approve translation variant and sent to QA"
          :disabled="disabled"
          @click="changeState(TASK_STATES.NEEDS_QA)"
        >
          Send to QA
        </v-btn>
      </template>
      <template v-if="state === TASK_STATES.NEEDS_QA">
        <v-btn
          outlined
          color="success"
          rounded
          small
          title="Take to verify"
          :disabled="disabled"
          @click="changeState(TASK_STATES.VERIFYING)"
        >
          Take to verify
        </v-btn>
      </template>
      <template v-if="state === TASK_STATES.VERIFYING">
        <v-btn
          outlined
          color="error"
          rounded
          small
          title="Sends task back into the QA list"
          :disabled="disabled"
          @click="changeState(TASK_STATES.NEEDS_QA)"
        >
          Unassign me
        </v-btn>
        <v-btn
          outlined
          color="success"
          rounded
          small
          title="Approve translation and send to a client"
          :disabled="disabled"
          @click="changeState(TASK_STATES.COMPLETED)"
        >
          Approve
        </v-btn>
        <v-btn
          outlined
          color="primary"
          rounded
          small
          title="Assign to the author of translation in order to get new variant"
          :disabled="disabled"
          @click="changeState(TASK_STATES.IN_PROGRESS)"
        >
          Send back to the translator
        </v-btn>
      </template>
    </template>
  </v-flex>
</template>

<script>
  import {TASK_STATES, TASK_STATES_TRANSLATIONS} from "../constants/task_states";
  import {ROLES} from "../constants/roles";

  export default {
    name: "TaskActionsBar",
    props: {
      state: {
        type: Number,
        required: true,
        validator(val) {
          return Object.values(TASK_STATES).includes(val);
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
      isAdmin() {
        return this.$auth.user.roles.includes(ROLES.ADMIN);
      },
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
    },
    methods: {
      changeState(newState) {
          this.$emit('change', +newState);
      },
    }
  }
</script>
