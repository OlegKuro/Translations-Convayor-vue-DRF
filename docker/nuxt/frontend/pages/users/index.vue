<template>
  <div></div>
</template>

<script>
    export default {
      fetchOnServer: false,
      async fetch() {
        this.users = await this.$axios.get('/users/');
      },
      data() {
        return {
          users: [],
        }
      },
      name: "UsersIndex",
    }
</script>
