export default function ({ store, route, error, redirect }) {
  if (route.path == '/login' || !store.state.auth.loggedIn) {
    return Promise.resolve();
  }

  const myAvailableSections = store.state.app.availableSections;

  if (route.path === '/') {
    if (!myAvailableSections.length) {

      return error({statusCode: 403, message: 'You have no roles. Please contact administrator'})
    }
    return redirect('/' + myAvailableSections[0]);
  }

  const routeBasePath = route.path.split('/').filter(s => !!s)[0];

  if (!myAvailableSections.includes(routeBasePath)) {
    return error({statusCode: 403, message: 'This page is forbidden for you due to insufficient permissions'})
  } else {
    return Promise.resolve()
  }
}
