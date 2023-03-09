import { createStore } from 'vuex'
import { getAPI } from './axios-api'
import VuexPersistence from 'vuex-persist'

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
  });

export default createStore({
    plugins: [vuexLocal.plugin],
    state(){
        return {
            accessToken: null,
            refreshToken: null,
            APIData: '',
            isSuperUser: false
        }
    },
    mutations: {
        updateStorage(state, { access, refresh ,isSuperUser}) {
          state.accessToken = access;
          state.refreshToken = refresh;
          state.isSuperUser = isSuperUser;
        },
        destroyToken(state) {
          state.accessToken = null;
          state.refreshToken = null;
          state.isSuperUser = false;
        },
        storeUserData(state, { access, refresh, isSuperUser }) {
          state.accessToken = access;
          state.refreshToken = refresh;
          state.isSuperUser = isSuperUser;
        },
      },
      getters: {
        loggedIn(state) {
          return state.accessToken !== null;
        }
      },
      actions: {
        userLogout(context) {
          if (context.getters.loggedIn) {
            context.commit('destroyToken');
          }
        },
        userLogin(context, usercredentials) {
          return new Promise((resolve, reject) => {
            getAPI.post('api/api-token/', {
              is_super_user: false,
              username: usercredentials.username,
              password: usercredentials.password
            })
            .then(response => {
              console.log(response.data.is_super_user);
              context.commit('updateStorage', { access: response.data.access, refresh: response.data.refresh, isSuperUser: response.data.is_super_user });
              resolve();
            })
            .catch(err => {
              reject(err);
            });
          });
        },
        userSignup(context, usercredentials) {
            return new Promise((resolve, reject) => {
              getAPI.post('api/signup/', {
                username: usercredentials.username,
                password: usercredentials.password
              })
              .then(response => {
                // Store User signin  data 
                context.commit('storeUserData', { access: response.data.access, refresh: response.data.refresh, isSuperUser: response.data.is_super_user  });
                resolve(response.data);
              })
              .catch(err => {
                console.log(err)
                // Handle error here
                reject(err);
              });
            });
        }
    }
})