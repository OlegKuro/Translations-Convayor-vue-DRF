<template>
  <tasks-list :params="params">
  </tasks-list>
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
