import {ROLES} from "../constants/roles";

const state = () => ({
  name: 'Translators Convayor',
  roleToAvailableMenuSections: {
    [ROLES.ADMIN]: [
      'users',
      'available-tasks',
      'qa-tasks',
      'done-tasks',
      'my',
      'all',
    ],
    [ROLES.ROLE_TRANSLATOR]: [
      'available-tasks',
      'my',
    ],
    [ROLES.ROLE_QA]: [
      'qa-tasks',
      'my',
    ],
  },
  availableSections: [],
});

const mutations = {
  setAvailableSections(state, sections) {
    state.availableSections = sections;
  }
};

const getters = {

};

const actions = {

};

export {state, getters, mutations, actions};
