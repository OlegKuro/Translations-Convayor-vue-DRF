<template>
  <div></div>
</template>

<script>
    export default {
      name: 'UsersIndex',
      async fetch() {
        const {data} = await this.$axios.get('/users/');
        this.users = data;
      },
      data() {
        return {
          users: [],
        }
      },
    }
</script>
