<template>
  <div class="User-Page">
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
      <div id="profile-dash" class="profile-card"  style="width: 16rem;">
          <img class="card-img-top rounded-circle" style="width: 6cm; height: 6cm;"
          v-bind:src="require('../../../static/images/' + user.profile_photo)"
          width="200" height="200" alt="profile photo" />
          <div class="card-body">
              <h5 class="card-title">{{ user["name"] }}</h5>
              <h7>@{{ user["username"] }}</h7><br><br>
              <h7>Followers: {{ user["followers"] }}</h7><br>
              <b-button v-if="!follow" variant="primary" size="sm"
              @click="follow_user()">
                Follow</b-button>
              <b-button v-if="follow" size="sm"
              @click="unfollow_user()">Following</b-button>
              <p class="card-text">{{ user['bio'] }}</p>
          </div>
      </div>
      <div id="posts">
          <div class="col">
              <div class="card" v-for="post in posts" :key="post" style="width: 40rem;">
                  <div class="card-body">
                  <img class="rounded-circle" style="width: 1cm; height: 1cm;"
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
                  <b-button v-if="!likes.includes(post.post_id)"
                  variant="default" @click="likePost(post.post_id)">
                    <strong><i class="bi bi-hand-thumbs-up"></i>
                      <img src="../../../static/images/like.png" alt="liked"
                      style="height: 30px; width: 30px;">
                      ({{ post["likes_num"]  }})</strong></b-button>
                    <b-button v-if="likes.includes(post.post_id)"
                  variant="default" @click="unlikePost(post.post_id)">
                    <strong><i class="bi bi-hand-thumbs-up"></i>
                      <img src="../../../static/images/liked.png" alt="liked"
                      style="height: 30px; width: 30px;">
                      ({{ post["likes_num"] }})</strong></b-button>
                  <b-button variant="default" @click="toPost(post.post_id)">
                    <strong><i class="bi bi-chat"></i>
                    <img src="../../../static/images/comment.png" alt="comment"
                    style="height: 30px; width: 30px;">
                    ({{ post["comments_num"]  }})</strong></b-button>
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
      likes:[],
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
      this.getLikes();
      this.getUser();
      this.getFollows();
      this.getPost();
    },
    methods: {
      getLikes() {
        CustomFetch('http://localhost:8080/like/*', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          console.log(res)
          for(let i = 0; i < res.length; i++) {
            this.likes.push(res[i]["post_id"])
          }
          console.log(this.likes)
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getFollows() {
        CustomFetch('http://localhost:8080/follow/*', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          for(let i = 0; i < res.length; i++) {
            if(res[i].following == this.user.username) {
              this.follow = true
              break
            }
          }
        })
        .catch((error) => {
          console.error(error);
        });
      },
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
      const payload = {
          following: this.user.username,
        };
        console.log(payload)
        CustomFetch('http://localhost:8080/follow', {
          method: 'POST',
          body: JSON.stringify(payload),
          mode: 'cors',
          headers: {
                  'Content-Type': 'application/json',
              },
        })
        .then(() => {
          this.getUser();
          this.getFollows();
          this.getPost();
        })
        .catch((error) => {
          console.error(error);
        });
        this.getUser();
        this.getFollows();
    },
    unfollow_user(){
      this.follow=false;
      CustomFetch('http://localhost:8080/follow/'+this.user.username, {
          method: 'DELETE',
          mode: 'cors',
        })
        .then(() => {
          this.$router.go()
        })
        .catch((error) => {
          this.$router.go();
        });
        this.getUser();
        this.getFollows();
    },
    unlikePost(post_id) {
      CustomFetch(`http://localhost:8080/like/${post_id}`, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
          'Content-type': 'application/json',
        },
      })
      .then(() => {
        this.getUser();
        this.getPost();
      })
      .catch((error) => {
        console.error(error);
        this.getUser();
        this.getPost();
      });
    },
    likePost(post_id) {
      console.log("post a like")
      const new_like = {"post_id": post_id}
      CustomFetch("http://localhost:8080/like", {
              method: 'POST',
              body: JSON.stringify(new_like),
              mode: 'cors',
              headers: {
                  'Content-Type': 'application/json',
              },
          })
      .then(() => {
        this.getUser();
        this.getLikes();
        this.getPost();
      })
      .catch((error) => {
        console.log(error);
        this.getUser();
        this.getLikes();
        this.getPost();
      });
    },
    toPost(post_id) {
      this.$router.push({path:'/posts/'+post_id})
    }
    } 
  }
</script>

<style>
.User-Page {
  background-image: url("../../../static/images/login-back.png");
  background-size: cover;
  height: 100%;
}
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
#profile-dash{
position: fixed;
font-size: 10px;
top: 15%;
left: 5%;
color: white;
padding: 15px;
box-shadow: 0px 0px 10px rgba(213, 121, 121, 5);
}

</style>
