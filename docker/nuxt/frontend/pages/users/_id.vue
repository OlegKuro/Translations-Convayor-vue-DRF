<template>
  <v-card>
    <v-row>
      <v-text-field
        v-model="email"
        label="email"
      ></v-text-field>
    </v-row>
  </v-card>
</template>

<script>
    export default {
      name: "CertainUser",
      data() {
        return {
          email: null,
          password: [null, null],
          roles: [],
        }
      }
    }
</script>
