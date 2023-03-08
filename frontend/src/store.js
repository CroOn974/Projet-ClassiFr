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
            APIData: ''
        }
    },
    mutations: {
        updateStorage(state, { access, refresh }) {
          state.accessToken = access;
          state.refreshToken = refresh;
        },
        destroyToken(state) {
          state.accessToken = null;
          state.refreshToken = null;
        },
        storeUserData(state, { access, refresh }) {
          state.accessToken = access;
          state.refreshToken = refresh;
        }
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
              username: usercredentials.username,
              password: usercredentials.password
            })
            .then(response => {
              context.commit('updateStorage', { access: response.data.access, refresh: response.data.refresh });
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
                context.commit('storeUserData', { access: response.data.access, refresh: response.data.refresh });
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