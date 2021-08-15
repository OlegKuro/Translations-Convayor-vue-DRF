<template>
  <v-container>
    <v-row class="my-2">
      <v-text-field
        :value="user.email"
        @input="updateField('email', $event)"
        :error-messages="emailError"
        :disabled="disabled"
        label="User email"
        outlined
        hide-details="auto"
        single-line
        dense
      ></v-text-field>
    </v-row>
    <v-row class="mb-2">
      <v-text-field
        :value="user.password"
        @input="updateField('password', $event)"
        :error-messages="passwordError"
        :disabled="disabled"
        label="password"
        outlined
        hide-details="auto"
        single-line
        dense
        type="password"
      ></v-text-field>
      <v-spacer></v-spacer>
      <v-text-field
        :value="user.repeatPassword"
        @input="updateField('repeatPassword', $event)"
        :error-messages="passwordRepeatError"
        :disabled="disabled"
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
        :disabled="disabled"
        @input="updateField('roles', $event)"
        :error-messages="rolesError"
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
  import {ROLES_TRANSLATIONS} from '../constants/roles';
  import {cloneDeep, set, get} from 'lodash';
  import {validationMixin} from 'vuelidate';
  import {required, minLength, sameAs, maxLength, not} from 'vuelidate/lib/validators';

  const validateEmail = function(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  };

  export default {
    name: "UserModelForm",
    mixins: [
        validationMixin,
    ],
    model: {
      prop: 'user',
      event: 'change',
    },
    props: {
      user: {
        type: Object,
        required: true,
      },
      disabled: {
        type: Boolean,
        default: false,
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
      emailError() {
        const errors = [];
        if (!this.$v.user.email.$dirty) return errors;
        !this.$v.user.email.required && errors.push('Email is required field');
        !this.$v.user.email.validateEmail && errors.push('Please type in correct email');
        return errors;
      },
      passwordError() {
        const errors = [];
        if (!this.$v.user.password.$dirty) return errors;
        !this.$v.user.password.required && errors.push('Please fill the password');
        !this.$v.user.password.minLength && errors.push('Must contain at least 8 characters');
        !this.$v.user.password.maxLength && errors.push('Not greater than 128 characters please');
        !this.$v.user.password.differ && errors.push('Password can not be the same as email');
        return errors;
      },
      passwordRepeatError() {
        const errors = [];
        if (!this.$v.user.repeatPassword.$dirty) return errors;
        !this.$v.user.repeatPassword.samePassword && errors.push('Password mismatch');
        return errors;
      },
      rolesError() {
        const errors = [];
        if (!this.$v.user.roles.$dirty) return errors;
        !this.$v.user.roles.required && errors.push('Please pick some roles');
        !this.$v.user.roles.minLength && errors.push('User should have at least 1 role');
        return errors;
      },
    },
    methods: {
      updateField(fieldName, value) {
        const user = cloneDeep(this.user);
        set(user, fieldName, value);
        this.$emit('change', user);
        this.touchVuelidateField(fieldName);
      },
      touchVuelidateField(fieldName) {
        get(this.$v.user, fieldName).$touch();
      },
    },
    validations() {
      return {
        user: {
          email: {
            required,
            validateEmail,
          },
          password: {
            required,
            minLength: minLength(8),
            maxLength: maxLength(128),
            differ: not(sameAs('email')),
          },
          repeatPassword: {
            samePassword: sameAs('password'),
          },
          roles: {
            required,
            minLength: minLength(1),
          },
        }
      }
    }
  }
</script>
