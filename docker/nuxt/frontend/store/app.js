import {ROLES} from "../constants/roles";

const state = () => ({
  name: 'Translators Convayor',
  roleToAvailableMenuSections: {
    [ROLES.ADMIN]: [
      'users',
    ],
    [ROLES.ROLE_TRANSLATOR]: [

    ],
    [ROLES.ROLE_QA]: [

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
