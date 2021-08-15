<template>
  <v-container>
    <v-row class="my-2">
      <v-text-field
        :value="user.email"
        @input="updateField('email', $event)"
        label="User email"
        outlined
        hide-details="auto"
        single-line
        dense
      ></v-text-field>
    </v-row>
    <v-row class="mb-2">
      <v-text-field
        :value="user.password[0]"
        @input="updateField('password.0', $event)"
        label="password"
        outlined
        hide-details="auto"
        single-line
        dense
        type="password"
      ></v-text-field>
      <v-spacer></v-spacer>
      <v-text-field
        :value="user.password[1]"
        @input="updateField('password.1', $event)"
        label="password again"
        outlined
        hide-details="auto"
        single-line
        dense
        type="password"
      ></v-text-field>
    </v-row>
    <v-row class="mb-2">
      <v-select
        :value="user.roles"
        :items="rolesOptions"
        @input="updateField('roles', $event)"
        item-value="value"
        item-text="label"
        label="User roles"
        multiple
        chips
        dense
        hide-details="auto"
        single-line
        outlined
      ></v-select>
    </v-row>
  </v-container>
</template>

<script>
  import {ROLES_TRANSLATIONS} from "../constants/roles";
  import {cloneDeep, set} from 'lodash';

  export default {
    name: "UserModelForm",
    model: {
      prop: 'user',
      event: 'change',
    },
    props: {
      user: {
        type: Object,
        required: true,
      },
    },
    computed: {
      isCreatingMode() {
        return 'id' in this.value;
      },
      rolesOptions() {
        const options = [];
        Object.entries(ROLES_TRANSLATIONS).forEach(([role, translation]) => {
          options.push({
            label: translation,
            value: role,
          })
        });
        return options;
      },
    },
    methods: {
      updateField(fieldName, value) {
        const user = cloneDeep(this.user);
        set(user, fieldName, value);
        this.$emit('change', user);
      },
    }
  }
</script>
