export default function ({store}) {
  if (!store.state.auth.loggedIn) {
    return Promise.resolve();
  }
  
  // Set of available sections based on user's roles and role sections availability map
  const {roleToAvailableMenuSections} = store.state.app;
  let myAvailableSections = Object
    .entries(roleToAvailableMenuSections)
    .filter(([role, menuSections]) => store.state.auth.user.roles.includes(+role))
    .map(([role, menuSections]) => [...menuSections])
    .flat();

  store.commit('app/setAvailableSections', myAvailableSections);

  return Promise.resolve();
}
