<template>
    <div>
      <div>
        <b-navbar type="dark" variant="dark">
          <b-navbar-nav style="padding: 25px;">
            <b-nav-item style="position: absolute; top: 5%;">
              <h2>BlogLite</h2></b-nav-item>
            <b-nav-item @click="goHome()" style="position: absolute; top: 18%; left: 80%;">
              <i class="bi bi-house"></i> Home</b-nav-item>
            <b-nav-item-dropdown text= "Profile" left
            style="position: absolute; top: 18%; left: 88%;">
              <b-dropdown-item @click="goEdit()"><i class="bi bi-gear">
              </i> Edit Profile</b-dropdown-item>
              <b-dropdown-item @click="logout()"><i class="bi bi-box-arrow-right"></i>
                Logout</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-navbar>
      </div>
        <div id="profile" class="card">
            <img class="card-img-top rounded-circle"
            v-bind:src="require('../../../static/images/' + user.profile_photo)"
            width="200" height="200" alt="profile photo" />
            <div class="card-body">
                <h5 class="card-title">{{ user["name"] }}</h5>
                <h7>@{{ user["username"] }}</h7><br><br>
                <b-button v-if="!follow" variant="primary" size="sm"
                @click="follow_user()">
                  Follow</b-button>
                <b-button v-if="follow" size="sm"
                @click="unfollow_user()">Unfollow</b-button>
                <p class="card-text">{{ user['bio'] }}</p>
            </div>
        </div>
        <div id="posts">
            <div class="col">
                <div class="card" v-for="post in posts" :key="post" style="width: 40rem;">
                    <div class="card-body">
                    <img class="rounded-circle" style="width: 1cm;"
            v-bind:src="require('../../../static/images/' + post.user.profile_photo)"
            alt="post photo" />
               <b-link @click="$event=>toUser(post.username)"
                style="font-weight: bold; font-size: medium; color: black;">
                @{{ post["username"] }}</b-link><br><br>
                    <img class="card-img-top" id="poster"
            v-bind:src="require('../../../static/images/' + post.post_photo)"
            alt="post photo" /><br><br>
                    <b-link @click="toPost(post.post_id)"
                    style="font-weight: bold; font-size: large; color: black;"
                    class="card-title">{{post["title"]}}</b-link>
                    <p class="card-text">{{post["description"]}}</p>
                </div>
                </div>
            </div>
        </div>
    </div>
  </template>

<script>
/* eslint-disable */
import CustomFetch from './CustomFetch';
  export default {
    name: 'User',
    data() {
      return {
        follow:false,
        view_user: window.location.pathname.split("/").at(-1),
        user: [],
        posts: [],
        commentForm: {
            post_id: null,
            body: '',
            commenter: null,
        }
      }
      },
      mounted() {
        this.getUser();
        this.getPost();
      },
      methods: {
        getUser() {
          CustomFetch('http://localhost:8080/user/'+this.view_user, {
            method: 'GET',
            mode: 'cors',
          })
          .then((res) => {
            this.user = res;
          })
          .catch((error) => {
            console.error(error);
          });
        },
        getPost() {
          CustomFetch('http://localhost:8080/post/'+this.view_user, {
            method: 'GET',
            mode: 'cors',
          })
          .then((res) => {
            this.posts = res;
            this.posts = this.posts.reverse()
          })
          .catch((error) => {
            console.error(error);
          });
        },
      toUser(username) {
        console.log(username)
      },
      toPost(post_id) {
        this.$router.push({path:'/posts/'+post_id})
      },
      goHome() {
        this.$router.push({path:'/dashboard'})
      },
      goEdit() {
        this.$router.push({path:'/profilesettings'})
      },
      logout() {
        CustomFetch('http://localhost:8080/logout', {
            method: 'GET',
            mode: 'cors',
          })
          .then((res) => {
            this.$router.push({path:'/'})
          })
          .catch((error) => {
            console.error(error);
          });
      },
      follow_user(){
        this.follow=true;
      },
      unfollow_user(){
        this.follow=false;
      }
      } 
    }
</script>

<style>
#profile {
  position: fixed;
  font-size: 10px;
  top: 15%;
  left: 5%;
  padding: 15px;
  background-color: lavender;
}

#posts {
    padding: 10px;
    margin-top: 6%;
    margin-left: 35%;
}

.card{
    margin-bottom: 12px;
}

</style>
