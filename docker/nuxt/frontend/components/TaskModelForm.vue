<template>
  <v-card>
    <v-card-title>Task {{task.id}}</v-card-title>
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
  }
</script>
