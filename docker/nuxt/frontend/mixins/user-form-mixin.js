import {cloneDeep} from "lodash";

export default {
  methods: {
    goBack() {
      this.$router.replace({name: 'users'});
    },
    async validateForm(formRef) {
      const formComponent = this.$refs[formRef];
      formComponent.$v.$reset();
      await this.$nextTick();
      formComponent.$v.$touch();
      return formComponent.$invalid;
    },
    /**
     *
     * @param {String} method
     * @param {String} url
     * @param {String} successText
     * @return {Promise<void>}
     */
    async syncWithBackend(method, url, successText) {
      try {
        this.isUpdating = true;
        await this.$axios[method](url, this.prepareUserFields());
        this.$toast.success(successText);
        this.goBack();
      } catch (e) {
        if (e.response.status === 400) {
          const details = await e.response.data;
          if ('email' in details) {
            this.$toast.error(details.email);
          }
        } else {
          this.$toast.error(Object.values(e.response.data).join(' \\ '));
        }
      }
    },
    prepareUserFields() {
      const user = cloneDeep(this.user);
      delete user.repeatPassword;
      return user
    },
  },
}
